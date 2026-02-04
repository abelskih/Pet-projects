using System.Collections.Generic;
using System.Linq;
using JiraTasksAnalisis;

namespace JiraTasksAnalisis.Tests
{
    internal sealed class FakeGoogleSheetsHelper : IGoogleSheetsHelper
    {
        internal bool SheetExists { get; set; } = true;
        internal int NextEmptyRow { get; set; } = 2;
        internal List<WriteCall> Writes { get; } = new List<WriteCall>();

        public bool CheckSheetInTable(string id_table, string sheetName) => SheetExists;

        public bool CreateSheetInTable(string id_table, string sheetName, IOrderedEnumerable<TitlesCollum> list) => true;

        public int GetNextEmptyRow(string sheetName, string id_table) => NextEmptyRow;

        public void WriteDateToGoogleSheets(string id_table, string sheetName, string value, string rang)
        {
            Writes.Add(new WriteCall(sheetName, rang, value));
        }

        public bool ClearValues(string id_table, string sheetName, string range) => true;

        public string toRange(int begin_col, int end_col, int begin_row, int end_row) =>
            $"{begin_col}:{end_col}:{begin_row}:{end_row}";

        public string toRange(int begin_col, int end_col, int begin_row) =>
            $"{begin_col}:{end_col}:{begin_row}";

        public void WriteTaskToGoogleSheets(string id_table, string sheetName, string value_key, double value_total, string status, int col, int row)
        {
        }

        internal sealed record WriteCall(string SheetName, string Range, string Value);
    }
}
