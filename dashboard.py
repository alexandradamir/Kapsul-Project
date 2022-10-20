from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import numpy as np
from datetime import datetime as dt
import plotly.express as px

#import cleaned air quality datasets
bosna= pd.read_csv('/workspace/project/bosna.csv')
selcuklu=pd.read_csv('/workspace/project/selcuklu.csv')
#add all air quality datasets the same way

#import air quality stations location dataset
data= pd.read_csv('/workspace/project/23_202108_havaistasyonkonum.csv')

# create a point geometry column
from shapely.geometry import Point
data['geometry'] = data.apply(lambda x: Point((x.BOYLAM, x.ENLEM)),axis = 1)
data.head(3)

#Creating a GeoDataFrame from a DataFrame
data_crs = {'init':  'epsg:4326'}
data_geo = gpd.GeoDataFrame(data,
                            crs = data_crs,
                            geometry = data.geometry)
data_geo.head(3)

#save all datasets in a variable
myVars = locals()

#create map graph of the stations location
import plotly.graph_objects as go
fig = go.Figure(go.Scattermapbox(lat=list(data['ENLEM']),
                        lon=list(data['BOYLAM']),
                        mode='markers',
                        marker=dict(size=12),
                        text=data['ISTASYON_ADI'],
                        hoverinfo='text'))

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox=dict(
        center=go.layout.mapbox.Center(
            lat=data['ENLEM'][0],
            lon=data['BOYLAM'][0]
        ),
        zoom=9
    )
)

# Build the app components
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], suppress_callback_exceptions=True)
mytitle = html.H1('Air quality in the city of Konya')
mygraph = dcc.Graph(id='plot', figure=fig)
text=html.P(id='text', children=[])

# Customize Layout
app.layout = html.Div([
    mytitle,
    html.Div([
        html.Div([mygraph], style={'display':'inline-block','width':'60%'}),
        html.Div(
        style={'display':'inline-block','width':'35%', 'vertical-align': 'top', 'text-align':'justify'},
        id='info')
    ],
    style={'width':'100%', 'height':'90%','display':'inline-block'}),
    html.Div([html.Div(id='date_picker'),
        html.Div(id='graph')],
        style={'width':'60%'}),
    # dcc.Store inside the user's current browser session
    dcc.Store(id='store-data', data=[], storage_type='memory') # 'local' or 'session'
],style={'text-align':'center','display':'inline-block', 'width':'100%','margin-left':'5px'})

# Trigger callback on click
@app.callback(
    Output('store-data', 'data'),
    Input('plot', 'clickData')
)
#store the clicked dataset (station)
def store_data(clickData):
    if clickData:
        station = clickData['points'][0]['text']
        data=myVars[station]
        dff=data[~data.iloc[:, 2:].isnull().all(axis=1)]
        return dff.to_dict('records')

#create buttons with air quality information and a date picker
@app.callback(
    Output('info', 'children'),
    Output('date_picker', 'children'),
    Input('plot', 'clickData'),
    Input('store-data', 'data'))

def info(clickData, data):

    if not clickData:
        return html.H3('Select a station to see key stats'),''

    dff = pd.DataFrame(data)
    station = clickData['points'][0]['text']
    last_info=dff.sort_values(by='date', ascending=False)\
        .reset_index(drop=True).loc[0,]
    first_info=dff.sort_values(by='date', ascending=True)\
        .reset_index(drop=True).loc[0,]
    last_date=last_info['date']
    buttons=[]

    for c in dff.iloc[:, 2:]:
        if np.isnan(last_info[c]):
            buttons.append(dbc.Button(f'{c}: No information', id=c, n_clicks=0, outline=True, color="secondary", className="me-1"))
        else: 
            buttons.append(dbc.Button(f'{c}: {last_info[c]}', id=c, n_clicks=0, outline=True, color="info", className="me-1"))

    info=[html.H3([f'Air quality for : {station.capitalize()}'], id='station'),
            html.H4([f'Date: {last_date}', html.Br()], id='date'), 
            html.Div(buttons, id='buttons'),
            text]

    date_picker= dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        min_date_allowed=str(first_info['date']),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=str(last_info['date']),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=str(last_info['date']),  # the month initially presented when the user opens the calendar
        display_format='YYYY-MM-DD',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        minimum_nights=0,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='memory',  # session, local, or memory. Default is 'local'

        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
        ),

    return info, date_picker

#create 2 dropdowns(air quality index and type of graph) and a graph
@app.callback(
    Output('graph', 'children'),
    Input('store-data', 'data'),
    [State('graph', 'children')]
)
def display_graphs(data, div_children):
    if data:
        dff = pd.DataFrame(data)
        values=[{'label': s, 'value': s} for s in np.sort(dff.iloc[:, 2:].columns)]
        first_column=dff.iloc[:, 2:].columns[0]
        div_children = html.Div(
            style={'width': '100%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'margin-left':'45px', 'padding': 10},
            children=[
                dcc.Dropdown(
                    id='options',
                    style={'color': 'black'},
                    options=values,
                    multi=False,
                    value=first_column
                )
            ]
        ),html.Div(
            style={'width': '100%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'margin-left':'45px', 'padding': 10},
            children=[
                dcc.Dropdown(
                    id='graph_type',
                    style={'color': 'black'},
                    options=[{'label': 'Day Comparison Chart', 'value': 'day_comparison'},
                        {'label': 'Month Comparison Chart', 'value': 'month_comparison'},
                        {'label': 'Trend Chart', 'value': 'trend'}],
                    multi=False,
                    value='trend'
                )
            ]
        ),html.Div(
            style={'width': '100%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'margin-left':'45px', 'padding': 10},
            children=[
                dcc.Graph(
                     id='line',
                     figure={}
                )
            ]
        )
        return div_children

#update graph based on user selections in the dropdowns and date picker
@app.callback(
    Output('line', 'figure'),
    Input('options', 'value'),
    Input('graph_type', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('store-data', 'data'))

def update_graph(value, type, start_date, end_date, data):
    if data is not None :
        dff = pd.DataFrame(data)
        dff['date']=pd.to_datetime(dff['date'])
        if value not in dff.iloc[:, 2:].columns:
            fig={}
        else:
                if end_date is None:
                    fig = px.line(dff, x='date', y=value)
                elif start_date is None:
                    dff = dff[dff['date'].dt.strftime('%Y-%m-%d') == end_date]
                    fig = px.line(dff, x='date', y=value)
                else:
                    if type=='trend':
                        dff = dff[(dff['date'].dt.strftime('%Y-%m-%d')>=start_date) & (dff['date'].dt.strftime('%Y-%m-%d')<=end_date)]
                        fig = px.line(dff, x='date', y=value)
                    elif type=='day_comparison':
                        dff = dff[(dff['date'].dt.strftime('%Y-%m-%d')>=start_date) & (dff['date'].dt.strftime('%Y-%m-%d')<=end_date)]
                        fig=px.line(
                            data_frame=dff,  
                            x=dff['date'].dt.hour,  
                            y=value, 
                            color=dff['date'].dt.strftime('%Y-%m-%d'),
                            labels={'x':'Hour'})
                    elif type=='month_comparison':
                        dff = dff[(dff['date'].dt.strftime('%Y-%m-%d')>=start_date) & (dff['date'].dt.strftime('%Y-%m-%d')<=end_date)]
                        fig = px.bar(  
                            data_frame=dff,  
                            x=dff['date'].dt.day,  
                            y='pm10_µg_m3', color=dff['date'].dt.strftime('%Y-%m'),
                            barmode = 'overlay', labels={'x':'Day'})
        return fig
#run app on server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8055)


