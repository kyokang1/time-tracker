#
# Module & Package Import
#
from flask import Flask, Blueprint, request, render_template, jsonify, flash, redirect, url_for
import datetime
import os

from app.time_tracker import *

main_routes = Blueprint("main_routes", __name__)

#
# START /
#
@main_routes.route("/")
def index():
    print("VISITING THE START PAGE")
    return render_template("start.html")

#
# CREAT /
#
@main_routes.route('/create', methods=["POST"])
def create():
    print("CREATING A NEW ROW...")
    print("FORM DATA:", dict(request.form))
    try:
        row_attributes = {
            "date": request.form["input_date"],
            "hour": request.form["input_hour"]
        }
        row_dow = day_of_week(row_attributes["date"])
        row_yyyy, row_mm, row_dd = (row_attributes["date"].split('-'))
        response = create_records(row_attributes["date"],row_attributes["hour"], row_dow, row_yyyy, row_mm)
        return redirect("/results")
    except Exception as err:
        print("ERROR:", type(err), err.name)
#        flash(f"ERROR: {err.name}. Please try again.", "danger") # use the "danger" category to correspond with twitter bootstrap alert colors
        return redirect("/results")

#
# RESULTS /
#
@main_routes.route("/results", methods=["GET", "POST"])
def results():
    print("VISITING THE MONTHLY RESULT PAGE")
    
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   
    
    avg_hr_ytd = avg_hour_ytd(c_year)
    avg_hr_mtd = avg_hour_mtd(c_year, c_month)

    total_hr_ytd = total_hour_ytd(c_year)
    total_hr_mtd = total_hour_mtd(c_year, c_month)

    eval_ytd = evaluate_hour(avg_hr_ytd)
    eval_mtd = evaluate_hour(avg_hr_mtd)

    # Run the chart on plotly online studio
    chart_mtd_avg()
    chart_mtd_total()
    chart_ytd_avg()
    chart_ytd_total()

    return render_template("results.html",
        c_year = c_year,
        c_month = c_month,
        ytd_avg_hour = avg_hr_ytd,
        ytd_hour = total_hr_ytd,
        ytd_eval = eval_ytd,
        mtd_avg_hour = avg_hr_mtd,
        mtd_hour = total_hr_mtd,
        mtd_eval = eval_mtd,
    )
