# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:20:04 2019

@author: esol

Created on Thu Jun 13 10:01:36 2019

The current python script demonstrates use of neqsim in python
A gas mixture is defined and the density of the gas is calculated.
@author: esol
"""
from neqsim.thermo import fluid, TPflash, phaseenvelope, fluidComposition

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(100.0, "bara")
fluid1.addComponent("nitrogen", 1.0, "mol/sec")
fluid1.addComponent("CO2", 2.3, "mol/sec")
fluid1.addComponent("methane", 80.0, "mol/sec")
fluid1.addComponent("ethane", 6.0, "mol/sec")
fluid1.addComponent("propane", 3.0, "mol/sec")
fluid1.addComponent("i-butane", 1.0, "mol/sec")
fluid1.addComponent("n-butane", 1.0, "mol/sec")
fluid1.addComponent("i-pentane", 0.4, "mol/sec")
fluid1.addComponent("n-pentane", 0.2, "mol/sec")
fluid1.addComponent("n-hexane", 0.1, "mol/sec")
fluid1.setMixingRule("classic") # classic will use binary kij 
fluid1.setMultiPhaseCheck(True) #True if more than two phases could be present

"""
Set a new fluid composition, temperature and pressure (fluid composition will 
be normalized), and calculate nubmber of phases and composition at 
equilibrium (TPflash). Thermodynamic properties (enthalpies, densities, 
entropy, etc.) are calculated using initThermoProperties(). Physical properties
 (viscosities, thermal conductivities etc.) are calculated using 
 initPhysicalProperties()
"""
fluidcomposition = [0.01, 0.02, 0.9, 0.1, 0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
fluidComposition(fluid1, fluidcomposition)
fluid1.setPressure(101.0, "bara")
fluid1.setTemperature(22.3, "C")
TPflash(fluid1)
fluid1.initThermoProperties()
fluid1.initPhysicalProperties()

"""
Print results (number of phases at equilibrium and density). 
For how to read more properties see: propertiesOfNaturalGas.py
"""
print("number of phases ", fluid1.getNumberOfPhases())
print("fluid density ", fluid1.getDensity("kg/m3"), " kg/m3")
