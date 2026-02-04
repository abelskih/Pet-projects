using System;
using System.Collections.Generic;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using MathNet.Numerics.Statistics;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using System.Globalization;
using JiraTasksAnalisis;

namespace GoogleSheets
{
   
    public class GoogleSheetsHelper : IGoogleSheetsHelper
    {
        private readonly IGoogleSheetsClient _client;
        private readonly ISleeper _sleeper;

        public GoogleSheetsHelper()
        {
            _client = new GoogleSheetsClient("config.json");
            _sleeper = new ThreadSleeper();
        }

        public GoogleSheetsHelper(IGoogleSheetsClient client, ISleeper sleeper = null)
        {
            _client = client ?? throw new ArgumentNullException(nameof(client));
            _sleeper = sleeper ?? new ThreadSleeper();
        }
        
        public bool CheckSheetInTable(string id_table, string sheetName)
        { var check = false;
            try
            {
                Spreadsheet ss = _client.GetSpreadsheet(id_table);
                foreach (Sheet sheet in ss.Sheets)
                {
                    if (sheet.Properties.Title == sheetName) check = true;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error check sheet in table {id_table}");
                Console.WriteLine($"Error - {e.Message}");
            }
            return check;
        }
        
        public bool ClearValues(string id_table, string sheetName, string range)
        { var check = false;
            try
            {
                _client.ClearValues(id_table, sheetName + '!' + range);
                check = true;
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error clear table {id_table}");
                Console.WriteLine($"Error - {e.Message}");
            }
            return check;
        }
        
        public string toRange(int begin_col, int end_col, int begin_row, int end_row)
        { var check = "";
            try
            {
                check = $"{GetExcelColumnName(begin_col)}{begin_row}:{GetExcelColumnName(end_col)}{end_row}";
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error create Range");
                Console.WriteLine($"Error - {e.Message}");
            }
            return check;
        }
        
        public string toRange(int begin_col, int end_col,int begin_row)
        { var check = "";
            try
            {
                check = $"{GetExcelColumnName(begin_col)}{begin_row}:{GetExcelColumnName(end_col)}";
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error create Range");
                Console.WriteLine($"Error - {e.Message}");
            }
            return check;
        }
        
        public bool CreateSheetInTable(string id_table, string sheetName, IOrderedEnumerable<TitlesCollum> list)
        { 
            try
            { var addSheetRequest = new AddSheetRequest();
                addSheetRequest.Properties = new SheetProperties();
                addSheetRequest.Properties.Title = sheetName;
                BatchUpdateSpreadsheetRequest batchUpdateSpreadsheetRequest = new BatchUpdateSpreadsheetRequest();
                batchUpdateSpreadsheetRequest.Requests = new List<Request>();
                batchUpdateSpreadsheetRequest.Requests.Add(new Request
                {
                    AddSheet = addSheetRequest
                });
                _client.BatchUpdate(id_table, batchUpdateSpreadsheetRequest);
                var temp = list.ElementAt(list.Count()-1).collum;
                var range = $"{sheetName}!A1:{temp}1";
                var valueRange = new ValueRange();
                    var oblist = new List<object>();
                    for (int i = 1; i <= GetColumnNumber(temp);i++)
                    {
                        var filterresult = list.Where(x => x.collum == GetExcelColumnName(i));
                        if (filterresult.Count() > 0)
                        {
                            oblist.Add(filterresult.ElementAt(0).Title);  
                            if (filterresult.Count() > 1) 
                                Console.WriteLine($"Error collum {GetExcelColumnName(i)} dublicate. Add one filterresult.ElementAt(0).Title");
                        }
                        else oblist.Add("");  
                    }

                   // oblist1 = new List<object>() { "Player", "Start Village name", "Start Village coord", "move unit", "Time to arrive", "Target name", "Target coord", "time start", "time until start", "type", "vawe", "comment" };


                    valueRange.Values = new List<IList<object>> { oblist };
                    while (!_client.TryUpdateValues(id_table, range, valueRange))
                    {
                        Console.WriteLine($" Error add:{range}%");
                        Console.WriteLine($" Exeption Goggle. Repeat after 100 sec");
                        _sleeper.Sleep(100000);
                    }
                
                return UpdateFormatCell(id_table,sheetName,GetColumnNumber(temp),"Title");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error Create sheet in table {id_table}");
                Console.WriteLine($"Error - {e.Message}");
                return false;
            }
        }

        public List<String> ReadDateToGoogleSheets(string id_table, string sheetName)
        {
            
            var target = new List<String>();
            try
            {
                var nextEmptyRow = GetNextEmptyRow(sheetName,id_table);
                var dataRange = $"{sheetName}!A2:E{nextEmptyRow-1}";
                ValueRange response = _client.GetValues(id_table, dataRange);
                IList<IList<Object>> values = response.Values;
                if (values != null && values.Count > 0)
                {
                    foreach (var row in values)
                    {
                        target.Add(row[0].ToString());
                    }
                }
                else
                {
                    Console.WriteLine("No data found.");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Couldn't read the sheet {sheetName} in the table");
                throw;
            }
            return target;
        }
        
       
        public bool UpdateFormatCell(string id_table, string sheetName, int collum, string typeform )
        { 
            try
            { 
                Spreadsheet ss = _client.GetSpreadsheet(id_table);
                Sheet sh = ss.Sheets.Where(s => s.Properties.Title == sheetName).FirstOrDefault();
                int sheetId = (int)sh.Properties.SheetId;
                var rang = new GridRange()
                {
                    SheetId = sheetId,
                    StartRowIndex = 0,
                    StartColumnIndex = 0,
                    EndRowIndex = GetNextEmptyRow(sheetName, id_table),
                    EndColumnIndex = collum
                };
                
                BatchUpdateSpreadsheetRequest bussr = new BatchUpdateSpreadsheetRequest();

                var userEnteredFormat = new CellFormat();

                if (typeform == "time")
                {
                    userEnteredFormat = new CellFormat()
                    {
                        NumberFormat = new NumberFormat()
                        {
                            Type = "DATE",
                            Pattern = "hh:mm:ss"
                        },
                    };
                }
                else
                {
                    userEnteredFormat = new CellFormat()
                    {
                        TextFormat = new TextFormat()
                        {
                            FontSize = 16
                        },
                        WrapStrategy = "WRAP"

                    };
                }

//create the update request for cells from the first row
                var updateCellsRequest = new Request()
                {
                    RepeatCell = new RepeatCellRequest()
                    {   Range = rang,
                        Cell = new CellData()
                        {
                            UserEnteredFormat = userEnteredFormat
                        },
                        Fields = "UserEnteredFormat"
                    }
                };

                var UpdateDimensionRequest = new Request()
                {
                    UpdateDimensionProperties =  new UpdateDimensionPropertiesRequest()
                    {
                        Range = new DimensionRange()
                        {
                            SheetId = sheetId,
                            Dimension = "COLUMNS",
                            StartIndex = 0,
                            EndIndex = collum
                        },  
                        Properties = new DimensionProperties
                        {
                            PixelSize = 230
                        },
                        Fields = "pixelSize"
                    }
                };
                
                var AutoResizenRequest = new Request()
                {
                    AutoResizeDimensions =  new AutoResizeDimensionsRequest()
                    {
                        Dimensions = new DimensionRange()
                        {
                            SheetId = sheetId,
                            Dimension = "ROWS",
                            StartIndex = 0,
                            EndIndex = 1
                        }
                    }
                };
                
                
                bussr.Requests = new List<Request>();
                bussr.Requests.Add(updateCellsRequest);
                bussr.Requests.Add(UpdateDimensionRequest);
                bussr.Requests.Add(AutoResizenRequest);
                _client.BatchUpdate(id_table, bussr);
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error Create sheet in table {id_table}");
                return false;
            }
        }

        public void WriteDateToGoogleSheetsList(string id_table, string sheetName, List<string> list, string collum)
        { 
            try
            {
                Console.WriteLine($" Write data in {sheetName}");
                if (list != null && list.Count() > 0)
                {
                    int i = 2;
                    var sum_scan = new List<String>();
                    foreach (var scan in list)
                    {
                        sum_scan.Add("test");
                    }

                    int progress_c = sum_scan.Count();
                    decimal progress_t = 0;
                    int startindex = i;
                    int k = 0;
                    var values = new List<IList<object>>();


                    foreach (var elem  in sum_scan)
                    {
                        var valueRange = new ValueRange();
                        
                        var oblist = new List<object>()
                            { "test" };
                        values.Add(oblist);
                        if ((startindex > i - 30)||k>=list.Count()-1)
                        {
                             var range = $"{sheetName}!A{startindex}:T{i}";
                             valueRange.Values = values;
                             while (!_client.TryUpdateValues(id_table, range, valueRange))
                             {
                                 Console.WriteLine($" Error add:{range}%");
                                 Console.WriteLine($" Exeption Goggle. Repeat after 120 sec");
                                 _sleeper.Sleep(120000);
                             }
                             if (progress_t != (Math.Round(((decimal)i / progress_c) * 100)))
                             {
                                 Console.WriteLine($"Progress:{progress_t}%");
                                 progress_t = Math.Round(((decimal)i / progress_c) * 100);
                             }
                             startindex = i+1;
                             values.Clear();
                        }
                        i++;
                        k++;
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error writing to sheet {sheetName} in table");
                throw;
            }
        }
        
        public void WriteDateToGoogleSheets(string id_table, string sheetName, string value, string rang)
        { 
            try
            {
                    var values = new List<IList<object>>();
                    var valueRange = new ValueRange();
                    var oblist = new List<object>() { value };
                    values.Add(oblist);
                    var range = $"{sheetName}!{rang}";
                    valueRange.Values = values;
                    while (!_client.TryUpdateValues(id_table, range, valueRange))
                    {
                        Console.WriteLine($" Error add:{range}%");
                        Console.WriteLine($" Exeption Goggle. Repeat after 120 sec");
                        _sleeper.Sleep(120000);
                    }
                    
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error writing to sheet {sheetName} in table");
                throw;
            }
        }
        
        public void WriteTaskToGoogleSheets(string id_table, string sheetName, string value_key, double value_total, string status, int col, int row)
        { 
            try
            {
                var rang = toRange(col,col+2,row,row); //$"{GetExcelColumnName(col)}{row}:{GetExcelColumnName(col+1)}{row}";
                var values = new List<IList<object>>();
                var valueRange = new ValueRange();
                var oblist = new List<object>() { value_key, value_total, status};
                values.Add(oblist);
                var range = $"{sheetName}!{rang}";
                valueRange.Values = values;
                while (!_client.TryUpdateValues(id_table, range, valueRange))
                {
                    Console.WriteLine($" Error add:{range}%");
                    Console.WriteLine($" Exeption Goggle. Repeat after 120 sec");
                    _sleeper.Sleep(120000);
                }
                    
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error writing to sheet {sheetName} in table");
                throw;
            }
        }

        private string GetExcelColumnName(int columnNumber)
        {
            string columnName = "";

            while (columnNumber > 0)
            {
                int modulo = (columnNumber - 1) % 26;
                columnName = Convert.ToChar('A' + modulo) + columnName;
                columnNumber = (columnNumber - modulo) / 26;
            } 

            return columnName;
        }
        
        public static int GetColumnNumber(string name)
        {
            int number = 0;
            int pow = 1;
            for (int i = name.Length - 1; i >= 0; i--)
            {
                number += (name[i] - 'A' + 1) * pow;
                pow *= 26;
            }

            return number;
        }

        public string GetEndRange(string sheetName, string id_table, int row)
        {
            var range = $"{sheetName}!{row}:{row}";
            try
            {
                var response = _client.GetValues(id_table, range, SpreadsheetsResource.ValuesResource.GetRequest.MajorDimensionEnum.COLUMNS);
                var values = response.Values;

                if (values == null || values.Count == 0)
                {
                    // Если столбец пуст, вернуть первую строку
                    return $"A{row}";
                }

                // Найти первую пустую строку
                for (int i = 1; i < values.Count; i++)
                {
                    var cellValue = values[i][0]?.ToString();
                    if (string.IsNullOrEmpty(cellValue))
                    {
                        // Найдена пустая строка, вернуть номер этой строки
                        return $"{GetExcelColumnName(i + 1)}{row}";
                    }
                }

                // Если все строки заполнены, вернуть номер следующей строки
                return $"{GetExcelColumnName(values.Count)}";
            }
            catch (Exception ex)
            {
                // Обработка ошибок, например, вывод в консоль или логирование
                Console.WriteLine($"Error getting values: {ex.Message}");
                throw;
            }
        }

        public int GetNextEmptyRow(string sheetName, string id_table)
        {
            var range = $"{sheetName}!A1:A";

            try
            {
                var response = _client.GetValues(id_table, range);
                var values = response.Values;
                if (values == null || values.Count == 0)
                {
                    // Если столбец пуст, вернуть первую строку
                    return 1;
                }
                // Если все строки заполнены, вернуть номер следующей строки
                return values.Count+1;
            }
            catch (Exception ex)
            {
                // Обработка ошибок, например, вывод в консоль или логирование
                Console.WriteLine($"Error getting values: {ex.Message}");
                throw;
            }
        }
    }
}
