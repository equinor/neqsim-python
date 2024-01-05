# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 23:45:38 2020

@author: ESOL
"""


import pandas as pd
from neqsim.thermo import (
    TPflash,
    addOilFractions,
    createfluid,
    createfluid2,
    dataFrame,
    fluid,
    fluid_df,
    fluidcreator,
    phaseenvelope,
    printFrame,
)

reservoirfluid = fluid("Electrolyte-CPA-EoS")
reservoirfluid.addComponent("H2S", 0.12)
reservoirfluid.addComponent("nitrogen", 1.0)
reservoirfluid.addComponent("methane", 70.0)
reservoirfluid.addComponent("ethane", 4.3)
reservoirfluid.addComponent("propane", 1.2)
reservoirfluid.addComponent("nC10", 1.2)
reservoirfluid.addComponent("water", 5.0, "kg/sec")
reservoirfluid.addComponent("Na+", 0.010)
reservoirfluid.addComponent("Cl-", 0.01)
reservoirfluid.addComponent("OH-", 0.0001)

reservoirfluid.chemicalReactionInit()
reservoirfluid.setMultiPhaseCheck(True)
reservoirfluid.setMixingRule(10)

reservoirfluid.setTotalFlowRate(1.0, "MSm3/day")
reservoirfluid.setTemperature(55.0, "C")
reservoirfluid.setPressure(15.0, "bara")


TPflash(reservoirfluid)
printFrame(reservoirfluid)
