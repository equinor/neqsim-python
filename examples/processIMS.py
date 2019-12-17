# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:28:01 2019

@author: esol
"""
from neqsim import methods
from neqsim.thermo import fluid
from neqsim.process import clearProcess, stream, valve, separator, compressor, runProcess, viewProcess, heater, mixer, recycle

feedPressure = 30.0
MPpressure = 10.0
LPpressure = 2.1

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.addComponent("nitrogen", 1.0)
fluid1.addComponent("CO2", 2.0)
fluid1.addComponent("methane", 85.0)
fluid1.addComponent("ethane", 5.0)
fluid1.addComponent("propane", 3.0)
fluid1.addComponent("i-butane", 2.0)
fluid1.addComponent("n-butane", 2.0)
fluid1.addComponent("n-nonane", 11.1)
fluid1.setMixingRule(2)
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(feedPressure, "bara")
fluid1.setTotalFlowRate(10.0, "MSm3/day")
# demonstration of setting up a simple process calculation
clearProcess()
stream1 = stream(fluid1)
methods(stream1)