# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 21:36:49 2019

@author: esol
"""

from neqsim.standards import ISO6976
from neqsim.thermo import TPflash, fluid, fluidComposition, phaseenvelope

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(100.0, "bara")
fluid1.addComponent("nitrogen", 1.0, "mol/sec")
fluid1.addComponent("CO2", 2.3, "mol/sec")
fluid1.addComponent("methane", 85.0, "mol/sec")
fluid1.addComponent("ethane", 6.0, "mol/sec")
fluid1.addComponent("propane", 3.0, "mol/sec")
fluid1.addComponent("i-butane", 1.0, "mol/sec")
fluid1.addComponent("n-butane", 1.0, "mol/sec")
fluid1.addComponent("i-pentane", 0.04, "mol/sec")
fluid1.addComponent("n-pentane", 0.002, "mol/sec")
fluid1.addComponent("n-hexane", 0.001, "mol/sec")
fluid1.setMixingRule("classic")  # classic will use binary kij

TPflash(fluid1)

iso6976 = ISO6976(fluid1)
iso6976.setReferenceType("volume")
iso6976.setVolRefT(15.0)
iso6976.setEnergyRefT(15.0)
iso6976.calculate()

GCV = iso6976.getValue("SuperiorCalorificValue") / 1.0e3
WI = iso6976.getValue("SuperiorWobbeIndex") / 1.0e3

print("GCV " + str(GCV) + " MJ/m3")
print("WI " + str(WI), " MJ/m3")
