# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 10:44:42 2019

@author: esol
"""
from neqsim.thermo.thermoTools import PVTpropTable, TPflash, fluid

fluid1 = fluid('srk')
fluid1.addComponent("methane", 79.2)
fluid1.addComponent("nC10", 79.2)
fluid1.setMultiPhaseCheck(True)
TPflash(fluid1)
fluid1.display()
fileName = "c:/temp/testPVT.tab"

lowTemperature = 273.15  # K
highTemperature = 373.15  # K
Tsteps = 20
lowPressure = 10.0  # bara
highPressure = 100.0  # bara
Psteps = 20

PVTpropTable(fluid1, fileName, lowTemperature, highTemperature,
             Tsteps, lowPressure, highPressure, Psteps)
