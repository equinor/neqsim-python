# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:13:11 2020

@author: ESOL
"""

from neqsim.process import (
    clearProcess,
    compressor,
    cooler,
    heater,
    runProcess,
    stream,
    valve,
)
from neqsim.thermo.thermoTools import *

fluid_1 = fluid("srk")
fluid_1.addComponent("propane", 1.0)

fluid_1.setPressure(15.0, "bara")
fluid_1.setTemperature(30.0, "C")
fluid_1.setTotalFlowRate(1000.0, "kg/hr")

clearProcess()
stream_1 = stream('stream1', fluid_1)
stream_1.setSpecification("bubT")

JTvalve = valve('valve 1', stream_1, 1.0)

cooler_1 = cooler('cooler 1', JTvalve.getOutStream())
cooler_1.setSpecification("out stream")

stream_2 = stream('stream2', cooler_1.getOutStream())
stream_2.setSpecification("dewP")

cooler_1.setOutStream(stream_2)
JTvalve.setOutletPressure(stream_2.getPressure())

compressor_1 = compressor('comp2', stream_2, 10.0)
compressor_1.setSpecification("out stream")
compressor_1.setOutletPressure(stream_1.getPressure())

heater = heater('heat22', compressor_1.getOutStream())
heater.setSpecification("out stream")
heater.setOutStream(stream_1)

runProcess()

print("Compressor power ", compressor_1.getTotalWork() / 1e3, " kW")
print("Cooling duty ", cooler_1.getDuty() / 1e3, " kW")
print("Heating duty ", heater.getDuty() / 1e3, " kW")
