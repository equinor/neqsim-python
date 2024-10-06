# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim import methods
from neqsim.process import clearProcess, expander, runProcess, separator, stream
from neqsim.thermo import fluid

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
stream1 = stream('stream 1', fluid1)
expander1 = expander('expander 1', stream1, 40.0)
separator1 = separator('sep 1', expander1.getOutStream())
runProcess()

print(
    "temperature in separator",
    expander1.getOutStream().getTemperature() - 273.15,
    " °C",
)
print("expander power ", expander1.getPower() / 1e6, " MW")

separator1.displayResult()
methods(expander1)
