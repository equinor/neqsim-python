# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:56:43 2019

@author: esol
"""

from neqsim.thermo import fluid, hydt,addfluids

pressure = 150.0

nitrogen = 1.5 
CO2 = 2.5
methane = 95.0
ethane = 5.0  
propane =  2.5 
ibutane =  1.25
nbutane =  1.25
water =  10.25

fluid1 = fluid('cpa')
fluid1.addComponent("nitrogen", nitrogen, 'mol/sec')
fluid1.addComponent("CO2", CO2, 'mol/sec')
fluid1.addComponent("methane", methane, 'mol/sec')
fluid1.addComponent("ethane", ethane, 'mol/sec')
fluid1.addComponent("propane", propane, 'mol/sec')
fluid1.addComponent("i-butane", ibutane, 'mol/sec')
fluid1.addComponent("n-butane", nbutane, 'mol/sec')
fluid1.addComponent("water", water, 'mol/sec')
fluid1.setMixingRule(10);


fluid1.setPressure(pressure, 'bara')


fluid2 = fluid('cpa')
fluid2.addComponent("oxygen", nitrogen, 'mol/sec')
fluid2.setMixingRule(10);

fluid3 = addfluids(fluid1,fluid2)
hydt(fluid3)
print("Hydrate equilibrium temperature ", fluid3.getTemperature()-273.15, " C")