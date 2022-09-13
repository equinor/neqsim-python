# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:03:16 2020

@author: ESOL
"""

import pandas as pd
from neqsim.thermo.thermoTools import *

# In cryogenic processes mercury will typically be in the soild form. Such a calculation is done in neqsim in the follwoing script.

gascondensate = {'ComponentName':  ["mercury", "nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane"],
                 'MolarComposition[-]':  [0.00002, 0.53, 0.003, 82.98, 5.68, 4.1, 0.7, 1.42, 0.54, 0.67, 0.85]
                 }

gascondensatedf = pd.DataFrame(gascondensate)
print("Gas Condensate Fluid:\n")
print(gascondensatedf.head(30).to_string())
gascondensateFluid = fluid_df(
    gascondensatedf, lastIsPlusFraction=True).setModel('SRK-TwuCoon-EOS')
gascondensateFluid.setMixingRule('classic')
gascondensateFluid.setPressure(21.0, "bara")
gascondensateFluid.setTemperature(-90.0, "C")
gascondensateFluid.setMultiPhaseCheck(True)
gascondensateFluid.setSolidPhaseCheck("mercury")
TPflash(gascondensateFluid)

printFrame(gascondensateFluid)


print("T trip ", gascondensateFluid.getPhase(
    0).getComponent('mercury').getTriplePointTemperature())
