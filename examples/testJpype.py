# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:28:07 2020

@author: ESOL
"""

# Import module
import jpype
# Enable Java imports
import jpype.imports
from jpype.types import *
from neqsim.neqsimpython import neqsim

fluid1 = neqsim.thermo.system.SystemSrkEos(303.15, 35.01325)

fluid1.addComponent("nitrogen", 0.0028941)
fluid1.addComponent("CO2", 0.054069291)
fluid1.addComponent("methane", 0.730570915)
fluid1.addComponent("ethane", 0.109004002)
fluid1.addComponent("propane", 0.061518891)
fluid1.addComponent("n-butane", 0.0164998)
fluid1.addComponent("i-butane", 0.006585)
fluid1.addComponent("n-pentane", 0.005953)
fluid1.addComponent("i-pentane", 0.0040184)
fluid1.addTBPfraction("C6", 0.6178399, 86.17801 / 1000.0, 0.6639999)
fluid1.addComponent("water", 0.27082)
fluid1.createDatabase(True)
fluid1.setMixingRule(2)
fluid1.setMultiPhaseCheck(True)
