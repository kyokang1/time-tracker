import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from app.time_tracker import *

#TODO: APIKey sent to environment
plotly.tools.set_credentials_file(username="kyokang1", api_key='DKCft9dRaKZMfuhb2zFY')

sheet, rows = get_records()

c_year = 2019
rows_year = [r for r in rows if str(r["yyyy"]) == str(c_year)]
rows_year_dt = [r["date"] for r in rows_year]
rows_year_hr = [r["hour"] for r in rows_year]

data = [go.Bar(
    x= rows_year_dt,
    y= rows_year_hr
)]

py.plot(data, filename = 'basic-line', auto_open=True)



