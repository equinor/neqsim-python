# -*- coding: utf-8 -*-
"""
This script simulates a Carnot cycle using the neqsim library for thermodynamic calculations.

The Carnot cycle consists of four main processes:
1. Isothermal Expansion (1-2): Heat is transferred reversibly from a high-temperature reservoir at constant temperature.
2. Isentropic Expansion (2-3): Reversible adiabatic expansion of the gas, resulting in work output.
3. Isothermal Compression (3-4): Heat is transferred reversibly to a low-temperature reservoir at constant temperature.
4. Adiabatic Reversible Compression (4-1): The gas is compressed adiabatically and reversibly.

The script performs the following steps:
1. Initializes a fluid at thermodynamic equilibrium with specified components and conditions.
2. Simulates the isothermal expansion process and calculates the state properties.
3. Simulates the isentropic expansion process and calculates the state properties.
4. Simulates the isothermal compression process and calculates the state properties.
5. Simulates the adiabatic reversible compression process and calculates the state properties.
6. Calculates the Carnot efficiency based on the heat transferred during the cycle.
7. Plots the pressure-volume (PV) and temperature-entropy (TS) diagrams for the Carnot cycle.

Variables:
- P1: Initial pressure in bara.
- T_hot: High temperature in Celsius.
- T_cold: Low temperature in Celsius.
- fluid_1: Thermodynamic fluid object.
- T1, T2, T3, T4, T5: Temperatures at different states in Celsius.
- P2, P3, P4, P5: Pressures at different states in bara.
- H1, H2, H3, H4, H5: Enthalpies at different states in kJ/kg.
- U1, U2, U3, U4, U5: Internal energies at different states in kJ/kg.
- S1, S2, S3, S4, S5: Entropies at different states in kJ/kgK.
- V1, V2, V3, V4, V5: Volumes at different states in m3.
- dS: Change in entropy between states 1 and 2 in kJ/kgK.
- QH: Heat added during the isothermal expansion in kJ.
- QC: Heat rejected during the isothermal compression in kJ.
- efficiency: Calculated Carnot efficiency.
- efficiency2: Theoretical Carnot efficiency.

Plots:
- Pressure vs. Volume (PV) diagram.
- Temperature vs. Entropy (TS) diagram.
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
printFrame(fluid_1)
T1 = fluid_1.getTemperature("C")
H1 = fluid_1.getEnthalpy("kJ/kg")
U1 = fluid_1.getInternalEnergy("kJ/kg")
S1 = fluid_1.getEntropy("kJ/kgK")
V1 = fluid_1.getVolume("m3")

# The Carnot cycle when acting as a heat engine consists of the following steps:¨
# 1-2: Isothermal Expansion. Heat is transferred reversibly from high temperature reservoir at constant temperature TH (isothermal heat addition or absorption).
V2 = V1 * 1.5
TVflash(fluid_1, V2, "m3")
printFrame(fluid_1)
T2 = fluid_1.getTemperature("C")
P2 = fluid_1.getPressure("bara")
H2 = fluid_1.getEnthalpy("kJ/kg")
U2 = fluid_1.getInternalEnergy("kJ/kg")
S2 = fluid_1.getEntropy("kJ/kgK")

# 2-3: Isentropic (reversible adiabatic) expansion of the gas (isentropic work output).
fluid_1.setTemperature(T_cold, "C")
TSflash(fluid_1, S2, "kJ/kgK")
printFrame(fluid_1)

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

printFrame(fluid_1)
# 4-1 Adiabatic reversible compression.

VSflash(fluid_1, V1, S4, "m3", "kJ/kgK")
T5 = fluid_1.getTemperature("C")
P5 = fluid_1.getPressure("bara")
H5 = fluid_1.getEnthalpy("kJ/kg")
U5 = fluid_1.getInternalEnergy("kJ/kg")
S5 = fluid_1.getEntropy("kJ/kgK")
V5 = fluid_1.getVolume("m3")
printFrame(fluid_1)

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
