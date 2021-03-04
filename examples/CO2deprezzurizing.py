# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:37:26 2020

@author: ESOL
"""
from neqsim.thermo import fluid, TPflash,printFrame,PHflash, PHsolidflash,TPsolidflash,dewt,bubt


fluid1 = fluid('srk')
fluid1.addComponent("CO2", 100.0)

fluid1.setTemperature(-25.0, "C")
fluid1.setPressure(18.0, "bara")
fluid1.setMultiPhaseCheck(True)
fluid1.setSolidPhaseCheck("CO2")

TPflash(fluid1)
#dewt(fluid1)
bubt(fluid1)
printFrame(fluid1)

print("temperature before deprezurization ", fluid1.getTemperature("C"))
fluid1.initProperties()
enthalpy = fluid1.getEnthalpy()

fluid1.setPressure(1.0, "bara")
PHflash(fluid1, enthalpy)
#TPsolidflash(fluid1)
printFrame(fluid1)
print("temperature after deprezurization ", fluid1.getTemperature("C"))

#TPsolidflash(fluid1)
#printFrame(fluid1)