using System.Collections.Generic;
using Jira.DataContract.Models.DTO;

namespace Jira.DataContract.Models.Responses
{
    public class GetIssueHistoryResponse: IssueDto
    {
        public ChangelogDto Changelog { get; set; }
    }
}