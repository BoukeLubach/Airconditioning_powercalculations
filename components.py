# -*- coding: utf-8 -*-

import dash_html_components as html


def get_menu():

    menu = html.Div(
                className="menu-bar",
                children = [
                        
                    

               
                ], style={  'width': '10%', 
                    'display': 'inline-block', 
                    'vertical-align': 'top',
                    'height' : 1500,
                    'border-top-left-radius' :'25px' },

    )
    
    return menu

def get_header():
    
    header = html.Div(
                className="header",
                children= [
                    html.H3('Weather data'),
                ]
                
            )      
                    

    
    return header
