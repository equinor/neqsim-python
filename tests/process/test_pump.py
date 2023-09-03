from neqsim.process.processTools import (pump, stream, clearProcess, runProcess, pumpChart)
from neqsim.thermo import (fluid, printFrame, fluid_df)
from numpy import isnan
from pytest import approx
from jpype.types import *
from neqsim import jNeqSim

def test_pump():
    clearProcess()
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(30.0, "C")
    fluid1.setPressure(1.0, "bara")
    fluid1.addComponent("n-pentane", 1.0, "kg/sec")
    fluid1.addComponent("n-hexane", 1.0, "kg/sec")
    fluid1.setMixingRule(2)
    stream1 = stream(fluid1)
    stream1.setFlowRate(30000, "kg/hr");

    curveConditions = []
    speed = [500]
    flow = [[27.1285, 31.0375, 36.2288, 41.4503, 45.2768, 49.7728, 52.0329, 56.0331],]
    head = [[80.0375, 78.8934, 76.2142, 71.8678, 67.0062, 60.6061, 53.0499, 39.728],]
    polyEff = [[77.2, 79.4, 80.7, 80.5, 79.2, 75.4, 69.6, 58.7],]

    pump1 = pump(stream1)
    pump1.setName('pump1')
    pumpChart(pump1, curveConditions, speed, flow, head, polyEff)
    pump1.setSpeed(500)
    pump1.getPumpChart().setHeadUnit("meter")
    runProcess()
    pump1.run()
    assert pump1.getOutletPressure() == 7.274237081101573