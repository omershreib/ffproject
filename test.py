
# import datetime
# from datetime import date
#
# time_lable = []
# date_now = datetime.datetime.now().month, datetime.datetime.now().year
# for i in xrange(-4, 0, 1):
#     month = date_now[0] + i
#     year = date_now[1]
#     if month < 1:
#         month = month + 12
#         year = date_now[1] - 1
#     time_lable.append(date(year, month, 1))
# time_lable.append(date(date_now[1], date_now[0], 1))
# for i in xrange(1, 8, 1):
#     month = date_now[0] + i
#     year = date_now[1]
#     if month > 12:
#         month = month - 12
#         year = date_now[1] + 1
#     time_lable.append(date(year, month, 1))
#
# for i in xrange(4,0,-1):
#     print i
# print time_lable

import dash
import dash_html_components as dhc
import dash_core_components as dcc

app = dash.react.Dash('Dash Hello World')

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)
plotly_figure = dict(data=[dict(x=[1, 2, 3], y=[2, 4, 8])])

app.layout = dhc.Div([
    dhc.H2('My First Dash App', style=text_style),
    dhc.P('Enter a Plotly trace type into the text box, such as histogram, bar, or scatter.', style=text_style),
    dcc.Input(id='text1', placeholder='box', value=''),
    dcc.Graph(id='plot1', figure=plotly_figure),
])
@app.react( 'plot1', ['text1'] )
def text_callback( text_input_dict ):
    return {'figure': dict(data=[dict(x=[1,2,3], y=[2,4,8], type=text_input_dict['value'])]) }

# Register your Dash component suites. This line won't be necessary in future releases of Dash.
app.component_suites = [
    'dash_html_components',
    'dash_core_components'
]

app.server.run()