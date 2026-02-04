using System;
using System.Collections.Generic;
using System.Globalization;

namespace Jira.DataContract.Models.DTO
{
    public class IssueHistoryDto
    {
        public string Id { get; set; }

        public string Created { get; set; }
        
        public IEnumerable<IssueHistoryItemDto> Items { get; set; }

        public DateTime CreatedDate => DateTime.Parse(Created);
    }
}