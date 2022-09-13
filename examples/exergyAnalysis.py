# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 20:48:13 2020

@author: esol
"""
import neqsim
from neqsim.thermo.thermoTools import *

Tsurr = 20.0+273.15  # surrounding temperature in Kelvin

Tgas = 50.0
P_in = 20.0
P_out = 10.0

fluid_1 = fluid("srk")
fluid_1.addComponent("methane", 1.0, "kg/sec")
fluid_1.addComponent("ethane", 0.10, "kg/sec")
fluid_1.setTemperature(Tgas, "C")
fluid_1.setPressure(P_in, "bara")
TPflash(fluid_1)
T1 = fluid_1.getTemperature("C")
H1 = fluid_1.getEnthalpy("kJ/kg")
U1 = fluid_1.getInternalEnergy("kJ/kg")
S1 = fluid_1.getEntropy("kJ/kgK")
V1 = fluid_1.getVolume("m3")
E1 = fluid_1.getExergy(Tsurr, "kJ/kg")


# simulating a throtling process - an isenthalpic process
fluid_1.setPressure(P_out)
PHflash(fluid_1, E1, "kJ/kg")

T2 = fluid_1.getTemperature("C")
H2 = fluid_1.getEnthalpy("kJ/kg")
U2 = fluid_1.getInternalEnergy("kJ/kg")
S2 = fluid_1.getEntropy("kJ/kgK")
V2 = fluid_1.getVolume("m3")
E2 = fluid_1.getExergy(Tsurr, "kJ/kg")


#Reduction in exergy

redEx = E1-E2

print("Reduction in exergy in valve is ", redEx)


# In an adiabatic expander we will take out work at constant entropy

PSflash(fluid_1, S1, "kJ/kgK")

T3 = fluid_1.getTemperature("C")
H3 = fluid_1.getEnthalpy("kJ/kg")
U3 = fluid_1.getInternalEnergy("kJ/kg")
S3 = fluid_1.getEntropy("kJ/kgK")
V3 = fluid_1.getVolume("m3")
E3 = fluid_1.getExergy(Tsurr, "kJ/kg")

# THe work done will be
work = H1-H3
print("expander work ", work)
# change in exergi is
exChange = E1-E3

print("reduced exergy ",  exChange)
