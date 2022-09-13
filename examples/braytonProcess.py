# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:06:45 2020

@author: esol
"""

import matplotlib
# @markdown Simulation of a Braiton Cycle in neqsim
import matplotlib.pyplot as plt
import neqsim
from neqsim.standards import ISO6976
from neqsim.thermo.thermoTools import *

T1 = 15.0
P1 = 1.01325

T2 = 30.0
P2 = 15.4

drygas = createfluid('dry gas')
drygas.setPressure(P2, "bara")
drygas.setTemperature(T2, "C")
drygas.setTotalFlowRate(14.8, "kg/sec")
TPflash(drygas)

# printFrame(drygas)

air = createfluid('air')
air.setPressure(P1, "bara")
air.setTemperature(T1, "C")
air.setTotalFlowRate(630.0, "kg/sec")
TPflash(air)

S1 = air.getEntropy("kJ/kgK")
H1 = air.getEnthalpy("kJ/kg")
V1 = air.getVolume("m3")
P1 = air.getPressure("bara")
T1 = air.getTemperature("C")

# 1. adiabatic process – compression
air.setPressure(P2, "bara")
PSflash(air, S1, "kJ/kgK")
printFrame(air)

S2 = air.getEntropy("kJ/kgK")
H2 = air.getEnthalpy("kJ/kg")
V2 = air.getVolume("m3")
P2 = air.getPressure("bara")
T2 = air.getTemperature("C")


# 2. isobaric process – heat addition
GCVgas = GCV(drygas, 'kJ/kg')
energyCombustion = GCVgas*1000.0*drygas.getFlowRate("kg/sec")
air.setTemperature(1400.0)
PHflash(air, air.getEnthalpy()+energyCombustion, "J")

S3 = air.getEntropy("kJ/kgK")
H3 = air.getEnthalpy("kJ/kg")
V3 = air.getVolume("m3")
P3 = air.getPressure("bara")
T3 = air.getTemperature("C")

# 3. adiabatic process – expansion
air.setPressure(P1, "bara")
PSflash(air, S3, "kJ/kgK")

S4 = air.getEntropy("kJ/kgK")
H4 = air.getEnthalpy("kJ/kg")
V4 = air.getVolume("m3")
P4 = air.getPressure("bara")
T4 = air.getTemperature("C")

# 4. isobaric process – heat rejection
PHflash(air, H1, "kJ/kg")

S5 = air.getEntropy("kJ/kgK")
H5 = air.getEnthalpy("kJ/kg")
V5 = air.getVolume("m3")
P5 = air.getPressure("bara")
T5 = air.getTemperature("C")

idealBrytonEff = 1.0 - T1/T2
airMassFlow = air.getFlowRate("kg/sec")
fuelMassFLow = drygas.getFlowRate("kg/sec")
AFR = airMassFlow/fuelMassFLow
print("air fuel ratio ", AFR, " kg/kg")

print("air inlet flow ", V1, " m3/sec")
print("fuel inlet flow ", drygas.getFlowRate("kg/sec"), " kg/sec")
print("compressor power ", (H2-H1)*airMassFlow/1e3, " MW")
print("Heat of combustion ", GCVgas/1e3, " MJ/kg")
print("Turbine power ", (H3-H4)*airMassFlow/1e3, " MW")
print("Temperature of air to turbine ", T3, " C")
print("Temperature of exhaust air ", T4, " C")

powerOutput = (H3-H4)*airMassFlow/1e3 - (H2-H1)*airMassFlow/1e3
print("plant net output ", powerOutput, " MW")
netEfficiency = powerOutput/(energyCombustion/1e6)
print("efficiency ", netEfficiency)
# plot results in Ts-diagram
entropy = [S1, S2, S3, S4, S5]
temperature = [T1, T2, T3, T4, T5]
plt.plot(entropy, temperature)
plt.xlabel('Entropy [kJ/kgK]')
plt.ylabel('Temperature [C]')
plt.show()
