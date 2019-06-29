from flask import Blueprint, request, render_template, jsonify, flash, redirect
import datetime

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
@main_routes.route("/results")
def results():
    print("VISITING THE RESULTS PAGE")
    
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month   
    
    result_avg_hr_ytd = round(avg_hour_ytd(c_year),1)
    result_avg_hr_mtd = round(avg_hour_mtd(c_year, c_month),1)

    return render_template("results.html",
        results_ytd = result_avg_hr_ytd,
        results_mtd = result_avg_hr_mtd
    )


#    sheet, rows = get_records()
#
#    # Get values from column "date"
#    col_date = sheet.col_values(1)
#    del col_date[col_date.index("date")] #Delete column heading
#
#    # Get values from column "hour"
#    col_hour = sheet.col_values(2)
#    del col_hour[col_hour.index("hour")] #Delete column heading


## TODO: Show Scatter Chart


#
#@main_routes.route("/create", methods=["GET", "POST"])
#def results():
#    print("VISITING THE RESULTS PAGE")
#    print("REQUEST PARAMS:", dict(request.args))
#    print("REQUEST VALUES:", dict(request.values))
#    
#    print(request.args)
#    print(request.values)
#
#    user_date = request.args["date"]
#    user_hour = request.args["hour"]











