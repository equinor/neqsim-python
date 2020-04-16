# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:39:11 2020

@author: esol
"""

from neqsim.thermo import fluid, fluid_df, printFrame, TPflash
import pandas as pd


#create gas condesate fluid
gascondensate = {'ComponentName':  ["nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"], 
        'MolarComposition[-]':  [0.53, 3.3, 72.98, 7.68, 4.1, 0.7, 1.42, 0.54, 0.67, 0.85, 1.33, 1.33, 0.78, 0.61, 0.42, 0.33, 0.42, 0.24, 0.3, 0.17, 0.21, 0.15, 0.15, 0.8], 
        'MolarMass[kg/mol]': [None,None, None,None,None,None,None,None,None,None,0.0913, 0.1041, 0.1188, 0.136, 0.150, 0.164, 0.179, 0.188, 0.204, 0.216, 0.236, 0.253, 0.27, 0.391],
        'RelativeDensity[-]': [None,None, None,None,None,None,None,None,None,None, 0.746, 0.768, 0.79, 0.787, 0.793, 0.804, 0.817, 0.83, 0.835, 0.843, 0.837, 0.84, 0.85, 0.877]
  } 

gascondensatedf = pd.DataFrame(gascondensate) 
print(gascondensatedf.head(30).to_string())
gascondensateFluid = fluid_df(gascondensatedf, lastIsPlusFraction=True)


4#Define a function to calculate properties of the fluid
def calcProperties(frame):
        gascondensateFluid.setTemperature(frame[0], "C")
        gascondensateFluid.setPressure(frame[1], "bara")
        TPflash(gascondensateFluid)
        gascondensateFluid.initPhysicalProperties()
        frame['gasthermalconductivity[W/mK]'] = gascondensateFluid.getThermalConductivity("W/mK")
        frame['gasviscosity[kg/msec]']  = gascondensateFluid.getViscosity("kg/msec")
        return frame

temperatures_list = [20.0]*1000
pressures_list = [10.0]*1000

temppres = {'Temperature':  temperatures_list, 
        'Pressure':  pressures_list
  }


df_properties = pd.DataFrame(temppres)
df_properties = df_properties.apply(calcProperties, axis=1)
print(df_properties.tail())