# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.thermo import fluid
from neqsim import methods
from neqsim.process import clearProcess, expander, stream, valve, separator, compressor, runProcess, viewProcess, heater

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.addComponent("nitrogen", 1.0)
fluid1.addComponent("CO2", 2.0)
fluid1.addComponent("methane", 85.0)
fluid1.addComponent("ethane", 5.0)
fluid1.addComponent("propane", 3.0)
fluid1.addComponent("i-butane", 2.0)
fluid1.addComponent("n-butane", 2.0)
fluid1.setMixingRule(2)

fluid1.setTemperature(28.15, "C")
fluid1.setPressure(80.0, "bara")
fluid1.setTotalFlowRate(10.0, "MSm3/day")


# demonstration of setting up a simple process calculation
clearProcess()
stream1 = stream(fluid1)
expander1 = expander(stream1, 40.0)
separartor1 = separator(expander1.getOutStream())
runProcess()

print("temperature in separartor", expander1.getOutStream().getTemperature()-273.15, " °C")
print("expander power ", expander1.getPower()/1e6, " MW")

separartor1.displayResult()
methods(expander1)

