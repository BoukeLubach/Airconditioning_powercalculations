# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import date
import colorscheme
import dash_table
from equipment import heater, cooler, calcMR
import components
import constants as cn




# STN      LON(east)   LAT(north)     ALT(m)  NAME
# 350:         4.936       51.566      14.90  GILZE-RIJEN
# 370:         5.377       51.451      22.60  EINDHOVEN
# 380:         5.762       50.906     114.30  MAASTRICHT



# YYYYMMDD = datum (YYYY=jaar,MM=maand,DD=dag); 
# HH       = tijd (HH=uur, UT.12 UT=13 MET, 14 MEZT. Uurvak 05 loopt van 04.00 UT tot 5.00 UT; 
# FH       = Uurgemiddelde windsnelheid (in 0.1 m/s). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken; 
# T        = Temperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# TD       = Dauwpuntstemperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# SQ       = Duur van de zonneschijn (in 0.1 uren) per uurvak, berekend uit globale straling  (-1 for <0.05 uur); 
# Q        = Globale straling (in J/cm2) per uurvak; 
# RH       = Uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm); 
# N        = Bewolking (bedekkingsgraad van de bovenlucht in achtsten), tijdens de waarneming (9=bovenlucht onzichtbaar); 
# M        = Mist 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# 
# STN,YYYYMMDD,   HH,   FH,    T,   TD,   SQ,    Q,   RH,    N,    M
# 


loc = [
            {'label':'Gilze-Rijen', 'value':'350'}
        ]
#
##
#df = pd.read_csv('Weergegevens_1990_2018.csv', sep=';').fillna(0)
#df = df.set_index(pd.to_datetime(df['Datetime'], dayfirst=True))
#df['T'] = df['T']/10
#df['TD'] = df['TD']/10
#df['Mix ratio'] = calcMR(df['TD'])


home_layout = html.Div(
        
        
       
        html.Div([
            components.get_menu(),
            
            html.Div([
                    components.get_header(),    
                
                    html.Div(className="dashboard-content",
                        children = [
                                html.Div([
                                        
                                    html.Div([
                                            html.Label("Choose location"),
                                            dcc.Dropdown(id = 'location-input', 
                                                        options=loc,
                                                        value='350'),
                                              
                                            html.Label("Airflow: "),    
                                            dcc.Input(id='airflow-input', type='number', value = 100000 ,placeholder='1000'),                
                                            html.Label("kg/h"),
                                             
                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
    
                                    html.Div([
                                        dcc.Graph(id='Outside-air-graph',
                                                  config={'displayModeBar': False}
                                        ),    
                                        dcc.RangeSlider(
                                            id='year_slider',
                                            min=2000,
                                            max=2019,
                                            value=[2018, 2019],
                                            marks={str(year): str(year) for year in list(range(2000,2020))}
                                        ),
#                                        
                                             
                                             
                                    ], style={'width': '40%', 'display': 'inline-block', 'padding': '2%'}),
                                        
                                    html.Div([
                                             
                                           
                                            html.H5(id='avg-temp'),
                                            html.H5("\n"),
                                            html.H5(id='avg-moisture'),

                                            
                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
                                                                                
                                    
                                                         
                                ]),    


#                               Cooler


                                html.Div([
                                        
                                    html.Div([
                                        html.Label("Desired dewpoint temperature"),    
                                        dcc.Input(id='step1-temperature', type='number', value = 12 ,placeholder='12'),     
                                             
                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
    
                                    html.Div([
                                        dcc.Graph(id='Airconditioning-step1',
                                                  config={'displayModeBar': False}
                                        )         
                                             
                                             
                                    ], style={'width': '40%', 'display': 'inline-block', 'padding': '2%'}),
                                        
                                        
                                    html.Div([
                                        html.H5(id='avg-temp2'),
                                        html.H5("\n"),
                                        html.H5(id='avg-moisture2'),
                                        html.H5("\n"),
                                        html.H5(id='peak-cooling'),
                                        html.H5("\n"),
                                        html.H5(id='avg-cooling'),
                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
                                ]),
#

#                               Heater        

                        
                                html.Div([
                                        
                                    html.Div([
                                        html.Label("Desired air temperature"),    
                                        dcc.Input(id='step2-temperature', type='number', value = 20),     
                                             
                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
    
                                    html.Div([
                                        dcc.Graph(id='Airconditioning-step2',
                                                  config={'displayModeBar': False}
                                        )         
                                             
                                             
                                    ], style={'width': '40%', 'display': 'inline-block', 'padding': '2%'}),
                                        
                                        
                                    html.Div([
                                        html.H5(id='avg-temp3'),
                                        html.H5("\n"),
                                        html.H5(id='avg-moisture3'),
                                        html.H5("\n"),
                                        html.H5(id='peak-heating'),
                                        html.H5("\n"),
                                        html.H5(id='avg-heating'),

                                    ], style={'width': '20%', 'display': 'inline-block', 'padding': '2%', 'verticalAlign':'top'}),
                                ])
                                
                        ], style={'width': '100%', 'display': 'inline-block', 'margin-left':'2%', 'margin-top':'2%'})

            ], style={'width': '88%', 'display': 'inline-block'})

        ],  style={'margin-top':'2%', 'margin-left':'2%'})
)
                



app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


#
@app.callback([Output('Outside-air-graph', 'figure'),
               Output('avg-temp', 'children'),
               Output('avg-moisture','children')],
              [Input('location-input', 'value'),
               Input('year_slider','value')])
def display_waetherdata(locationinput, years):
    

    dff = df[df.Date>years[0]*10000]
    dff = dff[dff.Date<years[1]*10000]

    trace1=go.Scatter(
            x=dff.index, 
            y=dff['T'],
            name = 'Temperature',
            
            
            line= dict(
                    width=2,
                    color='rgb(25,51,51)',
#                    dash = 'dot'
                    )
            )
    data = [trace1]
    layout = go.Layout(
        title="Weather data",
        height=450
        )
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
                template='none',
                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
                )
            )
    
    avgTemp = 'Average temperature:\t' + str(round(dff['T'].mean(),1)) + '\t '+ u'\N{DEGREE SIGN}''C'
    avgMoisture = 'Average moisture content: \t ' +  str(round(dff['Mix ratio'].mean()*1000,1)) + '  gram/kg dry air'
    
    return figure, avgTemp, avgMoisture

@app.callback([Output('Airconditioning-step1', 'figure'),
              Output('avg-temp2', 'children'),
              Output('avg-moisture2','children'),
              Output('peak-cooling', 'children'),
              Output('avg-cooling','children')],                      
              [Input('step1-temperature', 'value'),
               Input('year_slider','value'),
               Input('airflow-input','value')])
def display_coolingresult(desired_temperature, years,airflow):
    dff = df[df.Date>years[0]*10000]
    dff = dff[dff.Date<years[1]*10000]
    
    dff2 = cooler(dff, desired_temperature)
    dff2.to_csv('cooledAir.csv', sep=';')
    
    dff2['Cooling'] = airflow*(dff2['waterRemoved']*cn.evap_water+dff2['T cooled']*cn.Cp_air)/3600
    
    
    
    ## create figure
    trace1=go.Scatter(
            x=dff2.index, 
            y=dff2['T'],
            name = 'Temperature',
            
            line= dict(
                    width=2,
                    color='rgb(25,51,51)'
                    
#                    dash = 'dot'
                    ),
            yaxis = 'y'
            )
    trace2=go.Scatter(
            x=dff2.index, 
            y=dff2['Mix ratio'],
            name = 'Moisture in air',
                                
            line= dict(
                    width=2,
                    color='rgb(255,168,21)',
                    
#                    dash = 'dot'
                    ),
            yaxis = 'y2',
            
            )
    data = [trace1, trace2]
    layout = go.Layout(
        title="Conditioned air",
        height=450,
        yaxis=dict(
            title="Air temperature",
            titlefont=dict(
                color='rgb(25,51,51)'
            ),
            tickfont=dict(
                color='rgb(25,51,51)'
            ),
            range=[-10, 30]
        ),
        yaxis2=dict(
            title="Moisture in air",
            titlefont=dict(
                color='rgb(255,168,21)'
            ),
            tickfont=dict(
                color='rgb(255,168,21)'
            ),
            range=[0, 0.01],
            anchor="x",
            overlaying="y",
            side="right"
        ),
        
    )
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
                template='none',
                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
                )
            )
                
    
    avgTemp = 'Average temperature: \t' + str(round(dff2['T'].mean(),1)) + ' ' + u'\N{DEGREE SIGN}''C'
    avgMoisture = 'Average moisture content: \t ' +  str(round(dff2['Mix ratio'].mean()*1000,1)) + '  gram/kg dry air'
    peakCooling = 'Peak cooling: \t ' +  str(round(dff2['Cooling'].max(),1)) + '  kW'
    avgCooling = 'Average cooling: \t ' +  str(round(dff2['Cooling'].mean(),1)) + '  kW'
    
    
    return figure, avgTemp, avgMoisture, peakCooling, avgCooling


@app.callback([Output('Airconditioning-step2', 'figure'),
              Output('avg-temp3', 'children'),
              Output('avg-moisture3','children'),              
              Output('peak-heating', 'children'),
              Output('avg-heating','children')],   
              [Input('step2-temperature', 'value'),
               Input('year_slider','value'),
               Input('airflow-input','value')])
def display_heatingresult(temperature, years, airflow):
    

    print("code used")
    dff = pd.read_csv('cooledAir.csv', sep=';').fillna(0)

    dff = dff.set_index(pd.to_datetime(dff['Datetime'], dayfirst=True))
    dff2 = heater(dff, temperature)
    dff2['Heating'] = airflow*(dff2['T heated']*cn.Cp_air)/3600
    
    
    trace1=go.Scatter(
            x=dff2.index, 
            y=dff2['T'],
            name = 'Temperature',
            
            line= dict(
                    width=2,
                    color='rgb(25,51,51)'
                    
#                    dash = 'dot'
                    ),
            yaxis = 'y'
            )
    trace2=go.Scatter(
            x=dff2.index, 
            y=dff2['TD'],
            name = 'Moisture in air',
                                
            line= dict(
                    width=2,
                    color='rgb(25,51,51)',
                    
                    dash = 'dot'
                    ),
            yaxis = 'y',
            
            )
    data = [trace1, trace2]
    layout = go.Layout(
        title="Cooled air",
        height=450,
        yaxis=dict(
            title="Air temperature",
            titlefont=dict(
                color='rgb(25,51,51)'
            ),
            tickfont=dict(
                color='rgb(25,51,51)'
            ),
            range=[-10, 30]
        ),
        yaxis2=dict(
            title="Dewpoint temperature",
            titlefont=dict(
                color='rgb(255,168,21)'
            ),
            tickfont=dict(
                color='rgb(255,168,21)'
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        
        )
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
                template='none',
                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
                )
            )
    avgTemp = 'Average temperature: \t' + str(round(dff2['T'].mean(),1)) + ' ' + u'\N{DEGREE SIGN}''C'
    avgMoisture = 'Average moisture content: \t ' +  str(round(dff2['Mix ratio'].mean()*1000,1)) + '  gram/kg dry air'
    peakHeating = 'Peak heating: \t ' +  str(round(dff2['Heating'].max(),1)) + '  kW'
    avgHeating = 'Average heating: \t ' +  str(round(dff2['Heating'].mean(),1)) + '  kW'
    
    return figure, avgTemp, avgMoisture, peakHeating, avgHeating




















#
#def display_output(rows):
#
#    return


# Update page
# # # # # # # # #
# detail in depth what the callback below is doing
# # # # # # # # #
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home_layout
    else:
        return '404'




if __name__ == '__main__':
#    webbrowser.open('http://localhost:8050/')
    app.run_server(debug=False)
    