#time_tracker_test.py

import os

from app.time_tracker import get_records, day_of_week, dow_week, list_total, total_hour_ytd, avg_hour_ytd

def test_get_records():
    sheet, rows = get_records()
    dates = [row["date"] for row in rows]
    assert str(dates[0]) == str("2009-09-14")

def test_day_of_week():
    assert day_of_week("2019-07-01") == "Mon"
    assert day_of_week("2019-07-05") == "Fri"
    assert day_of_week("2019-07-07") == "Sun"

def test_dow_week():
    assert dow_week(day_of_week("2019-07-01")) == True
    assert dow_week(day_of_week("2019-07-05")) == True
    assert dow_week(day_of_week("2019-07-07")) == False

def test_list_total():
    test_list = [1,2,3,4,5,6,7,8,9,10]
    assert list_total(test_list) == 55

def test_total_hour_ytd():
    assert total_hour_ytd(2010) == 2233
    assert total_hour_ytd(2016) == 2265.5
    assert total_hour_ytd(2018) == 2145.5

def test_avg_hour_ytd():
    assert avg_hour_ytd(2009) == 9.2
    assert avg_hour_ytd(2014) == 8.5
    assert avg_hour_ytd(2017) == 9.6

# DEVELOPER's NOTE:
# Validation on the work hour and date is not required since the inputs are secured in html.
# For example, input of date is secured as date since html defines the input box of "date".
# And working hour is secured as the type of "number" and minimum/maximum values are defined.
# For detail, see the source code of "start.html"

