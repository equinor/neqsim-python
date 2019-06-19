# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.thermo import fluid
from neqsim.process import clearProcess, stream, valve, separator, compressor, runProcess, viewProcess

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(100.0, "bara")
fluid1.addComponent("nitrogen", 10.0, "mol/sec")
fluid1.addComponent("n-heptane", 5.0, "mol/sec")
fluid1.addComponent("water", 1.0, "kg/sec")
fluid1.setMixingRule(2)
fluid1.setMultiPhaseCheck(True)

# demonstration of setting up a simple process calculation
clearProcess()
stream1 = stream(fluid1)
inletValve = valve(stream1, 50.0)  # add valve and set outlet pressure
inletSeparator = separator(inletValve.getOutStream())
oilValve = valve(inletSeparator.getLiquidOutStream(), 1.0)
compressor1 = compressor(inletSeparator.getGasOutStream(), 100.0)  # add compressor and set out pressure

runProcess()
viewProcess()
