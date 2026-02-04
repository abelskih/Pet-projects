using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Jira.API;
using Jira.DataContract.Models.DTO;
using JiraTasksAnalisis;
using MathNet.Numerics.Statistics;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using Jira.DataContract.Models.Responses;
using Refit;

namespace JiraTaskAnalizer
{

    public class TasksAnalisis : BackgroundService
    {
        public TasksAnalisis(IServiceProvider services, IOptions<AppSettings> settings, IGoogleSheetsHelper googleSheetsHelper)
        {
            Services = services;
            Settings = settings.Value;
            GoogleSheets = googleSheetsHelper ?? throw new ArgumentNullException(nameof(googleSheetsHelper));
        }

        public async Task<List<IssueHistoryDto>> historyTask (string key)
        {
            var jiraApi = Services.GetRequiredService<IGamesJiraClient>();
            var history = new List<IssueHistoryDto>();
            var historyCount = 0;
            var historyStartedAt = 0;
            try
            {
                do
                {
                    var historyResponse = await jiraApi.GetIssueHistory(key, historyStartedAt);
                    var changeLog = historyResponse.Content.Changelog;
                    history.AddRange(changeLog.Histories);
                    historyStartedAt += changeLog.MaxResults;
                    historyCount = changeLog.Total;
                    System.Threading.Thread.Sleep(150);
                } while (historyStartedAt < historyCount);

                return history;
            }
            catch (Exception e)
            {
                Console.WriteLine("Attempt to read {0} failed",key);
                Console.WriteLine(e.Message);
                return new List<IssueHistoryDto>();
            }
        }
        
        public async Task<List<IssueDto>> IssueList (string jql)
        {
            var jiraApi = Services.GetRequiredService<IGamesJiraClient>();
            var issues = new List<IssueDto>();
            var count_task = 0;
            var startedAt = 0;
            try
            {
                do
                {
                    var tasksResponse = await jiraApi.GetIssues(jql, startedAt);
                    var tasks = tasksResponse.Content;
                    startedAt += tasks.MaxResults;
                    if (tasks != null && tasks.Total>0)
                    {
                        count_task = tasks.Total;
                        issues.AddRange(tasks.Issues);
                    }
                    else issues.Add(new IssueDto() {Key = "NO",Id = "0"});
                }
                while (startedAt < count_task);

                return issues;
            }
            catch (Exception e)
            {
                Console.WriteLine("Attempt to read {0} failed",jql);
                Console.WriteLine(e.Message);
                return new List<IssueDto>();
            }
        }

        public async Task<string> issueStatus(string key)
        {
            var jiraApi = Services.GetRequiredService<IGamesJiraClient>();
            var startedAt = 0;
            string status = "";
            try
            {
                var Field = await jiraApi.GetIssueStatus(key, 0);
                status = Field.Content.Fields.Status.name;
                return status;
            }
            catch (Exception e)
            {
                Console.WriteLine("Error read status issue {0} ",key);
                Console.WriteLine(e.Message);
                return "";
            }
        }

        public async Task Wait_Time( List<IssueDto> iisues, String status, DateTime limit, string id_table,string sheetName,string range, double days_limit,int p, int id_team)
        {
            var dictionary = new Dictionary<string, totalTimes>();
            var tasklist = new List<string> ();
            var GS = GoogleSheets;
            int t = 2;
            
            if (id_team==0) GS.ClearValues(id_table,"tasks", GS.toRange(p,p+2,2));
            foreach (var issue in iisues)
            {
                //if (issue.Key=="ALLIANCE-62373")
                    Console.WriteLine(issue.Key);
                
                var history = new List<IssueHistoryDto>();
                int tick = 0;
                while ((history.Count==0 || history==null) && tick < 10)
                {
                    history = await historyTask(issue.Key);
                    tick++;
                    System.Threading.Thread.Sleep(100);
                }

                if (history != null || history.Count>0)
                {

                    double totalDays = 0;
                    double totalHours = 0;
                    double lastDays = 0;
                    DateTime startTime = DateTime.MinValue;
                    DateTime lastTime = DateTime.MinValue;
                    foreach (var issueHistory in history)
                    {
                        var changeStatusItem = issueHistory.Items.FirstOrDefault(x => x.Field == "status");
                        if (changeStatusItem != null)
                        {
                            if (changeStatusItem.ToString.ToUpper() == status.ToUpper() && issueHistory.CreatedDate < limit)
                            {
                                lastTime = issueHistory.CreatedDate;
                                if (startTime == DateTime.MinValue) startTime = issueHistory.CreatedDate;
                            }
                            else if (startTime != DateTime.MinValue && changeStatusItem.FromString.ToUpper() == status.ToUpper())
                            {
                                totalDays += ((issueHistory.CreatedDate < limit ? issueHistory.CreatedDate : limit) -
                                              startTime).TotalDays;
                                totalHours += ((issueHistory.CreatedDate < limit ? issueHistory.CreatedDate : limit) -
                                               startTime).TotalHours;
                                //lastDays = (issueHistory.CreatedDate - lastTime).TotalDays;
                                startTime = DateTime.MinValue;
                            }
                        }
                    }

                    if (startTime != DateTime.MinValue)
                    {
                        totalDays += (limit - startTime).TotalDays;
                        totalHours += (limit - startTime).TotalHours;
                        //lastDays = (DateTime.Today - lastTime).TotalDays;
                    }

                    var test = new totalTimes();
                    test.totalDays = totalDays;
                    test.totalHours = totalHours;
                    test.lastDays = lastDays;
                    dictionary.Add(issue.Key, test);
                    if (totalDays >= days_limit && days_limit>0 && id_team==0)
                    {
                        var checkStatus = "";
                        tick = 0;
                        while (checkStatus=="" && tick < 3)
                        {
                            checkStatus = await issueStatus(issue.Key);
                            tick++;
                            System.Threading.Thread.Sleep(100);
                        }
                        
                        GS.WriteTaskToGoogleSheets(id_table,"tasks",issue.Key,totalDays,checkStatus,p,t);
                        t++;
                    }
                }
                else
                {
                    Console.WriteLine("Error read history task - {0}",issue.Key);
                }
            }
            var avgtotal = dictionary.Average(x => x.Value.totalDays);
            var avghtotal =  dictionary.Average(x => x.Value.totalHours);
            //var avglast = dictionary.Average(x => x.Value.lastDays);
            //Console.WriteLine($"average time  in status {status} total = {avgtotal.ToString("0.00")} last = {avglast.ToString("0.00")}");
            GS.WriteDateToGoogleSheets(id_table,sheetName,avgtotal.ToString("0.00"),range);
            Console.WriteLine($"average time  in status {status} total = {avgtotal.ToString("0.00")} in hours = {avghtotal.ToString("0.00")} -> {(avghtotal/24).ToString(("0.00"))}");
        }

        protected IServiceProvider Services { get; }
        protected AppSettings Settings { get; }
        private IGoogleSheetsHelper GoogleSheets { get; }

        public async Task Analize() => await ExecuteAsync(new CancellationToken());

        private static string BuildTeamClause(teamsFilter team)
        {
            if (team == null || string.IsNullOrWhiteSpace(team.filter))
                return "";

            return $" and ({team.filter})";
        }

        private static string ApplyTemplate(string template, string project, teamsFilter team, int days)
        {
            if (string.IsNullOrWhiteSpace(template))
                return template;

            var teamFilter = team?.filter ?? "";
            return template
                .Replace("{project}", project ?? "", StringComparison.OrdinalIgnoreCase)
                .Replace("{team}", teamFilter, StringComparison.OrdinalIgnoreCase)
                .Replace("{days}", days.ToString(), StringComparison.OrdinalIgnoreCase);
        }

        private static string BuildJql(string project, teamsFilter team, valuesFilter filter, int days, string filterText)
        {
            if (filter == null)
                return "";

            if (!string.IsNullOrWhiteSpace(filter.JqlOverride))
                return ApplyTemplate(filter.JqlOverride, project, team, days);

            var teamClause = BuildTeamClause(team);
            if (string.Equals(filter.Period, "interval", StringComparison.OrdinalIgnoreCase))
                return $"project = \"{project}\"{teamClause} and ({filterText} AFTER endOfDay({-days}))";

            return $"project = \"{project}\"{teamClause} and {filterText}";
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            try
            {
                var jiraApi = Services.GetRequiredService<IGamesJiraClient>();
                var startedAt = 0;
                var issuesCount = 0;                
                var count_task = 0; 
                string jql = "";
                var GS = GoogleSheets;
                DateTime current_date = DateTime.Today.AddDays(-1);
                int days = 0;
                if (Settings.Interval_type == "AFTER")
                {
                    if (int.TryParse(Settings.Interval, out days))
                    {
                            current_date = DateTime.Today.AddDays(-days);
                    }
                    else Console.WriteLine("Error intreval for AFTER");
                    
                }
                else
                {
                        Console.WriteLine("type not implemented");
                }
                var dateToWrite = $"{current_date:dd.MM}-{DateTime.Today.AddDays(-1):dd.MM}";


                for (int id_project = 0; id_project < Settings.Projects.Count; id_project++)
                {
                    Console.WriteLine(Settings.Projects[id_project].Project);
                    var titles = new List<TitlesCollum>()
                        { new TitlesCollum() { Title = "Date", collum = Settings.Date_collum } };
                    for (int id_filter = 0; id_filter < Settings.Projects[id_project].Filtres.Count; id_filter++)
                    {
                        titles.Add(new TitlesCollum()
                        {
                            Title = Settings.Projects[id_project].Filtres[id_filter].Title,
                            collum = Settings.Projects[id_project].Filtres[id_filter].collum
                        });
                    }
                    //var sort_titles = titles.OrderBy(x => x.collum);

                    for (int id_team = 0; id_team < Settings.Projects[id_project].Teams.Count; id_team++)
                    {
                        if (GS.CheckSheetInTable(Settings.Projects[id_project].GoogleSheet, Settings.Projects[id_project].Teams[id_team].Name) ||
                            (GS.CreateSheetInTable(Settings.Projects[id_project].GoogleSheet, Settings.Projects[id_project].Teams[id_team].Name,
                                titles.OrderBy(x => x.collum))))
                        {
                            var row = GS.GetNextEmptyRow(Settings.Projects[id_project].Teams[id_team].Name, Settings.Projects[id_project].GoogleSheet);
                            GS.WriteDateToGoogleSheets(Settings.Projects[id_project].GoogleSheet, Settings.Projects[id_project].Teams[id_team].Name, dateToWrite,
                                $"{Settings.Date_collum}{row}");
                            Console.WriteLine($"Write teams {Settings.Projects[id_project].Teams[id_team].Name}");
                            var p = 1;
                            for (int id_filter = 0; id_filter < Settings.Projects[id_project].Filtres.Count; id_filter++)
                            {
                                Console.WriteLine($"Write filter {Settings.Projects[id_project].Filtres[id_filter].filter}");
                                var issues = new List<IssueDto>();
                                var filterConfig = Settings.Projects[id_project].Filtres[id_filter];
                                var teamConfig = Settings.Projects[id_project].Teams[id_team];

                                var filterText = filterConfig.filter;
                                if (filterConfig.Name.Contains("filter_time"))
                                    filterText = $"status = \"{filterConfig.filter}\" OR status changed FROM (\"{filterConfig.filter}\")";

                                if (Settings.Interval_type == "AFTER")
                                {
                                    jql = BuildJql(Settings.Projects[id_project].Project, teamConfig, filterConfig, days, filterText);
                                }
                                else
                                {
                                    Console.WriteLine("type not implemented");
                                    jql = "";
                                }

                                Console.WriteLine($"Filter: {Settings.Projects[id_project].Filtres[id_filter].Name} jql: {jql}");
                                
                                   
                                   int tick = 0;
                                   while (issues.Count==0 && tick < 3)
                                   {
                                       issues = await IssueList(jql);
                                     
                                       tick++;
                                       System.Threading.Thread.Sleep(200);
                                   }
                                   
                                   if (issues != null && issues.Count>0 && issues[0].Key != "NO")
                                   { 
                                       count_task= issues.Count;
                                   }
                                   else count_task = 0;

                                   if (Settings.Projects[id_project].Filtres[id_filter].Name.Contains("filter_time") && count_task>0)
                                {
                                    await Wait_Time(issues, Settings.Projects[id_project].Filtres[id_filter].filter, DateTime.Today,
                                        Settings.Projects[id_project].GoogleSheet, Settings.Projects[id_project].Teams[id_team].Name,
                                        $"{Settings.Projects[id_project].Filtres[id_filter].collum}{row}",Settings.Projects[id_project].Filtres[id_filter].limit,p,id_team);
                                    p=p+3;
                                }

                                //вывод в файл
                                if (Settings.Projects[id_project].Filtres[id_filter].Name.Contains("filter_count"))
                                    GS.WriteDateToGoogleSheets(Settings.Projects[id_project].GoogleSheet, Settings.Projects[id_project].Teams[id_team].Name,
                                        count_task.ToString(), $"{Settings.Projects[id_project].Filtres[id_filter].collum}{row}");
                            }
                        }
                        else
                            Console.WriteLine("Error write in table");
                    }

                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                throw;
            }
        }
    }
}
