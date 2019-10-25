# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:24:21 2019

@author: WaterandEnergy
"""


#constants
Cp_air = 1.007                             #kJ/kgK
evap_water = 2247                          #kJ/kg
dens_air = 1.2

#antoine parameters water (0-100 degC)
A = 8.14019
B = 1810.94
C = 244.485

MwAir = 28.97                               #U
MwWater = 18.015                            #U

AtmPressure = 1.01325                        #barA

#P = 10^(A-(B/(C+T)))
#Pressure in mmHG
#T in degC

#pressure conversion
mmHG_to_bar = 0.00133322368


