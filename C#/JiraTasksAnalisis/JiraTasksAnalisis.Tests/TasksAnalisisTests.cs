using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Jira.API;
using Jira.DataContract.Models.DTO;
using Jira.DataContract.Models.Responses;
using JiraTaskAnalizer;
using JiraTasksAnalisis;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;
using Moq;
using NUnit.Framework;
using Refit;

namespace JiraTasksAnalisis.Tests
{
    [TestFixture]
    public class TasksAnalisisTests
    {
        [Test]
        public async Task Analize_BuildsJql_And_WritesCount()
        {
            var jiraMock = new Mock<IGamesJiraClient>();
            var capturedJqls = new List<string>();

            jiraMock
                .Setup(x => x.GetIssues(It.IsAny<string>(), It.IsAny<int>()))
                .ReturnsAsync((string jql, int startAt) =>
                {
                    capturedJqls.Add(jql);
                    var response = new GetIssuesResponse
                    {
                        MaxResults = 50,
                        Total = 1,
                        Issues = new[] { new IssueDto { Key = "PRJ-1", Id = "1" } }
                    };
                    return ApiResponseFactory.Ok(response);
                });

            var settings = new AppSettings
            {
                Interval_type = "AFTER",
                Interval = "8",
                Date_collum = "A",
                Projects = new List<Projects>
                {
                    new Projects
                    {
                        Project = "Project1",
                        GoogleSheet = "sheet-id",
                        Teams = new List<teamsFilter>
                        {
                            new teamsFilter { Name = "Team1", filter = "component = Core" }
                        },
                        Filtres = new List<valuesFilter>
                        {
                            new valuesFilter
                            {
                                Name = "filter_count_done",
                                Title = "Done",
                                filter = "status changed to (Done)",
                                Period = "interval",
                                collum = "B"
                            }
                        }
                    }
                }
            };

            var googleSheets = new FakeGoogleSheetsHelper();
            var provider = new ServiceCollection()
                .AddSingleton(jiraMock.Object)
                .BuildServiceProvider();

            var sut = new TasksAnalisis(provider, Options.Create(settings), googleSheets);

            await sut.Analize();

            Assert.That(capturedJqls.Count, Is.EqualTo(1));
            Assert.That(
                capturedJqls[0],
                Is.EqualTo("project = \"Project1\" and (component = Core) and (status changed to (Done) AFTER endOfDay(-8))")
            );

            Assert.That(
                googleSheets.Writes.Any(w => w.Range == "B2" && w.Value == "1"),
                Is.True
            );
        }

        [Test]
        public async Task Analize_Uses_JqlOverride_Template()
        {
            var jiraMock = new Mock<IGamesJiraClient>();
            var capturedJqls = new List<string>();

            jiraMock
                .Setup(x => x.GetIssues(It.IsAny<string>(), It.IsAny<int>()))
                .ReturnsAsync((string jql, int startAt) =>
                {
                    capturedJqls.Add(jql);
                    var response = new GetIssuesResponse
                    {
                        MaxResults = 50,
                        Total = 0,
                        Issues = Array.Empty<IssueDto>()
                    };
                    return ApiResponseFactory.Ok(response);
                });

            var settings = new AppSettings
            {
                Interval_type = "AFTER",
                Interval = "8",
                Date_collum = "A",
                Projects = new List<Projects>
                {
                    new Projects
                    {
                        Project = "ProjectX",
                        GoogleSheet = "sheet-id",
                        Teams = new List<teamsFilter>
                        {
                            new teamsFilter { Name = "TeamX", filter = "assignee = test.user" }
                        },
                        Filtres = new List<valuesFilter>
                        {
                            new valuesFilter
                            {
                                Name = "filter_count_custom",
                                Title = "Custom",
                                filter = "status = Done",
                                Period = "interval",
                                collum = "B",
                                JqlOverride = "project = \"{project}\" and ({team}) and updated >= -{days}d"
                            }
                        }
                    }
                }
            };

            var googleSheets = new FakeGoogleSheetsHelper();
            var provider = new ServiceCollection()
                .AddSingleton(jiraMock.Object)
                .BuildServiceProvider();

            var sut = new TasksAnalisis(provider, Options.Create(settings), googleSheets);

            await sut.Analize();

            Assert.That(capturedJqls.Count, Is.EqualTo(1));
            Assert.That(
                capturedJqls[0],
                Is.EqualTo("project = \"ProjectX\" and (assignee = test.user) and updated >= -8d")
            );
        }

        private static class ApiResponseFactory
        {
            public static ApiResponse<T> Ok<T>(T content)
            {
                var response = new HttpResponseMessage(HttpStatusCode.OK);
                return new ApiResponse<T>(response, content, new RefitSettings(), null);
            }
        }
    }
}
