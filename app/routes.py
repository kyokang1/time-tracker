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
        print(row_attributes)
        response = create_records(row_attributes["date"],row_attributes["hour"])
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
    return render_template("results.html")



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











