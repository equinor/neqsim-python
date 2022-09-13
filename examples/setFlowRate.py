# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:51:59 2020

@author: ESOL
"""

# -*- coding: utf-8 -*-
"""
The current python script demonstrates simple ways of creating fluids in neqsim
@author: esol
"""


from neqsim.thermo.thermoTools import *
from neqsim.thermo import (TPflash, addOilFractions, createfluid, createfluid2,
                           dataFrame, fluid, fluid_df, fluidcreator,
                           phaseenvelope, printFrame)
import pandas as pd
import neqsim
# Create a gas-condensate fluid

naturalgas = {'ComponentName':  ["nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane"],
              'MolarComposition[-]':  [0.34, 0.84, 90.4, 5.199, 2.06, 0.36, 0.55, 0.14, 0.097, 0.014]
              }

naturalgasdf = pd.DataFrame(naturalgas)
print("Natural Gas Fluid:\n")
print(naturalgasdf.head(30).to_string())
naturalgasFluid = fluid_df(naturalgasdf)

naturalgasFluid.setPressure(51.0, "bara")
naturalgasFluid.setTemperature(26.3, "C")

TPflash(naturalgasFluid)

printFrame(naturalgasFluid)

naturalgasFluid.setTotalFlowRate(622.4, "Am3/hr")
TPflash(naturalgasFluid)
print("flow rate ", naturalgasFluid.getFlowRate("m3/hr"))


# Test 1:
naturalgasFluid.setPressure(51.0, "bara")
naturalgasFluid.setTemperature(26.3, "C")
naturalgasFluid.setTotalFlowRate(550.2335548644567, "Am3/hr")

TPflash(naturalgasFluid)
naturalgasFluid.initProperties()
print("flow rate ", naturalgasFluid.getFlowRate("Sm3/day"))
print("flow rate ", naturalgasFluid.getFlowRate("kg/hr"))
print("flow rate ", naturalgasFluid.getFlowRate("m3/hr"))


# Test 2:
naturalgasFluid.setPressure(51.0, "bara")
naturalgasFluid.setTemperature(26.3, "C")
naturalgasFluid.setTotalFlowRate(550.2335548644567, "Am3/hr")

TPflash(naturalgasFluid)
naturalgasFluid.initProperties()

print("flow rate ", naturalgasFluid.getFlowRate("kg/hr"))
print("flow rate ", naturalgasFluid.getFlowRate("Sm3/day"))
print("flow rate ", naturalgasFluid.getFlowRate("m3/hr"))

# Test 3:
naturalgasFluid.setPressure(151.0, "bara")
naturalgasFluid.setTemperature(36.3, "C")
naturalgasFluid.setTotalFlowRate(520.2335548644567, "Am3/hr")

TPflash(naturalgasFluid)
naturalgasFluid.initProperties()

print("flow rate ", naturalgasFluid.getFlowRate("kg/hr"))
print("flow rate ", naturalgasFluid.getFlowRate("Sm3/day"))
print("flow rate ", naturalgasFluid.getFlowRate("m3/hr"))

# Test 4:
naturalgasFluid.setPressure(51.0, "bara")
naturalgasFluid.setTemperature(26.3, "C")
naturalgasFluid.setTotalFlowRate(550.2335548644567, "Am3/hr")

TPflash(naturalgasFluid)
naturalgasFluid.initProperties()

print("flow rate ", naturalgasFluid.getFlowRate("kg/hr"))
print("flow rate ", naturalgasFluid.getFlowRate("Sm3/day"))
print("flow rate ", naturalgasFluid.getFlowRate("m3/hr"))
