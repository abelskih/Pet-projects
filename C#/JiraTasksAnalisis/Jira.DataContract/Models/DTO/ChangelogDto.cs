using System.Collections.Generic;

namespace Jira.DataContract.Models.DTO
{
    public class ChangelogDto
    {
        public int StartAt { get; set; }
        public int MaxResults { get; set; }
        public int Total { get; set; }
        public IEnumerable<IssueHistoryDto> Histories { get; set; }
    }
}