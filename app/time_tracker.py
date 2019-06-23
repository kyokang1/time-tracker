
import json
import os

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
    'https://www.googleapis.com/auth/drive'
    ]

def get_records():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, scope)
    client = gspread.authorize(credentials)
    sheet = client.open("timetracker").sheet1
    rows = sheet.get_all_records()
    return sheet, rows

if __name__ == "__main__":
    sheet, rows = get_records()
    
    for row in rows:
        print(row)
    

#def get_records():



#def add_row():
#    return sheet.insert_row(["2019-06-11", "13"])

#add_row()

#def update_row()
    

#def get_records():
#    rows = sheet.get_all_values() #> <class 'list'>
#    return sheet, rows

#print(list(get_records()))

#def create_records():
#
#    product = {
#        "date": next_id,
#        "hour": product_attributes["name"],
#    }
#    next_row = list(product.values()) #> [13, 'Product CLI', 'snacks', 4.99, '2019-01-01']
#    next_row_number = len(products) + 2 # number of records, plus a header row, plus one
#    response = sheet.insert_row(next_row, next_row_number)
#    return response


# Extract and print all of the values





#list_of_hashes = sheet.get_all_values()
#list_of_hashes = sheet.row_values(1)
#list_of_hashes = sheet.col_values(1)
#list_of_hashes = sheet.cell(1, 1).value

#print(list_of_hashes)



#doc = client.open_by_key(DOCUMENT_KEY) #> <class 'gspread.models.Spreadsheet'>
#sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
#rows = sheet.get_all_records() #> <class 'list'>




