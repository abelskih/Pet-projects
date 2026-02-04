using System.Collections.Generic;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using JiraTasksAnalisis;

namespace JiraTasksAnalisis.Tests
{
    internal sealed class FakeGoogleSheetsClient : IGoogleSheetsClient
    {
        internal Spreadsheet Spreadsheet { get; set; } = new Spreadsheet
        {
            Sheets = new List<Sheet>()
        };

        internal Dictionary<string, ValueRange> ValuesByRange { get; } = new Dictionary<string, ValueRange>();
        internal List<BatchUpdateSpreadsheetRequest> BatchUpdates { get; } = new List<BatchUpdateSpreadsheetRequest>();
        internal List<UpdateCall> Updates { get; } = new List<UpdateCall>();
        internal bool UpdateResult { get; set; } = true;
        internal int FailUpdatesBeforeSuccess { get; set; } = 0;

        public Spreadsheet GetSpreadsheet(string spreadsheetId) => Spreadsheet;

        public void BatchUpdate(string spreadsheetId, BatchUpdateSpreadsheetRequest request) =>
            BatchUpdates.Add(request);

        public ValueRange GetValues(string spreadsheetId, string range, SpreadsheetsResource.ValuesResource.GetRequest.MajorDimensionEnum? majorDimension = null)
        {
            if (ValuesByRange.TryGetValue(range, out var value))
                return value;

            return new ValueRange { Values = new List<IList<object>>() };
        }

        public bool TryUpdateValues(string spreadsheetId, string range, ValueRange valueRange)
        {
            Updates.Add(new UpdateCall(range, valueRange));
            if (FailUpdatesBeforeSuccess > 0)
            {
                FailUpdatesBeforeSuccess--;
                return false;
            }

            return UpdateResult;
        }

        public void ClearValues(string spreadsheetId, string range)
        {
        }

        internal sealed record UpdateCall(string Range, ValueRange ValueRange);
    }
}
