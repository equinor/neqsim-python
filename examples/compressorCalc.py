# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:52:50 2020

@author: ESOL
"""
import pandas as pd
from neqsim.process import clearProcess, compressor, compressorChart, runProcess, stream
from neqsim.thermo import fluid, fluid_df

# Create a gas-condensate fluid
naturalgas = {
    "ComponentName": [
        "nitrogen",
        "CO2",
        "methane",
        "ethane",
        "propane",
        "i-butane",
        "n-butane",
        "i-pentane",
        "n-pentane",
        "n-hexane",
    ],
    "MolarComposition[-]": [
        0.633,
        1.371,
        85.697,
        6.914,
        3.086,
        0.475,
        0.886,
        0.242,
        0.254,
        0.016,
    ],
}
naturalgasFluid = fluid_df(pd.DataFrame(naturalgas))


# Setting up a process with an inpu stream and a compressor
clearProcess()
stream1 = stream('stream 1', naturalgasFluid)
compressor2 = compressor('compressor 1', stream1)


# setting up the compressor performance
MW = 19.7
inlepPres = 60.0
inletTemp = 22.9
Zinlet = 0.851
curveConditions = [MW, inlepPres, inletTemp, Zinlet]

speed = [11533.0]
flow = [[4327.9175, 4998.517, 5505.8851, 6027.6167, 6506.9064, 6908.2832]]
polytropicheadmeter = [
    [18882.3055, 18235.1912, 17531.6259, 16489.7195, 15037.1474, 13618.7919]
]
polytropicefficiency = [[72.54, 74.44, 74.5, 74.66, 72.66, 70.19]]

compressorChart(
    compressor2, curveConditions, speed, flow, polytropicheadmeter, polytropicefficiency
)
compressor2.getCompressorChart().setHeadUnit("meter")
compressor2.setUsePolytropicCalc(True)


# Method 1
# Run calculation with given flow, T and P at inlet. USe compressor curves for calculations.
stream1.getFluid().setTotalFlowRate(7.1854785, "MSm3/day")
stream1.setTemperature(25.0, "C")
stream1.setPressure(50.0, "bara")
compressor2.setSpeed(11015)
runProcess()
# Read results
polytropicHead = compressor2.getPolytropicHead()

flowRate = stream1.getThermoSystem().getFlowRate("m3/hr")
print("Method 1. Run calculation with given flow, T and P at inlet ")
print("pressure out ", compressor2.getOutletPressure())
print("temperature out ", compressor2.getOutTemperature() - 273.15, " C")
print("polytropic head ", compressor2.getPolytropicHead(), " meter")
print("polytropic efficiency ", compressor2.getPolytropicEfficiency())
print(
    "compressor speed ",
    compressor2.getCompressorChart().getSpeed(flowRate, polytropicHead),
)
print("power ", compressor2.getPower() / 1e6, " MW")


# Method 2
# Run calculation with given flow, T and P at inlet and T and P out (compressor curves are only used for reading compressor speed)
stream1.getFluid().setTotalFlowRate(7.1854785, "MSm3/day")
stream1.setTemperature(25.0, "C")
stream1.setPressure(50.0, "bara")
compressor2.setOutletPressure(160.0)
compressor2.setOutTemperature(130.57 + 273.15)
runProcess()
# Read results
polytropicHead = compressor2.getPolytropicHead()
flowRate = stream1.getThermoSystem().getFlowRate("m3/hr")
print(
    "Method 2. Run calculation with given flow, T and P at inlet and P out (compressor curves are not used)"
)
print("pressure out ", compressor2.getOutletPressure())
print("temperature out ", compressor2.getOutTemperature() - 273.15, " C")
print("polytropic head ", compressor2.getPolytropicHead(), " meter")
print("polytropic efficiency ", compressor2.getPolytropicEfficiency())
print(
    "compressor speed ",
    compressor2.getCompressorChart().getSpeed(flowRate, polytropicHead),
)
print("power ", compressor2.getPower() / 1e6, " MW")
