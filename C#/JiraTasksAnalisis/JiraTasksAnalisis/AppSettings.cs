using System.Collections.Generic;
using System.Linq;

namespace JiraTasksAnalisis
{
    public class Projects
    {
        public string Project { get; set; }
        public string GoogleSheet { get; set; }
        public List<teamsFilter> Teams { get; set; }
        public List<valuesFilter> Filtres { get; set; }
    }
    public class teamsFilter
    {
        public string Name { get; set; }
        public string filter { get; set; }
    }
    
    public class valuesFilter
    {
        public string Name { get; set; }
        public string Title { get; set; }
        public string filter { get; set; }
        public string JqlOverride { get; set; }
        public double limit { get; set; }
        public string collum { get; set; }
        public string Period { get; set; }
    }

    public class totalTimes
    {
        public double totalDays { get; set; }
        public double totalHours { get; set; }
        public double lastDays { get; set; }
    }
    
    public class TitlesCollum
    {
        public string Title { get; set; }
        public string collum { get; set; }
    }

    public class AppSettings
    {
        public string JiraToken { get; set; }
        public string Interval_type { get; set; }
        public string Interval { get; set; }
        public string Date_collum { get; set; }
        public List<Projects> Projects { get; set; }
    }
}
