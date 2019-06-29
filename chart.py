import plotly
import plotly.plotly as py
import plotly.graph_objs as go
#import plotly.io as pio
#import plotly.offline as offline
#from plotly.offline import iplot, init_notebook_mode

import os
#import numpy as np

from app.time_tracker import *

#TODO: APIKey sent to environment
plotly.tools.set_credentials_file(username="kyokang1", api_key='DKCft9dRaKZMfuhb2zFY')

sheet, rows = get_records()

c_year = datetime.datetime.now().year
c_month = datetime.datetime.now().month   

year_span =[]
year_inc = 2009
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

data = [go.Bar(
    x= year_span,
    y= avg_span
)]

fig = {
    'data': data,
}

py.plot(fig, filename = 'basic-line', auto_open=True)
#pio.write_image(fig, "app/static/fig1.png")


#TODO: 
# Customizing Individual Bar Colors
# Bar Chart with Direct Labels
# Vertical and Horizontal Lines Positioned Relative to the Axes


#trace0 = go.Scatter(
#    x=[3.5],
#    y=[1.9],
#    text=['Horizontal Dashed Line'],
#    mode='text',
#)
#data = [trace0]
#layout = {
##    'xaxis': {
##        'range': [0, 7]
##    },
##    'yaxis': {
##        'range': [0, 2.5]
##    },
#    'shapes': [
#        # Line Horizontal
#        {
#            'type': 'line',
#            'x0': 0,
#            'y0': 8,
#            'x1': 10,
#            'y1': 8,
#            'line': {
#                'color': 'rgb(50, 171, 96)',
#                'width': 4,
#                'dash': 'dashdot',
#            },
#        },
#    ]
#}
#
#fig = {
#    'data': data,
#    'layout': layout,
#}
#
#py.iplot(fig, filename='shapes-lines', auto_open=True)


