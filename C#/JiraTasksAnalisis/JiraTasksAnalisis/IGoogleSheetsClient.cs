using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;

namespace JiraTasksAnalisis
{
    public interface IGoogleSheetsClient
    {
        Spreadsheet GetSpreadsheet(string spreadsheetId);
        void BatchUpdate(string spreadsheetId, BatchUpdateSpreadsheetRequest request);
        ValueRange GetValues(string spreadsheetId, string range, SpreadsheetsResource.ValuesResource.GetRequest.MajorDimensionEnum? majorDimension = null);
        bool TryUpdateValues(string spreadsheetId, string range, ValueRange valueRange);
        void ClearValues(string spreadsheetId, string range);
    }
}
