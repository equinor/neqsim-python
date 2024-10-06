# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.process import clearProcess, pump, runProcess, stream
from neqsim.thermo import fluid

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.addComponent("n-nonane", 1.0)
fluid1.setMixingRule(2)
fluid1.init(0)

fluid1.setTemperature(28.15, "C")
fluid1.setPressure(1.0, "bara")
fluid1.setTotalFlowRate(135.0, "kg/hr")
# demonstration of setting up a simple process calculation

clearProcess()
stream1 = stream("stream 1", fluid1)
pump1 = pump("pump 1", stream1, 11.0)
runProcess()

print("temperature out of pump ", pump1.getOutStream().getTemperature() - 273.15, " °C")
print("pump power ", pump1.getPower() / 1e3, " kW")
