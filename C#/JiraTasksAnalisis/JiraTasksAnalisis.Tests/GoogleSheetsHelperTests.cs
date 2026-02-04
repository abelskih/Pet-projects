using System.Collections.Generic;
using System.Linq;
using Google.Apis.Sheets.v4.Data;
using GoogleSheets;
using JiraTasksAnalisis;
using NUnit.Framework;

namespace JiraTasksAnalisis.Tests
{
    [TestFixture]
    public class GoogleSheetsHelperTests
    {
        [Test]
        public void CheckSheetInTable_ReturnsTrue_WhenSheetExists()
        {
            var client = new FakeGoogleSheetsClient
            {
                Spreadsheet = new Spreadsheet
                {
                    Sheets = new List<Sheet>
                    {
                        new Sheet { Properties = new SheetProperties { Title = "Team1" } }
                    }
                }
            };

            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            var result = helper.CheckSheetInTable("sheet-id", "Team1");

            Assert.That(result, Is.True);
        }

        [Test]
        public void GetNextEmptyRow_Returns1_WhenColumnIsEmpty()
        {
            var client = new FakeGoogleSheetsClient();
            client.ValuesByRange["Sheet1!A1:A"] = new ValueRange { Values = new List<IList<object>>() };

            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            var result = helper.GetNextEmptyRow("Sheet1", "sheet-id");

            Assert.That(result, Is.EqualTo(1));
        }

        [Test]
        public void GetNextEmptyRow_ReturnsCountPlusOne_WhenColumnHasValues()
        {
            var client = new FakeGoogleSheetsClient();
            client.ValuesByRange["Sheet1!A1:A"] = new ValueRange
            {
                Values = new List<IList<object>>
                {
                    new List<object> { "A1" },
                    new List<object> { "A2" },
                    new List<object> { "A3" }
                }
            };

            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            var result = helper.GetNextEmptyRow("Sheet1", "sheet-id");

            Assert.That(result, Is.EqualTo(4));
        }

        [Test]
        public void CreateSheetInTable_WritesHeaderRow()
        {
            var client = new FakeGoogleSheetsClient();
            client.Spreadsheet = new Spreadsheet
            {
                Sheets = new List<Sheet>
                {
                    new Sheet { Properties = new SheetProperties { Title = "Team1", SheetId = 1 } }
                }
            };

            var helper = new GoogleSheetsHelper(client, new FakeSleeper());
            var titles = new List<TitlesCollum>
            {
                new TitlesCollum { Title = "Date", collum = "A" },
                new TitlesCollum { Title = "Done", collum = "B" }
            }.OrderBy(x => x.collum);

            var result = helper.CreateSheetInTable("sheet-id", "Team1", titles);

            Assert.That(result, Is.True);
            Assert.That(client.BatchUpdates.Count, Is.EqualTo(2));
            Assert.That(client.Updates.Count, Is.EqualTo(1));
            Assert.That(client.Updates[0].Range, Is.EqualTo("Team1!A1:B1"));
        }

        [Test]
        public void WriteDateToGoogleSheets_WritesSingleCell()
        {
            var client = new FakeGoogleSheetsClient();
            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            helper.WriteDateToGoogleSheets("sheet-id", "Team1", "5", "C3");

            Assert.That(client.Updates.Count, Is.EqualTo(1));
            Assert.That(client.Updates[0].Range, Is.EqualTo("Team1!C3"));
            Assert.That(client.Updates[0].ValueRange.Values[0][0], Is.EqualTo("5"));
        }

        [Test]
        public void GetEndRange_ReturnsFirstCell_WhenColumnIsEmpty()
        {
            var client = new FakeGoogleSheetsClient();
            client.ValuesByRange["Team1!5:5"] = new ValueRange { Values = new List<IList<object>>() };
            var helper = new GoogleSheetsHelper(client);

            var result = helper.GetEndRange("Team1", "sheet-id", 5);

            Assert.That(result, Is.EqualTo("A5"));
        }

        [Test]
        public void GetEndRange_ReturnsFirstEmptyColumn()
        {
            var client = new FakeGoogleSheetsClient();
            client.ValuesByRange["Team1!5:5"] = new ValueRange
            {
                Values = new List<IList<object>>
                {
                    new List<object> { "A5" },
                    new List<object> { "B5" },
                    new List<object> { "" }
                }
            };
            var helper = new GoogleSheetsHelper(client);

            var result = helper.GetEndRange("Team1", "sheet-id", 5);

            Assert.That(result, Is.EqualTo("C5"));
        }

        [Test]
        public void WriteTaskToGoogleSheets_WritesRangeWithThreeColumns()
        {
            var client = new FakeGoogleSheetsClient();
            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            helper.WriteTaskToGoogleSheets("sheet-id", "Team1", "KEY-1", 2.5, "Done", 2, 7);

            Assert.That(client.Updates.Count, Is.EqualTo(1));
            Assert.That(client.Updates[0].Range, Is.EqualTo("Team1!B7:D7"));
            var row = client.Updates[0].ValueRange.Values[0];
            Assert.That(row[0], Is.EqualTo("KEY-1"));
            Assert.That(row[1], Is.EqualTo(2.5));
            Assert.That(row[2], Is.EqualTo("Done"));
        }

        [Test]
        public void WriteDateToGoogleSheets_Retries_WhenClientReturnsFalse()
        {
            var client = new FakeGoogleSheetsClient
            {
                FailUpdatesBeforeSuccess = 2
            };
            var helper = new GoogleSheetsHelper(client, new FakeSleeper());

            helper.WriteDateToGoogleSheets("sheet-id", "Team1", "5", "C3");

            Assert.That(client.Updates.Count, Is.EqualTo(3));
        }
    }
}
