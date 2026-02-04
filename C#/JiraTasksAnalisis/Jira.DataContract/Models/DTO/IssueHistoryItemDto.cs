namespace Jira.DataContract.Models.DTO
{
    public class IssueHistoryItemDto
    {
        public string Field { get; set; }

        public string FieldType { get; set; }

        public string From { get; set; }
        
        public string FromString { get; set; }
        
        public string To { get; set; }
        
        public string ToString { get; set; }
    }
}