using System;
using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;

namespace JiraTasksAnalisis
{
    public sealed class GoogleSheetsClient : IGoogleSheetsClient
    {
        private readonly SheetsService _service;

        public GoogleSheetsClient(string credentialsPath)
        {
            GoogleCredential credential;
            using (var stream = System.IO.File.OpenRead(credentialsPath))
            {
                credential = GoogleCredential.FromStream(stream)
                    .CreateScoped(SheetsService.Scope.Spreadsheets);
            }

            _service = new SheetsService(new BaseClientService.Initializer
            {
                HttpClientInitializer = credential,
                ApplicationName = "JiraAnalisis",
            });
        }

        public Spreadsheet GetSpreadsheet(string spreadsheetId) =>
            _service.Spreadsheets.Get(spreadsheetId).Execute();

        public void BatchUpdate(string spreadsheetId, BatchUpdateSpreadsheetRequest request) =>
            _service.Spreadsheets.BatchUpdate(request, spreadsheetId).Execute();

        public ValueRange GetValues(string spreadsheetId, string range, SpreadsheetsResource.ValuesResource.GetRequest.MajorDimensionEnum? majorDimension = null)
        {
            var request = _service.Spreadsheets.Values.Get(spreadsheetId, range);
            if (majorDimension.HasValue)
                request.MajorDimension = majorDimension.Value;
            return request.Execute();
        }

        public bool TryUpdateValues(string spreadsheetId, string range, ValueRange valueRange)
        {
            var request = _service.Spreadsheets.Values.Update(valueRange, spreadsheetId, range);
            request.ValueInputOption = SpreadsheetsResource.ValuesResource.UpdateRequest.ValueInputOptionEnum.USERENTERED;
            try
            {
                request.Execute();
                return true;
            }
            catch (Exception e)
            {
                if (e.Message.Contains("exceeds grid limits"))
                {
                    Console.WriteLine("add collums");
                }

                return false;
            }
        }

        public void ClearValues(string spreadsheetId, string range)
        {
            var request = _service.Spreadsheets.Values.Clear(new ClearValuesRequest(), spreadsheetId, range);
            request.Execute();
        }
    }
}
