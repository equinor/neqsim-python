# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:19:21 2019

@author: esol
"""


from neqsim.thermo import fluid,printFrame, TPflash, checkScalePotential, calcIonComposition, printFluid, table
nitrogen = 1.0 #@param {type:"number"}
CO2 = 1.1 #@param {type:"number"}
methane = 88.3  #@param {type:"number"}
ethane = 5.0  #@param {type:"number"}
propane =  1.5 #@param {type:"number"}
water =  1.25 #@param {type:"number"}
Naplus =  0.025 #@param {type:"number"}
Clminus =  0.025 #@param {type:"number"}
Caplus =  0.00025 #@param {type:"number"}
Feplus =  0.00025 #@param {type:"number"}
OHminus =  0.00025 #@param {type:"number"}

fluid1 = fluid('Electrolyte-CPA-EoS')
fluid1.addComponent("nitrogen", nitrogen)
fluid1.addComponent("CO2", CO2)
fluid1.addComponent("methane", methane)
fluid1.addComponent("ethane", ethane)
fluid1.addComponent("propane", propane)
fluid1.addComponent("water", water,"kg/sec")
fluid1.addComponent("Na+", Naplus,"mol/sec")
fluid1.addComponent("Cl-", Clminus,"mol/sec")
fluid1.addComponent("Ca++", Caplus,"mol/sec")
fluid1.addComponent("Fe++", Feplus,"mol/sec")
fluid1.addComponent("OH-", OHminus,"mol/sec")
fluid1.chemicalReactionInit()
fluid1.setMixingRule(10)


TPflash(fluid1)
ionCompResults = calcIonComposition(fluid1)
scaleResults = checkScalePotential(fluid1)

print("pH of water ",fluid1.getPhase("aqueous").getpH())

import pandas
printFrame(fluid1)
print(pandas.DataFrame(ionCompResults))
print(pandas.DataFrame(scaleResults))

fluid1.display()