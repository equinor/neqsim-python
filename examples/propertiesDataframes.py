# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:39:11 2020

@author: esol
"""

from neqsim.thermo import fluid, fluid_df, printFrame, TPflash, phaseenvelope
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


4#Define a function to calculate properties of the fluid at equilibrium at given temperature and pressure
def calcProperties(frame):
        gascondensateFluid.setTemperature(frame[0], "C")
        gascondensateFluid.setPressure(frame[1], "bara")
        TPflash(gascondensateFluid)
        gascondensateFluid.initPhysicalProperties()
        #Reporting some properties of the total fluid
        frame['molarmass[kg/mol]'] =gascondensateFluid.getMolarMass('kg/mol')
        frame['enthalpy[J/mol]'] =gascondensateFluid.getEnthalpy("J/mol")
        #Reporting some properties of the gas phase (NaN will be reported if the phase is not present)
        if gascondensateFluid.hasPhaseType("gas"):
            phaseNumber = gascondensateFluid.getPhaseNumberOfPhase("gas")
            frame['gasmolfraction[mol/mol]'] = gascondensateFluid.getMoleFraction(phaseNumber)
            frame['gasvolumefraction[mol/mol]'] =  gascondensateFluid.getCorrectedVolumeFraction(phaseNumber)
            frame['gasthermalconductivity[W/mK]'] = gascondensateFluid.getPhase(phaseNumber).getThermalConductivity("W/mK")
            frame['gasZ[-]'] = gascondensateFluid.getPhase(phaseNumber).getZ()
            frame['gasmolarMass[kg/mol]'] = gascondensateFluid.getPhase(phaseNumber).getZ()
            frame['gasenthalpy[kg/mol]'] = gascondensateFluid.getPhase(phaseNumber).getEnthalpy("J/mol")
            frame['gasviscosity[kg/msec]']  = gascondensateFluid.getViscosity("kg/msec")
        #Reporting some properties of the oil phase (NaN will be reported if the phase is not present)
        if gascondensateFluid.hasPhaseType("oil"):
            phaseNumber = gascondensateFluid.getPhaseNumberOfPhase("oil")
            frame['oilmolfraction[mol/mol]'] = gascondensateFluid.getMoleFraction(phaseNumber)
            frame['oilvolumefraction[mol/mol]'] =  gascondensateFluid.getCorrectedVolumeFraction(phaseNumber)
            frame['oilthermalconductivity[W/mK]'] = gascondensateFluid.getPhase(phaseNumber).getThermalConductivity("W/mK")
            frame['oilZ[-]'] = gascondensateFluid.getPhase(phaseNumber).getZ()
            frame['oilmolarMass[kg/mol]'] = gascondensateFluid.getPhase(phaseNumber).getZ()
            frame['oilenthalpy[kg/mol]'] = gascondensateFluid.getPhase(phaseNumber).getEnthalpy("J/mol")
            frame['oilviscosity[kg/msec]']  = gascondensateFluid.getViscosity("kg/msec")
        return frame

temperatures_list = [random.uniform(0.0, 500.0) for i in range(1000)] #Create list of 1000 random tempeatures between 0 and 50 deg C
pressures_list = [random.uniform(1.0, 450.0) for i in range(1000)] #Create list of  1000 random pressures between 1 and 450 bara

temppres = {'Temperature':  temperatures_list, 
        'Pressure':  pressures_list
  }


df_properties = pd.DataFrame(temppres)
df_properties = df_properties.apply(calcProperties, axis=1)
print(df_properties)

