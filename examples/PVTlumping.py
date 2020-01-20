# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 22:54:57 2020

@author: esol
"""

import neqsim
from neqsim.thermo.thermoTools import *

fluid1 = fluid('srk',290.0, 11.0);

fluid1.getCharacterization().setLumpingModel("PVTlumpingModel")
fluid1.getCharacterization().getLumpingModel().setNumberOfPseudoComponents(12)
fluid1.addComponent("water", 0.2);
fluid1.addComponent("nitrogen", 0.002);
fluid1.addComponent("CO2", 0.005);
fluid1.addComponent("methane", 0.4);
fluid1.addComponent("ethane", 0.03);
fluid1.addComponent("propane", 0.01);
fluid1.addComponent("n-butane", 0.002);
fluid1.addComponent("i-butane", 0.006);
fluid1.addComponent("n-pentane", 0.004);
fluid1.addComponent("i-pentane", 0.005);

fluid1.addTBPfraction("C6", 0.004, 85.0253 / 1000.0, 0.667229);
fluid1.addTBPfraction("C7", 0.001, 90.3717 / 1000.0, 0.7463691);
fluid1.addTBPfraction("C8", 0.001, 102.46950 / 1000.0, 0.7709114);
fluid1.addTBPfraction("C9", 0.001, 115.6 / 1000.0, 0.7901);
fluid1.addPlusFraction("C10", 0.02, 225.5046 / 1000.0, 0.8411014);

fluid1.getCharacterization().characterisePlusFraction();
fluid1.setMixingRule(2);
fluid1.setMultiPhaseCheck(True)
TPflash(fluid1);
printFrame(fluid1)

molaFrac = [0.1, 0.01, 0.01, 0.6, 0.1, 0.02, 0.02, 0.01, 0.001, 0.002, 0.01, 0.001, 0.001,0.001, 0.4];
fluidCompositionPlus(fluid1, molaFrac);

TPflash(fluid1);
printFrame(fluid1)