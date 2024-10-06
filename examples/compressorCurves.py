# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:01:47 2019

@author: esol
"""
from neqsim.process import (
    clearProcess,
    compressor,
    compressorChart,
    compressorStoneWallCurve,
    compressorSurgeCurve,
    runProcess,
    stream,
)
from neqsim.thermo import fluid

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
# fluid1.addComponent("nitrogen", 1.0)
# fluid1.addComponent("CO2", 2.0)
fluid1.addComponent("methane", 91.0)
fluid1.addComponent("ethane", 5.0)
fluid1.addComponent("propane", 3.0)
fluid1.addComponent("i-butane", 2.0)
fluid1.addComponent("n-butane", 2.0)
fluid1.setMixingRule(2)

fluid1.setTemperature(25.0, "C")
fluid1.setPressure(50.0, "bara")
fluid1.setTotalFlowRate(0.635, "MSm3/day")
# demonstration of setting up a simple process calculation

clearProcess()
stream1 = stream('stream 1', fluid1)
compressor2 = compressor('compressor 1', stream1, 51.0)


MW = 28.01
inlepPres = 100.0
inletTemp = 26.2
Zinlet = 0.89
curveConditions = [MW, inlepPres, inletTemp, Zinlet]

speed = [1000.0, 2000.0, 3000.0, 4000.0]
flow = [
    [453.2, 600.0, 750.0, 800.0],
    [453.2, 600.0, 750.0, 800.0],
    [453.2, 600.0, 750.0, 800.0],
    [453.2, 600.0, 750.0, 800.0],
]
head = [
    [10000.0, 9000.0, 8000.0, 7500.0],
    [10000.0, 9000.0, 8000.0, 7500.0],
    [10000.0, 9000.0, 8000.0, 7500.0],
    [10000.0, 9000.0, 8000.0, 7500.0],
]
polyEff = [
    [90.0, 91.0, 89.0, 88.0],
    [90.0, 91.0, 89.0, 88.0],
    [90.0, 91.0, 89.0, 88.1],
    [90.0, 91.0, 89.0, 88.1],
]
compressorChart(compressor2, curveConditions, speed, flow, head, polyEff)


surgeFlow = [453.2, 600.0, 750.0, 800.0]
surgeHead = [6000.0, 7000.0, 8000.0, 10000.0]
compressorSurgeCurve(compressor2, curveConditions, surgeFlow, surgeHead)

stoneWallFlow = [923.2, 950.0, 980.0, 1000.0]
stoneWallHead = [6000.0, 7000.0, 8000.0, 10000.0]
compressorStoneWallCurve(compressor2, curveConditions, stoneWallFlow, stoneWallHead)


compressor2.setUsePolytropicCalc(True)
compressor2.getAntiSurge().isActive()
compressor2.setSpeed(2050)

runProcess()
print("inlet flow ", stream1.getThermoSystem().getFlowRate("m3/hr"), " m3/hr")
print("pressure out ", compressor2.getOutStream().getPressure(), " bara")
print("compressor2 power ", compressor2.getPower() / 1.0e6, " MW")
print(
    "temperature out of compressor2 ",
    compressor2.getOutStream().getTemperature() - 273.15,
    " °C",
)
