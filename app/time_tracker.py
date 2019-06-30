
##
## Module & Package Import
##

import json
import os
import datetime
import statistics

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from flask import Flask, Blueprint, request, render_template, jsonify, flash, redirect

from dotenv import load_dotenv
import gspread

from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials


##
## Credential & API Setup
##

load_dotenv()

# Google spreadsheet credentials setup
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

# plotly credential setup
PLOTLY_USER_NAME = os.environ.get("plotly_user_name")
PLOTLY_API_KEY = os.environ.get("plotly_api_key")

plotly.tools.set_credentials_file(username=PLOTLY_USER_NAME, api_key=PLOTLY_API_KEY)


##
## Define Functions
##

# google spreadsheet actions
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

# formula to be used for calculation
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

def dow_week (a):
    if a in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        return True
    else:
        return False

def list_total(rows):
    sum = 0
    for r in rows:
        sum = sum + float(r)
    return sum

#def month_id():
#    c_year = datetime.datetime.now().year
#    c_month = datetime.datetime.now().month
#    month_id = str(c_year) + str("_") + str(c_month)
#    return month_id

# Calculate - average/total work hour - YTD
def total_hour_ytd(i_year):
    sheet, rows = get_records()
    rows_year = [r for r in rows if int(r["yyyy"]) == int(i_year)]
    rows_year_hr = [r["hour"] for r in rows_year]
    total_hr_ytd = round(list_total(rows_year_hr),1)
    return total_hr_ytd

def avg_hour_ytd(i_year):
    sheet, rows = get_records()
    rows_year = [r for r in rows if int(r["yyyy"]) == int(i_year)]
    rows_year_hr = [r["hour"] for r in rows_year]
    total_hr_ytd = list_total(rows_year_hr)   
    rows_year_w = [r for r in rows_year if dow_week(r["dayofweek"]) == True and r["hour"] != 0]
    count_hr_ytd = len(rows_year_w)
    avg_hr_ytd = round(total_hr_ytd/count_hr_ytd,1)
    return avg_hr_ytd
    
# Calculate - average/total work hour - MTD
def total_hour_mtd(i_year, i_month):
    sheet, rows = get_records()
    rows_year = [r for r in rows if int(r["yyyy"]) == int(i_year)]
    rows_month = [r for r in rows_year if int(r["mm"]) == int(i_month)]
    rows_month_hr = [r["hour"] for r in rows_month]
    total_hr_mtd = round(list_total(rows_month_hr),1)
    return total_hr_mtd

def avg_hour_mtd(i_year, i_month):
    sheet, rows = get_records()
    rows_year = [r for r in rows if int(r["yyyy"]) == int(i_year)]
    rows_month = [r for r in rows_year if int(r["mm"]) == int(i_month)]
    rows_month_hr = [r["hour"] for r in rows_month]
    total_hr_mtd = list_total(rows_month_hr)   
    rows_month_w = [r for r in rows_month if dow_week(r["dayofweek"]) == True and r["hour"] != 0]
    count_hr_mtd = len(rows_month_w)
    avg_hr_mtd = round(total_hr_mtd/count_hr_mtd,1)
    return avg_hr_mtd

# Work-Life balance status evaluation
def evaluate_hour(hr):
    threshold_watch = 8     #> user setup
    threshold_warning = 9     #> user setup
    threshold_danger = 10     #> user setup

    if hr <= float(threshold_watch):
        evaluation = "SAFE"
    elif hr > float(threshold_watch) and hr <= float(threshold_warning):
        evaluation = "WATCH"
    elif hr > float(threshold_warning) and hr <= float(threshold_danger):
        evaluation = "WARNING"
    else:
        evaluation = "DANGER"
    return evaluation

# Create plotly chart - ytd avg
def chart_ytd_avg():
    sheet, rows = get_records()

    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   

    start_year = 2009     #> user setup
    threshold_watch = 8     #> user setup
    threshold_warning = 9     #> user setup
    threshold_danger = 10     #> user setup

    year_span =[]
    year_inc = start_year
    while True:
        year_span.append(year_inc)
        if year_inc == c_year:
            break
        else:
            year_inc = year_inc +1

    avg_span = []
    for i in year_span:
        avg_hr_inc = avg_hour_ytd(i)
        avg_span.append(avg_hr_inc)

    colorlist =[]
    year_inc = start_year
    color_basic = 'rgba(204,204,204,1)'
    color_highlight = 'rgba(26, 118, 255, 1)'
    while True:
        if year_inc == c_year:
            colorlist.append(color_highlight)
            break
        else:
            colorlist.append(color_basic)
            year_inc = year_inc +1

    data = [go.Bar(
        x= year_span,
        y= avg_span,
        text= avg_span,
        textposition = 'outside',
        marker= dict(color=colorlist)
        )
    ]
    
    layout = {
        'title': {
            'text':'Yearly Average Work Hour',
            'xref': 'paper',
            'x': 0,
        },
        'xaxis': {
            'title': 'Year',
        },
        'yaxis': {
                'title': 'Daily Work Hour',
            'autorange': True,
        },
        'shapes': [
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': threshold_watch,
            'x1': int(c_year+1),
            'y1': threshold_watch,
            'line':{
                'color': 'green',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': threshold_warning,
            'x1': int(c_year+1),
            'y1': threshold_warning,
            'line':{
                'color': 'yellow',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': threshold_danger,
            'x1': int(c_year+1),
            'y1': threshold_danger,
            'line':{
                'color': 'red',
                'width': 4,
                'dash': 'dashdot'
                },
            }
        ]
    }

    fig = {
        'data': data,
        'layout': layout,
    }

    response = py.plot(fig, filename = 'chart_ytd_avg')
    return response

# Create plotly chart - mtd average
def chart_mtd_avg():
    sheet, rows = get_records()

    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   

    threshold_watch = 8     #> user setup
    threshold_warning = 9     #> user setup
    threshold_danger = 10     #> user setup

    month_span =[]
    month_inc = 1
    while True:
        month_span.append(month_inc)
        if month_inc == c_month:
            break
        else:
            month_inc = month_inc +1

    avg_span = []
    for i in month_span:
        avg_hr_inc = avg_hour_mtd(c_year, i)
        avg_span.append(avg_hr_inc)

    colorlist =[]
    month_inc = 1
    color_basic = 'rgba(204,204,204,1)'
    color_highlight = 'rgba(26, 118, 255, 1)'
    while True:
        if month_inc == c_month:
            colorlist.append(color_highlight)
            break
        else:
            colorlist.append(color_basic)
            month_inc = month_inc +1

    data = [go.Bar(
        x= month_span,
        y= avg_span,
        text= avg_span,
        textposition = 'outside',
        marker= dict(color=colorlist)
        )
    ]
    
    layout = {
        'title': {
            'text':str(c_year) + ' Monthly Average Work Hour',
            'xref': 'paper',
            'x': 0,
        },
        'xaxis': {
            'title': str(c_year) + ' Months',
        },
        'yaxis': {
                'title': 'Daily Work Hour',
            'autorange': True,
        },
        'shapes': [
            {
            'type': 'line',
            'x0': 0,
            'y0': threshold_watch,
            'x1': 12,
            'y1': threshold_watch,
            'line':{
                'color': 'green',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': 0,
            'y0': threshold_warning,
            'x1': 12,
            'y1': threshold_warning,
            'line':{
                'color': 'yellow',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': 0,
            'y0': threshold_danger,
            'x1': 12,
            'y1': threshold_danger,
            'line':{
                'color': 'red',
                'width': 4,
                'dash': 'dashdot'
                },
            }
        ]
    }

    fig = {
        'data': data,
        'layout': layout,
    }

    response = py.plot(fig, filename = 'chart_mtd_avg')
    return response

# Create plotly chart - ytd total
def chart_ytd_total():
    sheet, rows = get_records()

    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   

    start_year = 2009     #> user setup
    threshold_watch = 8     #> user setup
    threshold_warning = 9     #> user setup
    threshold_danger = 10     #> user setup

    ytd_tot_benchmark1 = 1356  #> user setup: Good example - Germany 2017 (Source: OECD Statistics)
    ytd_tot_benchmark2 = 1780  #> user setup: Mid example - US 2017 (Source: OECD Statistics)
    ytd_tot_benchmark3 = 2024  #> user setup: Bad example - S.Korea 2017 (Source: OECD Statistics)

    year_span =[]
    year_inc = start_year
    while True:
        year_span.append(year_inc)
        if year_inc == c_year:
            break
        else:
            year_inc = year_inc +1

    tot_span = []
    for i in year_span:
        tot_hr_inc = total_hour_ytd(i)
        tot_span.append(tot_hr_inc)

    colorlist =[]
    year_inc = start_year
    color_basic = 'rgba(204,204,204,1)'
    color_highlight = 'rgba(26, 118, 255, 1)'
    while True:
        if year_inc == c_year:
            colorlist.append(color_highlight)
            break
        else:
            colorlist.append(color_basic)
            year_inc = year_inc +1

    data = [go.Bar(
        x= year_span,
        y= tot_span,
        text= tot_span,
        textposition = 'outside',
        marker= dict(color=colorlist)
        )
    ]
    
    layout = {
        'title': {
            'text':'Yearly Total Work Hour',
            'xref': 'paper',
            'x': 0,
        },
        'xaxis': {
            'title': 'Year',
        },
        'yaxis': {
                'title': 'Total Work Hour',
            'autorange': True,
        },
        'shapes': [
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': ytd_tot_benchmark1,
            'x1': int(c_year+1),
            'y1': ytd_tot_benchmark1,
            'line':{
                'color': 'green',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': ytd_tot_benchmark2,
            'x1': int(c_year+1),
            'y1': ytd_tot_benchmark2,
            'line':{
                'color': 'yellow',
                'width': 4,
                'dash': 'dashdot'
                },
            },
            {
            'type': 'line',
            'x0': int(start_year-1),
            'y0': ytd_tot_benchmark3,
            'x1': int(c_year+1),
            'y1': ytd_tot_benchmark3,
            'line':{
                'color': 'red',
                'width': 4,
                'dash': 'dashdot'
                },
            }
        ]
    }

    fig = {
        'data': data,
        'layout': layout,
    }

    response = py.plot(fig, filename = 'chart_ytd_total')
    return response

# Create plotly chart - mtd total
def chart_mtd_total():
    sheet, rows = get_records()

    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   

    month_span =[]
    month_inc = 1
    while True:
        month_span.append(month_inc)
        if month_inc == c_month:
            break
        else:
            month_inc = month_inc +1

    tot_span = []
    for i in month_span:
        tot_hr_inc = total_hour_mtd(c_year, i)
        tot_span.append(tot_hr_inc)

    colorlist =[]
    month_inc = 1
    color_basic = 'rgba(204,204,204,1)'
    color_highlight = 'rgba(26, 118, 255, 1)'
    while True:
        if month_inc == c_month:
            colorlist.append(color_highlight)
            break
        else:
            colorlist.append(color_basic)
            month_inc = month_inc +1

    data = [go.Bar(
        x= month_span,
        y= tot_span,
        text= tot_span,
        textposition = 'outside',
        marker= dict(color=colorlist)
        )
    ]
    
    layout = {
        'title': {
            'text':str(c_year) + ' Monthly Total Work Hour',
            'xref': 'paper',
            'x': 0,
        },
        'xaxis': {
            'title': str(c_year) + ' Months',
        },
        'yaxis': {
                'title': 'Total Work Hour',
            'autorange': True,
        }
    }

    fig = {
        'data': data,
        'layout': layout,
    }

    response = py.plot(fig, filename = 'chart_mtd_total')
    return response


##
## Maim Script
##

if __name__ == "__main__":
    sheet, rows = get_records()
#    breakpoint()


## TODO (as of Jun/22/2019):
## 1) Insert a new row in the bottom (DONE)
## 2) Date should be in date format (DONE)
## 3) If the input date already existing, update the existing row (DONE)
## 4) Validate input (Pass, input box is "number")
## 5) Validate input of hour < 24 (Done by set the max value 24)

## TODO Calculation (as of Jun/28/2019)
## 1) create yyyy, mm, dd when parsing inputs (DONE)
## 2) calculate by yyyy, and mm (DONE)

## TODO (as of Jun/29/2019):
## 1) value display (DONE)
## 2) highlight the last column (DONE)
## 3) title & axis name (DONE)
## 4) 8 hour 9 hour 10 hour line (DONE)
## 5) Chart for MTD (DONE)
## 6) Chart for Total Hours (DONE)

## TODO (as of Jun/30/2019)
## 0) DEBUGGING the error not working with actual data (Done)
## 1) .env & .gitignore update & plotly API separation (Done)
## 2) README.md update
## 3) prepare for the presentation 
## 4) planning documentation
