
import json
import os
import datetime
import statistics

from dotenv import load_dotenv
import gspread

from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "google_api_credentials.json")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file", #> Per-file access to files created or opened by the app.
    'https://www.googleapis.com/auth/drive'  #> without this, it does not fetch the data
    ]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, scope)
client = gspread.authorize(credentials)
sheet = client.open("timetracker").sheet1

def get_records():
    rows = sheet.get_all_records()
    return sheet, rows

def create_records(a, b):
    response = sheet.insert_row([a, b])
    return response


if __name__ == "__main__":
    sheet, rows = get_records()
    
    #for row in rows:
    #    print(row)
    
    #a = '2010-01-31'

    

    #dates = [row["date"] for row in rows]

    #date_format = datetime.datetime.strptime(dates, "%Y-%m-%d")
    #print(datee.month)
    #print(dates)



    hours = [row["hour"] for row in rows]
    avg_hour = statistics.mean(hours)
    print(round(avg_hour,1))

    




    #date_input = input("Please input date: ")
    #hour_input = input("Please input hours: ")
    
    #create_records(date_input, float(hour_input))
    





## TODO (as of Jun/22/2019):
## 1) Insert a new row in the bottom
## 2) Date should be in date format
## 3) If the input date already existing, update the existing row

## TODO - Calculation (as of Jun/24/2019)
## 



