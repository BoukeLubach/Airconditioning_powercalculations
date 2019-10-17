# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc


def get_menu():

    menu = html.Div(
                className="menu-bar",
                children = [
                        
                    dcc.Link('Home', href='/home', className="menu-link", 
                            style={
                                    'color':'white',
                                    'font-family': 'Open Sans',
                                    'text-decoration': 'none',
                                    'font-size':'32px'
                            }
                    ),
                    html.H3('\n'),
                    dcc.Link('TSS \n', href='/TSS', className="menu-link", 
                            style={
                                    'color':'white',
                                    'font-family': 'Open Sans',
                                    'text-decoration': 'none',
                                    'font-size':'32px'
                            }
                    ),
                    html.H3('\n'),
                    dcc.Link('Time in zone \n', href='/time-in-zone', className="menu-link", 
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
                    'height' : 1000
                    },

    )
    
    return menu

def get_header():
    
    header = html.Div(
                className="header",
                children= [
                    html.H3('Log'),
                ]
                
            )      
                    

    
    return header
