# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.process import (
    clearProcess,
    compressor,
    heater,
    runProcess,
    separator,
    stream,
    valve,
    viewProcess,
)
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
fluid1.setPressure(30.0, "bara")
fluid1.setTotalFlowRate(10.0, "MSm3/day")
# demonstration of setting up a simple process calculation

clearProcess()
stream1 = stream("stream 1", fluid1)
compressor1 = compressor(
    "compressor 1", stream1, 60.0
)  # add compressor and set out pressure
compressor1.setIsentropicEfficiency(0.8)
cooler1 = heater("coller 1", compressor1.getOutStream())
cooler1.setOutTemperature(303.0)
compressor2 = compressor("compressor 2", cooler1.getOutStream(), 120.0)
compressor2.setIsentropicEfficiency(0.77)

runProcess()

print("compressor1 power ", compressor1.getPower() / 1e6, " MW")
print("compressor2 power ", compressor2.getPower() / 1e6, " MW")

print(
    "temperature out of compressor1 ",
    compressor1.getOutStream().getTemperature() - 273.15,
    " °C",
)
print(
    "temperature out of compressor2 ",
    compressor2.getOutStream().getTemperature() - 273.15,
    " °C",
)
