using System.Collections.Generic;
using Jira.DataContract.Models.DTO;

namespace Jira.DataContract.Models.Responses
{
    public class GetIssuesResponse
    {
        public int StartAt { get; set; }
        public int MaxResults { get; set; }
        public int Total { get; set; }
        public IEnumerable<IssueDto> Issues { get; set; }
    }
}