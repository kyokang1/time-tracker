from flask import Blueprint, request, render_template

from app.time_tracker import *

main_routes = Blueprint("main_routes", __name__)

#
# GET /
#

@main_routes.route("/")
def index():
    print("VISITING THE START PAGE")
    return render_template("start.html")

#
# GET /results
# GET /results?choice=rock
# POST /results
#




