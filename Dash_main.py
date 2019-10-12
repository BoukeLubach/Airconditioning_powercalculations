import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import webbrowser
import plotly.graph_objs as go
from datetime import date
import colorscheme

df = pd.read_csv('TSSlog2.csv', sep=';')

app = dash.Dash(__name__)

app.layout = html.Div([
        html.Div([
                
            html.Div([
                    html.H3('Column 1'),
                    dcc.Graph(id='CTL-ATL-TSB-graph')
            ], style={'width': '49%', 'display': 'inline-block'}),
            
            html.Div([
                    html.H3('Column 2'),
                    dcc.Graph(id='TSS-overview-graph')
            ],  style={'width': '49%', 'display': 'inline-block'})
        ], className="row"),

        dash_table.DataTable(
            id='TSS-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            editable=True
        ),

])


@app.callback(Output('CTL-ATL-TSB-graph', 'figure'),
              [Input('TSS-table', 'data')])
def display_output(rows):
#    print(rows)
    df2 = pd.DataFrame(rows)
    df2 = df2.set_index(pd.to_datetime(df['Date'],dayfirst=True))
    df2 = df2.drop(columns=['Date'])
    
    df2 = df2[['Planned TSS', 'Actual TSS']].fillna(0)
    
    df2.to_csv('TSSlog2.csv', sep=';')
    

    CTLlookback = 42
    ATLlookback = 7

    ds = df2.values
    
    ds = ds.astype(float)
    
    a = np.zeros((ds.shape[0],6))
    ds = np.append(ds,a,axis=1)
    startATL = 10
    startCTL = 20
    ds[0,2] = startCTL
    ds[0,3] = startCTL
    ds[0,4] = startATL
    ds[0,5] = startATL
#    

    
    for i in range(1, ds.shape[0]):

        ds[i,2] = ds[i-1,2]+(ds[i-1,0]-ds[i-1,2])/CTLlookback      
        ds[i,3] = ds[i-1,3]+(ds[i-1,1]-ds[i-1,3])/CTLlookback
        ds[i,4] = ds[i-1,4]+(ds[i-1,0]-ds[i-1,4])/ATLlookback
        ds[i,5] = ds[i-1,5]+(ds[i-1,1]-ds[i-1,5])/ATLlookback
        

    ds[:,6] = ds[:,2]-ds[:,4]
    ds[:,7] = ds[:,3]-ds[:,5]
    
    df3 = pd.DataFrame()    
    df3 = pd.DataFrame(data = ds)#, index=ds[:,0])
    df3.columns = ['Planned TSS', 'Actual TSS', 'Planned CTL', 'Actual CTL', 'Planned ATL', 'Actual ATL', 'Planned TSB', 'Actual TSB']
    df3.index = df2.index
    
    today = pd.to_datetime(date.today())
    df4 = df3[df3.index < today]
        
    [color1, color2, color3] = colorscheme.pickColorset(3)

    trace1=go.Scatter(
            x=df3.index, 
            y=round(df3['Planned CTL']),
            name = df3.columns[1],
                    
            line= dict(
                    width=4,
                    color=color1.format('1'),
                    dash = 'dot'
                    )
            )
    
    
    trace2=go.Scatter(
            x=df4.index, 
            y=round(df4['Actual CTL']),
            name = df4.columns[2],
                        
            fill='tozeroy',
            fillcolor=color1.format('0.1'), 
            line= dict(
                    width=4,
                    color=color1.format('1')
                    )
            )
            
    trace3=go.Scatter(
            x=df3.index, 
            y=round(df3['Planned ATL']),
            name = df3.columns[3],
            line= dict(
                    width=4,
                    color= color2.format('1'),
                    dash = 'dot'
                    )
            )
                
      
    trace4=go.Scatter(
            x=df4.index, 
            y=round(df4['Actual ATL']),
            name = df4.columns[4],
            fillcolor= color2.format('0.1'),
            line= dict(
                    width=4,
                    color= color2.format('1')
                    )
            )
                
                
    trace5=go.Scatter(
            x=df3.index, 
            y=round(df3['Planned TSB']),
            name = df3.columns[5],
            line= dict(
                    width=4,
                    color=color3.format('1'),
                    dash = 'dot'
                    )
            )
                
    trace6=go.Scatter(
            x=df4.index, 
            y=round(df4['Actual TSB']),
            name = df3.columns[6],
            fill='tozeroy',
            fillcolor=color3.format('0.1'), 
            line= dict(
                    width=4,
                    color=color3.format('1')
                    )
            )
    
    data = [trace1, trace2, trace3, trace4, trace5, trace6]
    layout = go.Layout(
        title="Performance balance",
        height=450
        )
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(                
            template='none')
    figure.update_xaxes(range=[today-pd.Timedelta(days=30), today+pd.Timedelta(days=60)])
    
    
    return figure









@app.callback(Output('TSS-overview-graph', 'figure'),
              [Input('TSS-table', 'data')])

def display_TSS(rows):
#    print(rows)
    df2 = pd.DataFrame(rows)
    df2 = df2.set_index(pd.to_datetime(df['Date'],dayfirst=True))
    df2 = df2.drop(columns=['Date'])
    
    df2 = df2[['Planned TSS', 'Actual TSS']].fillna(0)
    today = pd.to_datetime(date.today())
           
    [color1, color2, color3] = colorscheme.pickColorset(3)

    trace1=go.Bar(
            x=df2.index, 
            y=round(df2['Actual TSS']),
            name = df2.columns[1]
            )
    
    data = [trace1]
    layout = go.Layout(
        title="TSS",
        height=450
        )
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
                template='none')
    figure.update_xaxes(range=[today-pd.Timedelta(days=30), today+pd.Timedelta(days=10)])
    
    return figure


if __name__ == '__main__':
#    webbrowser.open('http://localhost:8050/')
    app.run_server(debug=False)
    