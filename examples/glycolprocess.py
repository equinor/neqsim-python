# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 19:39:10 2020

@author: esol
"""

from neqsim.process import (
    clearProcess,
    compressor,
    heater,
    mixer,
    pump,
    recycle,
    runProcess,
    separator,
    stream,
    valve,
    viewProcess,
)
from neqsim.thermo import (
    TPflash,
    addOilFractions,
    createfluid,
    createfluid2,
    dataFrame,
    fluid,
    fluidComposition,
    fluidcreator,
    phaseenvelope,
    printFrame,
)

# Start by creating a fluid in neqsim uing a predifined fluid (dry gas, rich gas, light oil, black oil)
# Set temperature and pressure and do a TPflash. Show results in a dataframe.


feedPressure = 50.0
feedTemperature = 30.0
fluid1 = fluid("cpa")  # create a fluid using the SRK-EoS
fluid1.addComponent("CO2", 1e-10)
fluid1.addComponent("methane", 1e-10)
fluid1.addComponent("ethane", 1e-10)
fluid1.addComponent("propane", 1e-10)
fluid1.addComponent("water", 1e-10)
fluid1.addComponent("TEG", 1e-10)
fluid1.setMixingRule(10)
fluid1.setMultiPhaseCheck(True)
fluidcomposition = [0.031, 0.9297, 0.0258, 0.0135, 6.48413454028242e-002, 1.0e-15]
fluidComposition(fluid1, fluidcomposition)
fluid1.setTemperature(feedTemperature, "C")
fluid1.setPressure(feedPressure, "bara")
fluid1.setTotalFlowRate(5.0, "MSm3/day")

fluid2 = fluid("cpa")
fluid2.addComponent("CO2", 1.0e-10)
fluid2.addComponent("methane", 1.0e-10)
fluid2.addComponent("ethane", 1.0e-10)
fluid2.addComponent("propane", 1.0e-10)
fluid2.addComponent("water", 1.0, "kg/sec")
fluid2.addComponent("TEG", 99.0, "kg/sec")
fluid2.setMixingRule(10)
fluid2.setMultiPhaseCheck(True)
fluid2.setTemperature(313.15, "K")
fluid2.setPressure(75.0, "bara")
fluid2.setTotalFlowRate(10625.0, "kg/hr")

# demonstration of setting up a simple process calculation
clearProcess()
stream1 = stream("stream 1", fluid1)
glycolstream = stream("stream 2", fluid2)
separator1 = separator("sep 1", stream1)
compressor1 = compressor("comp 1", separator1.getGasOutStream(), 75.0)

heater1 = heater("heater 1", compressor1.getOutStream())
heater1.setOutTemperature(313.0)

mixer1 = mixer("mixer 1")
mixer1.addStream(heater1.getOutStream())
mixer1.addStream(glycolstream)

scrubberLP = separator("sep1", mixer1.getOutStream())
valve1 = valve("valve1", scrubberLP.getLiquidOutStream(), 10.0)
flashDrum = separator("sep2", valve1.getOutStream())
heater1 = heater("heat2", flashDrum.getLiquidOutStream())
heater1.setOutTemperature(273.15 + 195.0)
stripper = separator("sep4", heater1.getOutStream())

cooler1 = heater("cooler5", stripper.getLiquidOutStream())
cooler1.setOutTemperature(313.0)

pump1 = pump("pump5", cooler1.getOutStream(), 75.0)


runProcess()
print("1")

runProcess()
print("2")

runProcess()
print("3")
