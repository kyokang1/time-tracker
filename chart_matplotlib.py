import matplotlib.pyplot as plt

from app.time_tracker import get_records

sheet, rows = get_records()

# Get values from column "date"
col_date = sheet.col_values(1)
del col_date[col_date.index("date")] #Delete column heading

# Get values from column "hour"
col_hour = sheet.col_values(2)
del col_hour[col_hour.index("hour")] #Delete column heading

date=col_date
hour=col_hour

fig1, ax1 = plt.subplots()
ax1.plot(date, hour)
fig1.suptitle('Work Hour')
plt.show() # need to explicitly "show" the chart window

#date=["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
#hour=[8, 10, 9, 11]

## TODO: 
# 1) Scale the chart
# 2) Implement the chart to the browser


#breakpoint()
#
##sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90
#
##labels = ["Product A", "Product B", "Product C", "Product D"]
##sizes = [15, 30, 45, 10]
#
