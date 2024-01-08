# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:58:36 2020

@author: esol
"""

from neqsim.thermo.thermoTools import *

temperature = 20.0  # C
presssure = 10.0  # bara
fluid1 = fluid("srk")
fluid1.addComponent("CO2", 1.0, "mol/sec")
fluid1.addComponent("methane", 95.0, "mol/sec")
fluid1.addComponent("ethane", 4.0, "mol/sec")

fluid1.setTemperature(temperature, "C")
fluid1.setPressure(presssure, "bara")

TPflash(fluid1)

fluid1.getInterphaseProperties().initAdsorption()
fluid1.getInterphaseProperties().setSolidAdsorbentMaterial("AC")  # AC Norit R1
fluid1.getInterphaseProperties().calcAdsorption()
surfaceExcessCO2 = (
    fluid1.getInterphaseProperties().getAdsorptionCalc("gas").getSurfaceExcess("CO2")
)

print("surface excess CO2 gas-solid ", surfaceExcessCO2, " kg CO2/kg AC")
