import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json
f= open('us-states.json', )

states= json.load(f)

df= pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
df_state= pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
df_county= pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

df_state['new_cases']= df_state['cases']- df_state['cases'].shift(-1)
df_nys= df_state.loc[df_state.state=='New York']
df_nyc= df_county.loc[df_county.county=='New York City']


import dash  # use Dash version 1.16.0 or higher for this app to work
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig= go.Figure()

fig.add_trace(go.Scatter(x=df.date, y=df.cases, name= 'US Cases', line= dict(color='#1f77b4', width= 3)))


fig.add_trace(go.Scatter(x=df_nys.date, y=df_nys.cases, name= 'NYS Cases', line= dict(color='#ff7f0e', width= 3)))


fig.add_trace(go.Scatter(x=df_nyc.date, y=df_nyc.cases, name= 'NYC Cases', line= dict(color='#2ca02c', width= 3)))

fig.update_layout(title='Covid-19 Cases in NYC vs NYS and US',
                 xaxis_title='Date',
                 yaxis_title='Number of Cases')


app.layout = html.Div([
    dcc.Graph(id='map-graph', figure={}, className='six columns'),
    dcc.Graph(id='my-graph', figure=fig, clickData=None, hoverData=None, # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  ),
    
])

# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
)
def update_side_graph(hov_data):
    if hov_data is None:
        fig2 = px.choropleth(df_state, geojson=states, locations='fips', color=None,
                           color_continuous_scale="blues",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'new_cases':'new cases'}
                          )
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        hov_year = hov_data['points'][0]['x']
        dff2 = df_state[df_state.date == hov_year]
        #fig2 = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}')
        fig3= px.choropleth(dff2, geojson=states, locations='fips', color='new_cases',
                           color_continuous_scale="blues",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'new_cases':'new cases'}
                          )
        return fig3


if __name__ == '__main__':
    app.run_server(debug=True)