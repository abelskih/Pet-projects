namespace Jira.DataContract
{
    public class ApiRoutes
    {
        public const string GetIssues = "/search";
        public const string GetIssuesTestRail = "/issue/{key}?fields=customfield_78147";
        public const string GetIssueHistory = "/issue/{key}?expand=changelog";
        public const string GetIssueStatus = "/issue/{key}?fields=status";
    }
}