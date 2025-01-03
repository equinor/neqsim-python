# -*- coding: utf-8 -*-
"""
This script demonstrates the process of CO2 depressurization using the NeqSim library.

The script performs the following steps:
1. Creates a fluid object using the SRK equation of state.
2. Adds 100 moles of CO2 to the fluid.
3. Sets the initial temperature to -25°C and pressure to 18 bara.
4. Enables multi-phase and solid-phase checks for CO2.
5. Performs a temperature-pressure (TP) flash calculation.
6. Calculates the bubble point temperature.
7. Prints the fluid properties before depressurization.
8. Initializes the fluid properties and calculates the enthalpy.
9. Sets the pressure to 1 bara and performs a pressure-enthalpy (PH) flash calculation.
10. Prints the fluid properties after depressurization.

The script also includes commented-out lines for performing dew point and solid phase flash calculations.

Created on Tue Jun 23 10:37:26 2020

@author: ESOL
"""
from neqsim.thermo import (
    PHflash,
    PHsolidflash,
    TPflash,
    TPsolidflash,
    bubt,
    dewt,
    fluid,
    printFrame,
)

fluid1 = fluid("srk")
fluid1.addComponent("CO2", 100.0)

fluid1.setTemperature(-25.0, "C")
fluid1.setPressure(18.0, "bara")
fluid1.setMultiPhaseCheck(True)
fluid1.setSolidPhaseCheck("CO2")

TPflash(fluid1)
# dewt(fluid1)
bubt(fluid1)
printFrame(fluid1)

print("temperature before deprezurization ", fluid1.getTemperature("C"))
fluid1.initProperties()
enthalpy = fluid1.getEnthalpy()

fluid1.setPressure(1.0, "bara")
PHflash(fluid1, enthalpy)
# TPsolidflash(fluid1)
printFrame(fluid1)
print("temperature after deprezurization ", fluid1.getTemperature("C"))

# TPsolidflash(fluid1)
# printFrame(fluid1)
