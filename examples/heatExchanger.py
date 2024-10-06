# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim import methods
from neqsim.process import clearProcess, heatExchanger, runProcess, stream
from neqsim.thermo import fluid

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-Eo
fluid1.addComponent("CO2", 2.0)
fluid1.addComponent("methane", 85.0)
fluid1.addComponent("ethane", 5.0)
fluid1.addComponent("propane", 3.0)
fluid1.addComponent("i-butane", 2.0)
fluid1.addComponent("n-butane", 2.0)
fluid1.setMixingRule(2)
fluid1.setTemperature(88.15, "C")
fluid1.setPressure(50.0, "bara")
fluid1.setTotalFlowRate(10.0, "MSm3/day")

fluid2 = fluid("srk")
fluid2.addComponent("water", 0.1)
fluid2.setMixingRule(2)
fluid2.setTemperature(28.15, "C")
fluid2.setPressure(3.0, "bara")
fluid2.setTotalFlowRate(2700.0, "Sm3/hr")


# demonstration of setting up a simple process calculation
clearProcess()
stream1 = stream("stream1", fluid1)
stream2 = stream("stream2", fluid2)

heatExchanger1 = heatExchanger("exchanger1", stream1, stream2)
runProcess()

# heatExchanger1.displayResult()

temp1 = heatExchanger1.getOutStream(0).getTemperature() - 273.15
temp2 = heatExchanger1.getOutStream(1).getTemperature() - 273.15
