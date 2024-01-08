# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:08:09 2019

@author: esol
"""
import time

import matplotlib.pyplot as plt
import numpy as np
from neqsim.thermo.thermoTools import *
from neqsim.thermo.thermoTools import fluid, phaseenvelope

time.sleep(3)
eosname = "srk"  # @param ["srk", "pr"]
# @param ["methane", "ethane", "propane", "i-butane", "n-butane"]
camponentName = "CO2"
fluid1 = fluid("eosname")  # create a fluid using the SRK-EoS
fluid1.addComponent(camponentName, 1.0)  # adding 1 mole methane to the fluid

TTrip = fluid1.getPhase(0).getComponent(camponentName).getTriplePointTemperature()
PTrip = fluid1.getPhase(0).getComponent(camponentName).getTriplePointPressure()
Tcritical = fluid1.getPhase(0).getComponent(camponentName).getTC()
Pcritical = fluid1.getPhase(0).getComponent(camponentName).getPC()

fluid1.setTemperature(TTrip)
fluid1.setPressure(PTrip)
print("triple point temperature ", TTrip, "[K] and pressure ", PTrip, "[bara]")
print("critical temperature ", Tcritical, "[K] and pressure ", Pcritical, "[bara]")


def bubleP(pressure):
    fluid1.setPressure(pressure)
    bubt(fluid1)
    return fluid1.getTemperature("C")


pressure = np.arange(PTrip, Pcritical - 5.0, 1.0)
temperature = [bubleP(P) for P in pressure]

plt.plot(temperature, pressure)
plt.xlabel("Temperature [C]")
plt.ylabel("Pressure [bara]")
