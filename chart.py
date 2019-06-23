import matplotlib.pyplot as plt

date=["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
hour=[8, 10, 9, 11]

fig1, ax1 = plt.subplots()
ax1.plot(date, hour)
plt.show() # need to explicitly "show" the chart window



breakpoint()

#sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90

#labels = ["Product A", "Product B", "Product C", "Product D"]
#sizes = [15, 30, 45, 10]


import plotly
import plotly.graph_objs as go

## Question: Why is it working only in Python command line?


plotly.offline.plot({
    "data": [go.Scatter(x=date, y=hour)],
    "layout": go.Layout(title="Daily Working Hour")
}, auto_open=True)

go.show()






#line_data = [
#    {"date": "2019-01-01", "stock_price_usd": 100.00},
#    {"date": "2019-01-02", "stock_price_usd": 101.01},
#    {"date": "2019-01-03", "stock_price_usd": 120.20},
#    {"date": "2019-01-04", "stock_price_usd": 107.07},
#    {"date": "2019-01-05", "stock_price_usd": 142.42},
#    {"date": "2019-01-06", "stock_price_usd": 135.35},
#    {"date": "2019-01-07", "stock_price_usd": 160.60},
#    {"date": "2019-01-08", "stock_price_usd": 162.62},
#]
#
#breakpoint()
#
#
#def transform_response():
#    rows = []
#    for row in line_data.items():
#        row = {
#            "date": a,
#            "price": float(b)
#        }
#        rows.append(row)
#    return rows
#
#rows = transform_response(line_data)
#
#
#
#
#
#plotly.offline.plot({
#    "data": [go.Scatter(x=line_data["date"], y=[4, 3, 2, 1])],
#    "layout": go.Layout(title="hello world")
#}, auto_open=True)
#
#
#print("----------------")
#print("GENERATING LINE GRAPH...")
#print(line_data)

