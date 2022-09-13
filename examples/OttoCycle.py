# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:39:13 2020

@author: esol
"""

import matplotlib
import matplotlib.pyplot as plt
import neqsim
from neqsim.standards import ISO6976
from neqsim.thermo.thermoTools import *

T1 = 15.0
P1 = 1.01325

compressionRatio = 14
T2 = 30.0
P2 = 15.4

petrol = createfluid('dry gas')
petrol.setPressure(P2, "bara")
petrol.setTemperature(T2, "C")
petrol.setTotalFlowRate(22.2, "kg/hr")
TPflash(petrol)

# Process 0–1 intake stroke (green arrow)
air = createfluid('air')
air.setPressure(P1, "bara")
air.setTemperature(T1, "C")
air.setTotalFlowRate(3100.0, "kg/hr")
TPflash(air)

S1 = air.getEntropy("kJ/kgK")
H1 = air.getEnthalpy("kJ/kg")
V1 = air.getVolume("m3")
P1 = air.getPressure("bara")
T1 = air.getTemperature("C")

# Process 1–2 compression stroke (B on diagrams)
V2 = V1/compressionRatio
VSflash(air, V2, S1, "m3", "kJ/kgK")

S2 = air.getEntropy("kJ/kgK")
H2 = air.getEnthalpy("kJ/kg")
V2 = air.getVolume("m3")
P2 = air.getPressure("bara")
T2 = air.getTemperature("C")


# Process 2–3 ignition phase
GCVgas = GCV(petrol, 'kJ/kg')
energyCombustion = GCVgas*1000.0*petrol.getFlowRate("kg/sec")
VHflash(air, V2, air.getEnthalpy()+energyCombustion, "m3", "J")
# need to implement this in java/python
S3 = air.getEntropy("kJ/kgK")
H3 = air.getEnthalpy("kJ/kg")
V3 = air.getVolume("m3")
P3 = air.getPressure("bara")
T3 = air.getTemperature("C")

# Process 3–4 expansion stroke
VSflash(air, V1, S3, "m3", "kJ/kgK")

S4 = air.getEntropy("kJ/kgK")
H4 = air.getEnthalpy("kJ/kg")
V4 = air.getVolume("m3")
P4 = air.getPressure("bara")
T4 = air.getTemperature("C")

# Process 4–1 idealized heat rejection
VSflash(air, V1, S1, "m3", "kJ/kgK")

S5 = air.getEntropy("kJ/kgK")
H5 = air.getEnthalpy("kJ/kg")
V5 = air.getVolume("m3")
P5 = air.getPressure("bara")
T5 = air.getTemperature("C")

airMassFlow = air.getFlowRate("kg/sec")
fuelMassFLow = petrol.getFlowRate("kg/sec")
AFR = airMassFlow/fuelMassFLow
print("air fuel ratio ", AFR, " kg/kg")
print("air inlet flow ", V1, " m3/sec")
print("fuel inlet flow ", petrol.getFlowRate("kg/sec"), " kg/sec")
print("pistion power ", (H3-H4)*airMassFlow, " kW")
print("Heat of combustion ", GCVgas, " kJ/kg")

powerOutput = (H3-H4)*airMassFlow - (H2-H1)*airMassFlow
print("power output ", powerOutput, " kW, ", (powerOutput*1.3596216173), " hp")

# plot results in Ts-diagram
entropy = [S1, S2, S3, S4, S5]
temperature = [T1, T2, T3, T4, T5]
volumes = [V1, V2, V3, V4, V5]
pressures = [P1, P2, P3, P4, P5]
plt.plot(entropy, temperature)
plt.xlabel('Entropy [kJ/kgK]')
plt.ylabel('Temperature [C]')
plt.show()

plt.plot(volumes, pressures)
plt.xlabel('Volume [m3]')
plt.ylabel('Pressure [bara]')
plt.show()
