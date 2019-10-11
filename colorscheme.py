# -*- coding: utf-8 -*-

def pickColorset(selection):
    
    if selection == 1:
        color1 = 'rgba(0, 25, 150, {})'
        color2 = 'rgba(228, 0, 124, {})'
        color3 = 'rgba(255, 220, 70, {})'
    else:
        color1 = 'rgba(8, 217, 214, {})'
        color2 = 'rgba(255, 46, 99, {})'
        color3 = 'rgba(100, 18, 39, {})'
        
    return color1, color2, color3 