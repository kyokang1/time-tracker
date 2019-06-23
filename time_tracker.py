
import json
import os

#from dotenv import load_dotenv
import gspread

#from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

#load_dotenv()

#DOCUMENT_KEY = os.environ.get("GOOGLE_SHEET_ID", "OOPS Please get the spreadsheet identifier from its URL")
#SHEET_NAME = "tracker"

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("google_api_credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("timetracker").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)




#doc = client.open_by_key(DOCUMENT_KEY) #> <class 'gspread.models.Spreadsheet'>
#sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
#rows = sheet.get_all_records() #> <class 'list'>




