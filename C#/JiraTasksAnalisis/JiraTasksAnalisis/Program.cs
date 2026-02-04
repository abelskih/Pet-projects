using Microsoft.Extensions.DependencyInjection;
using Jira.API;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using Refit;
using System;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Net.Http;
using JiraTaskAnalizer;
using GoogleSheets;

namespace JiraTasksAnalisis
{
    public class Program
    {
        static HttpClient client = new HttpClient();

        static async Task GetProductAsync (string path)
        {
            HttpResponseMessage response = await client.GetAsync(path);
            if (response.IsSuccessStatusCode)
            {
                var tmp = await response.Content.ReadAsStringAsync();
                Console.WriteLine(tmp);
            }          
        }

        public static void Main(string[] args)
        {
            try
            {
                var services = new ServiceCollection();

                ConfigureServices(services);

                services
                    .AddSingleton<TasksAnalisis, TasksAnalisis>()
                    .BuildServiceProvider()
                    .GetService<TasksAnalisis>()
                    .Analize()
                    .Wait();
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
            
            Console.WriteLine($"Console close after 60 sec");
            Thread.Sleep(60000);
        }

        private static void ConfigureServices(IServiceCollection services)
        {
            var config = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile($"appsettings.json", optional: false)
                .Build();

            services.AddOptions();            
            services.Configure<AppSettings>(config);
            services.AddSingleton<IGoogleSheetsHelper, GoogleSheetsHelper>();
            services.AddRefitClient<IGamesJiraClient>(serviceProvider => GetRefitSettingsForGamesJira(serviceProvider))
                .ConfigureHttpClient(c => c.BaseAddress = new Uri("url_here"));
            
        }

        private static RefitSettings GetRefitSettingsForGamesJira(IServiceProvider serviceProvider)
        {
            var settings = serviceProvider.GetRequiredService<IOptions<AppSettings>>();
            var token = settings.Value.JiraToken;
            return new RefitSettings()
            {
                AuthorizationHeaderValueGetter = (message,cancellationToken) => Task.FromResult(token),
            };
        }
    }
}
