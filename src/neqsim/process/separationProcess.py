# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:49:28 2019

@author: esol
"""
from neqsim.thermo import fluid
from neqsim.process import clearProcess, stream, valve, separator, compressor, runProcess, viewProcess, heater




fluid1 = fluid('srk')
fluid1.addComponent('water', 2.7)
fluid1.addComponent('nitrogen', 0.7)
fluid1.addComponent('CO2', 2.1)
fluid1.addComponent('methane', 70.0)
fluid1.addComponent('ethane', 10.0)
fluid1.addComponent('propane', 5.0)
fluid1.addComponent('i-butane', 3.0)
fluid1.addComponent('n-butane', 2.0)
fluid1.addComponent('i-pentane', 1.0)
fluid1.addComponent('n-pentane', 1.0)
fluid1.addTBPfraction('C6', 1.49985, 86.3 / 1000.0, 0.7432) #adding oil component mol/ molar mass (kg/mol) / relative density (gr/gr)
fluid1.addTBPfraction('C7', 0.49985, 103.3 / 1000.0, 0.76432)
fluid1.addTBPfraction('C8', 0.39985, 125.0 / 1000.0, 0.78432)
fluid1.addTBPfraction('C9', 0.49985, 145.0 / 1000.0, 0.79432)
fluid1.addTBPfraction('C10', 0.149985, 165.0 / 1000.0, 0.81)
fluid1.setMixingRule('classic')
fluid1.setMultiPhaseCheck(True)

fluid1.setTemperature(55.0, 'C')
fluid1.setPressure(55.0, 'bara')

clearProcess()
feedStream = stream(fluid1,"feed fluid")

separator1 = separator(feedStream)
oilstream1 = separator1.getLiquidOutStream()
valve1 = valve(oilstream1,10.0, 'valv1')

runProcess()
valve1.displayResult()