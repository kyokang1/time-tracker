
import json
import os
#from datetime import datetime
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

def create_records(a, b, c, d, e):
    sheet, rows = get_records()
    dates = [row["date"] for row in rows]
    if a in dates:
        cell = sheet.find(a)
        response = sheet.update_cell(cell.row, cell.col+1, float(b))
        response = sheet.update_cell(cell.row, cell.col+2, c)
    else:
        response = sheet.append_row([a, float(b), c, int(d), int(e)])
    return response

def day_of_week(d):
    yyyy, mm, dd = (int(d) for d in d.split('-'))
    dow_no = datetime.date(yyyy, mm, dd).weekday()
    if dow_no == 0:
        dow = "Mon"
    elif dow_no == 1:
        dow = "Tue"
    elif dow_no == 2:
        dow = "Wed"
    elif dow_no == 3:
        dow = "Thu"
    elif dow_no == 4:
        dow = "Fri"
    elif dow_no == 5:
        dow = "Sat"
    elif dow_no == 6:
        dow = "Sun"
    return dow

def avg_hour(a, b):
    return a/b

def dow_week (a):
    if a in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        return True
    else:
        return False

def list_total(rows):
    sum = 0
    for r in rows:
        sum = sum + r
    return sum

def evaluate_hour(hr):
    if hr <= 8:
        evaluation = "Safe"
    elif hr > 8 and hr <= 9:
        evaluation = "Watch"
    elif hr > 9 and hr <= 10:
        evaluation = "Warning"
    else:
        evaluation = "Danger"
    return evaluation

if __name__ == "__main__":
    sheet, rows = get_records()

#    print(list(rows))
    
    #Define month_id
#    c_year = datetime.now().year
#    c_month = datetime.now().month
#    month_id = str(c_year) + str("_") + str(c_month)
    print(c_year)

#    
#    #r = rows["date"]
##    print(type(rows))
##    print(rows)##
#    #Calculate - total hour
#    c_year = 2018
#    c_month = 5
#    rows_year = [r for r in rows if str(r["yyyy"]) == str(c_year)]
#    rows_month = [r for r in rows_year if str(r["mm"]) == str(c_month)]#
#    rows_year_hr = [r["hour"] for r in rows_year]
#    rows_month_hr = [r["hour"] for r in rows_month]#
#    total_hr_ytd = list_total(rows_year_hr)
#    total_hr_mtd = list_total(rows_month_hr)#
#    #Calculate - count of weekdays
##    rows_year_w = [r for r in rows_year if r["dayofweek"] not in ["Mon", "Tue", "Wed", "Thu", "Fri"]]
#    rows_year_w = [r for r in rows_year if dow_week(r["dayofweek"]) == True]
#    rows_month_w = [r for r in rows_month if dow_week(r["dayofweek"]) == True]
##    rows_month = [r for r in rows_year if str(r["mm"]) == str(c_month)]
#    print(rows_year_w)
##    print(rows_month_w)



    


#    print(rows_year)

#    c_month_hour = 
#    print(c_rows)




#   breakpoint()







## TODO (as of Jun/22/2019): (DONE)
## 1) Insert a new row in the bottom (DONE)
## 2) Date should be in date format (DONE)
## 3) If the input date already existing, update the existing row (DONE)
## 4) Validate input (Pass, input box is "number")


## TODO - Calculation (as of Jun/28/2019)
## 1) create yyyy, mm, dd when parsing inputs
## 2) calculate by yyyy, and mm



