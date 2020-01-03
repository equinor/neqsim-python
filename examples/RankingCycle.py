# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:56:35 2020

@author: esol
"""

#There are four processes in the Rankine cycle.
P_cold = 0.06 #bara
P_hot = 50.0 #bara
T_hot_superheat = 350.0 #C

import neqsim
from neqsim.thermo.thermoTools import *

fluid_1 = fluid("cpa-statoil")
fluid_1.addComponent("water", 1.0)
fluid_1.setPressure(P_cold, "bara")
fluid_1.setTotalFlowRate(1000.0, "kg/hr")
bubt(fluid_1)
fluid_1.initProperties()
#TPflash(fluid_1)
#The starting point of the cycle is liuqid at the boiling point 
T1 = fluid_1.getTemperature("C")
H1 = fluid_1.getEnthalpy("kJ/kg")
U1 = fluid_1.getInternalEnergy("kJ/kg")
S1 = fluid_1.getEntropy("kJ/kgK")
V1 = fluid_1.getVolume("m3")

#Process 1–2: The working fluid is pumped from low to high pressure. 
fluid_1.setPressure(P_hot, "bara")
PSflash(fluid_1, S1, "kJ/kgK")
T2 = fluid_1.getTemperature("C")
H2 = fluid_1.getEnthalpy("kJ/kg")
U2 = fluid_1.getInternalEnergy("kJ/kg")
S2 = fluid_1.getEntropy("kJ/kgK")
V2 = fluid_1.getVolume("m3")
fluid_1.display()

#Process 2–3: The high-pressure liquid enters a boiler, where it is heated at constant pressure by an external heat source to become a dry saturated vapour.
fluid_1.setTemperature(T_hot_superheat, "C")
TPflash(fluid_1)
T3 = fluid_1.getTemperature("C")
H3 = fluid_1.getEnthalpy("kJ/kg")
U3 = fluid_1.getInternalEnergy("kJ/kg")
S3 = fluid_1.getEntropy("kJ/kgK")
V3 = fluid_1.getVolume("m3")
fluid_1.display()

#Process 3–4: The dry saturated vapour expands through a turbine, generating power. 
fluid_1.setPressure(P_cold, "bara")
PSflash(fluid_1, S3, "kJ/kgK")
T4 = fluid_1.getTemperature("C")
H4 = fluid_1.getEnthalpy("kJ/kg")
U4 = fluid_1.getInternalEnergy("kJ/kg")
S4 = fluid_1.getEntropy("kJ/kgK")
V4 = fluid_1.getVolume("m3")
fluid_1.display()

#Process 4–1: The wet vapour then enters a condenser, where it is condensed at a constant pressure to become a saturated liquid.
fluid_1.setPressure(P_cold, "bara")
bubt(fluid_1)
fluid_1.initProperties()
T5 = fluid_1.getTemperature("C")
H5 = fluid_1.getEnthalpy("kJ/kg")
U5 = fluid_1.getInternalEnergy("kJ/kg")
S5 = fluid_1.getEntropy("kJ/kgK")
V5 = fluid_1.getVolume("m3")

#estimating efficiency
QH = H3-H2
QC = H4-H5
pumpWork = H2-H1
expanderWork= H3-H4
efficiency = (QH-QC)/QH
print("turbine power generated ", expanderWork, " kJ/kg")
print("pump power used ", pumpWork, " kJ/kg")
print("Efficiency: ", efficiency)
efficiency2 = 1.0 - (T1+273.15)/(T3+273.15)
print("Carnot efficiency ",  efficiency2)

#plot results in Ts-diagram
entropy = [S1, S2,S3, S4, S5]
temperature = [T1, T2, T3, T4, T5]
import matplotlib
import matplotlib.pyplot as plt
plt.plot(entropy, temperature);
plt.xlabel('Entropy [kJ/kgK]');
plt.ylabel('Temperature [C]');
plt.show()
