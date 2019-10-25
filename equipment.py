#

import constants as cn                     
import math
import pandas as pd

def calcTD(MR):
    
    #calculate partial pressure
    volPercent = MR*cn.MwAir/cn.MwWater
    Pbar = volPercent*cn.AtmPressure
    PmmHG = Pbar/cn.mmHG_to_bar
    
    #Reverse Antoine calculation
    D = math.log(PmmHG,10)
    Temp = (cn.C*(cn.A-D)-cn.B)/(D-cn.A)
    
    return Temp

def calcMR(Temp):
    
    #1 calculate partial pressure of water at given temperature using Antoine constants
    PmmHG = 10**(cn.A-(cn.B/(cn.C+Temp)))
    Pbar = PmmHG * cn.mmHG_to_bar

    
    #2 calculate moistuure content at 100% RH
    volPercent = Pbar/cn.AtmPressure
    massPercent = volPercent*cn.MwWater/cn.MwAir

#    print("Moisture content (dry air): " + str(massPercent*1000//0.1*0.1) + "  g/kg")
    return massPercent
   
    
    
def heater(stateIn, T_req):
    stateOut = pd.DataFrame()
    stateOut['TD'] = stateIn['TD']
    stateOut['T heated'] = T_req-stateIn['T']
    stateOut['T heated'][stateOut['T heated']<0] = 0
    stateOut['T'] = stateIn['T']+stateOut['T heated'] 
    stateOut['Mix ratio'] = calcMR(stateOut['TD'])
    return stateOut


def cooler(stateIn, Td_req):
    stateOut = pd.DataFrame()
    
   
    stateOut['TD'] = stateIn['TD']
    stateOut['T'] = stateIn['T']
    
    #reduce temperature when higher than Td
    stateOut['T'][stateOut['T']>Td_req] = Td_req
    stateOut['T cooled'] = stateIn['T']-stateOut['T']

    
    #remove water when Td in is higher than Td req
    stateOut['TD'][stateOut['TD']>Td_req] = Td_req
    stateOut['waterRemoved'] = calcMR(stateIn['TD']) - calcMR(stateOut['TD'])
    
    stateOut['Mix ratio'] = calcMR(stateOut['TD'])

    
       
    return stateOut


#def smartcooler(stateIn, T_req, Td_req):
#    stateOut = pd.DataFrame()
#    
#   
#    stateOut['Td'] = stateIn['Td']
#    stateOut['T'] = stateIn['T']
#    
#    #reduce temperature to required dewpoint if dewpoint is too high
#    stateOut[stateOut['Td']>Td_req] = Td_req
#    stateOut['T'][stateOut['Td']>Td_req] = Td_req
#    stateOut['T cooled'] = stateIn['T']-stateOut['T']
#    stateOut['waterRemoved'] = calcMR(stateIn['Td']) - calcMR(stateOut['Td'])
#    #reduce temperature 
#    stateOut['T'][stateOut['T']>T_req] = T_req
#    
#       
#    return stateOut



def steamspray(stateIn, Td_req):

    stateOut = pd.DataFrame()
    stateOut['T'] = stateIn['T']
    stateOut['waterAdded'] = calcMR(Td_req) - calcMR(stateIn['Td'])
    stateOut['Td'] = stateIn['Td']
    
    stateOut['Td'][stateOut['Td']<Td_req] = Td_req

    
    return stateOut