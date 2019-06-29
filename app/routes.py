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

    #Define month_id
    c_year = datetime.now().year
    c_month = datetime.now().month
    month_id = str(c_year) + str("_") + str(c_month)
    
    #Monthly result
    


    #YTD result



    # Get values from column "date"
    col_date = sheet.col_values(1)
    del col_date[col_date.index("date")] #Delete column heading

    # Get values from column "hour"
    col_hour = sheet.col_values(2)
    del col_hour[col_hour.index("hour")] #Delete column heading

    #date=col_date
    #hour=col_hour
    #
    #fig1, ax1 = plt.subplots()
    #ax1.plot(date, hour)
    #fig1.suptitle('Work Hour')
    #plt.show()

    return render_template("results.html",
        results_date = col_date,
        results_hour = col_hour
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











