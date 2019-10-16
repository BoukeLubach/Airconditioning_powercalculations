# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
#        get_logo(),
#        get_header(),
#        html.Br([]),
        get_menu()
    ])

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='http://logonoid.com/images/vanguard-logo.png', height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/dash-vanguard-report/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Vanguard 500 Index Fund Investor Shares')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([
                dcc.Link('Home', href='/home \n', className="tab first", 
                        style={
                                'color':'white',
                                'font-family': 'Open Sans',
                                'text-decoration': 'none',
                                'font-size':'32px'
                        }
                ),
                dcc.Link('TSS', href='/TSS \n', className="tab", 
                        style={
                                'color':'white',
                                'font-family': 'Open Sans',
                                'text-decoration': 'none',
                                'font-size':'32px'
                        }
                ),
                dcc.Link('Time in zone \n', href='/time-in-zone', className="tab", 
                        style={
                                'color':'white',
                                'font-family': 'Open Sans',
                                'text-decoration': 'none',
                                'font-size':'32px'
                        }
                ),

        ], style={  'width': '10%', 
                    'display': 'inline-block', 
                    'vertical-align': 'top',
                    'height' : 1000,
                    'background-color' :'rgb(62, 193, 211)'}
        )

        
                
    return menu
