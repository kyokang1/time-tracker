import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as offline

#from plotly.offline import iplot, init_notebook_mode

import os
import numpy as np

from app.time_tracker import *

#TODO: APIKey sent to environment
plotly.tools.set_credentials_file(username="kyokang1", api_key='DKCft9dRaKZMfuhb2zFY')

sheet, rows = get_records()

c_year = 2019
rows_year = [r for r in rows if str(r["yyyy"]) == str(c_year)]
rows_year_dt = [r["date"] for r in rows_year]
rows_year_hr = [r["hour"] for r in rows_year]

#TODO: 
# Customizing Individual Bar Colors
# Bar Chart with Direct Labels
# Vertical and Horizontal Lines Positioned Relative to the Axes

#data = [go.Bar(
#    x= rows_year_dt,
#    y= rows_year_hr
#)]

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
#py.plot(data, filename = 'basic-line', auto_open=True)

pio.write_image(fig, "app/static/fig1.png")

