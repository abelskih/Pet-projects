using System.Collections.Generic;
using System.Linq;

namespace JiraTasksAnalisis
{
    public interface IGoogleSheetsHelper
    {
        bool CheckSheetInTable(string id_table, string sheetName);
        bool CreateSheetInTable(string id_table, string sheetName, IOrderedEnumerable<TitlesCollum> list);
        int GetNextEmptyRow(string sheetName, string id_table);
        void WriteDateToGoogleSheets(string id_table, string sheetName, string value, string rang);
        bool ClearValues(string id_table, string sheetName, string range);
        string toRange(int begin_col, int end_col, int begin_row, int end_row);
        string toRange(int begin_col, int end_col, int begin_row);
        void WriteTaskToGoogleSheets(string id_table, string sheetName, string value_key, double value_total, string status, int col, int row);
    }
}
