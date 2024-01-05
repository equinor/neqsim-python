# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:49:07 2020

@author: esol
"""

import matplotlib.pyplot as plt
from neqsim.thermo.thermoTools import *

# The starting point is a fluid at termodynamic equilibrium
P1 = 200.0
T_hot = 200.0
T_cold = 150.0

fluid_1 = fluid("srk")
fluid_1.addComponent("methane", 1.0, "kg/sec")
fluid_1.addComponent("ethane", 0.10, "kg/sec")
fluid_1.setTemperature(T_hot, "C")
fluid_1.setPressure(P1, "bara")
TPflash(fluid_1)
fluid_1.display()
T1 = fluid_1.getTemperature("C")
H1 = fluid_1.getEnthalpy("kJ/kg")
U1 = fluid_1.getInternalEnergy("kJ/kg")
S1 = fluid_1.getEntropy("kJ/kgK")
V1 = fluid_1.getVolume("m3")

# The Carnot cycle when acting as a heat engine consists of the following steps:¨
# 1-2: Isothermal Expansion. Heat is transferred reversibly from high temperature reservoir at constant temperature TH (isothermal heat addition or absorption).
V2 = V1 * 1.5
TVflash(fluid_1, V2, "m3")
fluid_1.display()
T2 = fluid_1.getTemperature("C")
P2 = fluid_1.getPressure("bara")
H2 = fluid_1.getEnthalpy("kJ/kg")
U2 = fluid_1.getInternalEnergy("kJ/kg")
S2 = fluid_1.getEntropy("kJ/kgK")

# 2-3: Isentropic (reversible adiabatic) expansion of the gas (isentropic work output).
fluid_1.setTemperature(T_cold, "C")
TSflash(fluid_1, S2, "kJ/kgK")
fluid_1.display()

T3 = fluid_1.getTemperature("C")
P3 = fluid_1.getPressure()
H3 = fluid_1.getEnthalpy("kJ/kg")
U3 = fluid_1.getInternalEnergy("kJ/kg")
S3 = fluid_1.getEntropy("kJ/kgK")
V3 = fluid_1.getVolume("m3")

# 3-4 Isothermal compression. Heat transferred reversibly to low temperature reservoir at constant temperature TC. (isothermal heat rejection)
TSflash(fluid_1, S1, "kJ/kgK")

T4 = fluid_1.getTemperature("C")
P4 = fluid_1.getPressure("bara")
H4 = fluid_1.getEnthalpy("kJ/kg")
U4 = fluid_1.getInternalEnergy("kJ/kg")
S4 = fluid_1.getEntropy("kJ/kgK")
V4 = fluid_1.getVolume("m3")

fluid_1.display()
# 4-1 Adiabatic reversible compression.

VSflash(fluid_1, V1, S4, "m3", "kJ/kgK")
T5 = fluid_1.getTemperature("C")
P5 = fluid_1.getPressure("bara")
H5 = fluid_1.getEnthalpy("kJ/kg")
U5 = fluid_1.getInternalEnergy("kJ/kg")
S5 = fluid_1.getEntropy("kJ/kgK")
V5 = fluid_1.getVolume("m3")
fluid_1.display()

dS = S2 - S1
QH = (T_hot + 273.15) * dS
QC = (T_cold + 273.15) * dS
efficiency = (QH - QC) / QH

volumes = [V1, V2, V3, V4, V5]
pressures = [P1, P2, P3, P4, P5]
entropy = [S1, S2, S3, S4, S5]
temperature = [T1, T2, T3, T4, T5]

print("Carnot efficiency: ", efficiency)

efficiency2 = 1.0 - (T_cold + 273.15) / (T_hot + 273.15)
print("best Carnot efficiency ", efficiency2)


plt.plot(volumes, pressures)
plt.xlabel("Volume [m3]")
plt.ylabel("Pressure [bara]")
plt.show()

plt.plot(entropy, temperature)
plt.xlabel("Entropy [kJ/kgK]")
plt.ylabel("Temperature [C]")
plt.show()
