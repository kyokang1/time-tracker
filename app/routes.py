from flask import Blueprint, request, render_template, jsonify, flash, redirect

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
        #print(row_attributes)
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
    
    sheet, rows = get_records()

    # Get values from column "date"
    col_date = sheet.col_values(1)
    del col_date[col_date.index("date")] #Delete column heading

    # Get values from column "hour"
    col_hour = sheet.col_values(2)
    del col_hour[col_hour.index("hour")] #Delete column heading

    c_year = 2018
    c_month = 5

    #Calculate - average hour_ytd
    rows_year = [r for r in rows if str(r["yyyy"]) == str(c_year)]
    rows_year_hr = [r["hour"] for r in rows_year]
    total_hr_ytd = list_total(rows_year_hr)   
    rows_year_w = [r for r in rows_year if dow_week(r["dayofweek"]) == True]
    count_hr_ytd = len(rows_year_w)
    avg_hr_ytd = total_hr_ytd/count_hr_ytd
    
    #Calculate - average hour_mtd
    rows_year = [r for r in rows if str(r["yyyy"]) == str(c_year)]
    rows_month = [r for r in rows_year if str(r["mm"]) == str(c_month)]
    rows_month_hr = [r["hour"] for r in rows_month]
    total_hr_mtd = list_total(rows_month_hr)   
    rows_month_w = [r for r in rows_month if dow_week(r["dayofweek"]) == True]
    count_hr_mtd = len(rows_month_w)
    avg_hr_mtd = total_hr_mtd/count_hr_mtd

#    print(avg_hr_ytd)
#    print(avg_hr_mtd)


    return render_template("results.html",
        results_ytd = avg_hr_ytd,
        results_mtd = avg_hr_mtd
    )

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











