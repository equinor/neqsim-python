# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:45:43 2019

@author: esol
"""

from neqsim.thermo import fluid, TPflash, phaseenvelope, fluidComposition, ionComposition, scaleCheck

fluid1 = fluid("Electrolyte-CPA-EoS")  # create a fluid using the Electrolyte-CPA-EoS
fluid1.setTemperature(30.0, "C")
fluid1.setPressure(50.0, "bara")

fluid1.addComponent("nitrogen", 1.0, "mol/sec")
fluid1.addComponent("CO2", 2.3, "mol/sec")
fluid1.addComponent("methane", 80.0, "mol/sec")
fluid1.addComponent("ethane", 6.0, "mol/sec")
fluid1.addComponent("propane", 3.0, "mol/sec")
fluid1.addComponent("water", 100.0, "mol/sec")
fluid1.addComponent("Na+", 0.500, "mol/sec")
fluid1.addComponent("Cl-", 0.500, "mol/sec")
fluid1.addComponent("Ca++", 0.117200, "mol/sec")
fluid1.addComponent("CO3--", 0.117200, "mol/sec")
fluid1.addComponent("Fe++", 10.0e-5, "mol/sec")
fluid1.chemicalReactionInit();
fluid1.setMixingRule(10) # temperature dependent interaction coefficient
#fluid1.setMultiPhaseCheck(True)


TPflash(fluid1)
fluid1.display()

ionComposition(fluid1) # calculates ion composiion of aquous phase
scaleCheck(fluid1) # calculates scale potaential in aqueous phase

print("pH " + str(fluid1.getPhase(1).getpH()))