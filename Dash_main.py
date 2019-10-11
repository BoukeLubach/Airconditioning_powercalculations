import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import webbrowser
import plotly.graph_objs as go


df = pd.read_csv('TSSlog2.csv', sep=';')



app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(dcc.Graph(id='CTL-ATL-TSB-graph')),
    dash_table.DataTable(
        id='TSS-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
#        [
#            {'Planned TSS{}'.format(i): (j + (i-1)*5) for i in range(1, 5)}
#            for j in range(4)
#        ],
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
#    df3.to_csv('TSSlog3.csv', sep=';')

    
    
    
    trace1=go.Scatter(x=df3.index, y=round(df3['Planned CTL']))
    trace2=go.Scatter(x=df3.index, y=round(df3['Actual CTL']))
    trace3=go.Scatter(x=df3.index, y=round(df3['Planned ATL']))
    trace4=go.Scatter(x=df3.index, y=round(df3['Actual ATL']))
    
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title="My Dash Graph",
        height=700,
        template = 'none')
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(template='none')
    
    
    return figure


if __name__ == '__main__':
    webbrowser.open('http://localhost:8050/')
    app.run_server(debug=False)
    