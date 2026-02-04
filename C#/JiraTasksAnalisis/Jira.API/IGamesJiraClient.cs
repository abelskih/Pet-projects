using System.Threading.Tasks;
using Jira.DataContract;
using Jira.DataContract.Models.Responses;
using Refit;

namespace Jira.API
{
    [Headers("Authorization: Bearer")]
    public interface IGamesJiraClient
    {
        [Get(ApiRoutes.GetIssues)]
        Task<ApiResponse<GetIssuesResponse>> GetIssues(string jql, int startAt);
        
        [Get(ApiRoutes.GetIssueHistory)]
        Task<ApiResponse<GetIssueHistoryResponse>> GetIssueHistory([AliasAs("key")]string task, int startAt);

        [Get(ApiRoutes.GetIssueStatus)]
        Task<ApiResponse<GetIssueStatusResponse>> GetIssueStatus([AliasAs("key")] string task, int startAt);
    }
}