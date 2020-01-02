# -*- coding: utf-8 -*-
"""
The current python script demonstrates simple ways of creating fluids in neqsim
@author: esol
"""
from neqsim.thermo import fluid, addOilFractions, printFrame, dataFrame, fluidcreator,createfluid,createfluid2, TPflash, phaseenvelope

# Start by creating a fluid in neqsim uing a predifined fluid (dry gas, rich gas, light oil, black oil)
#Set temperature and pressure and do a TPflash. Show results in a dataframe.
fluidcreator.setHasWater(False)
fluid1 = createfluid('dry gas')
fluid1.setPressure(10.0, "bara")
fluid1.setTemperature(22.3, "C")
TPflash(fluid1)
print('results of TPflash for fluid 1')
printFrame(fluid1)

#Calculate and display the phase envelope of various fluid types
fluid1 = createfluid('black oil')
print('phase envelope for black oil')
phaseenvelope(fluid1, True)

fluid2 = createfluid('dry gas')
print('phase envelope for fluid 2')
phaseenvelope(fluid2, True)

fluid3 = createfluid('rich gas')
print('phase envelope for fluid 3')
phaseenvelope(fluid3, True)

#Demonstration of a simple way of generating a fluid when component names and comosition are given as list
names = ['methane', 'ethane']
molefractions = [0.5, 0.5]
fluid4 = createfluid2(names, molefractions, "mol/sec")
print('phase envelope for fluid 4')
phaseenvelope(fluid4, True)

#Demonstration of simple way to adde characterized oil fractions to a fluid (a new fluid will be created)
charNames = ["C10-C15", "C16-C19", "C20-C30", "C31-C50", "C51-C80"]
charFlowrate = [0.2, 0.1, 0.1, 0.05, 0.01]
molarMass = [0.20, 0.25, 0.3, 0.36, 0.4]
density = [700.0e-3, 750.0e-3, 810.0e-3, 880.0e-3, 920.0e-3]
fluid5 = addOilFractions(fluid4, charNames,charFlowrate,molarMass,  density);
print('phase envelope for fluid 5')
phaseenvelope(fluid5, True)
fluid5.setPressure(10.0, "bara")
fluid5.setTemperature(22.3, "C")
TPflash(fluid5)
print('results of TPflash for fluid 5')
printFrame(fluid5)