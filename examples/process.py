# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.process import (
    clearProcess,
    compressor,
    runProcess,
    separator,
    stream,
    valve,
    viewProcess,
)
from neqsim.thermo import fluid

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
stream1 = stream('stream 1', fluid1)
inletValve = valve('valve 1', stream1, 50.0)  # add valve and set outlet pressure
inletSeparator = separator('sep 1', inletValve.getOutStream())
oilValve = valve('valv2', inletSeparator.getLiquidOutStream(), 1.0)
# add compressor and set out pressure
compressor1 = compressor('comp1', inletSeparator.getGasOutStream(), 100.0)

# sensoir to read from Omnia
# temperatureTranmitter1 = temperatureTransmitter(stream1, "PT20232")
# pressureTranmitter1 = pressureTransmitter(stream1,"TIP2030I")

# signals to calculate
# VTemperatureTransmitter1 = VtemperatureTransmitter(inletValve.getOutStream(),"VT20314")


runProcess()
#viewProcess()

print("compressor power ", compressor1.getPower())
