from neqsim.process.measurement import measurement
from neqsim.process.processTools import (
    pump,
    stream,
    clearProcess,
    runProcess,
    pumpChart,
)
from neqsim.thermo import fluid
from jneqsim import neqsim
from jpype import JImplements, JOverride


class ExampleMeasurement(measurement):
    def __init__(self):
        super().__init__()
        self.name = ""

    def setInputStream(self, stream):
        self.inputstream = stream
        self.outputstream = stream.clone()

    def getMeasuredValue(self):
        return self.inputstream.getPressure("psia")


def test_addPythonUnitOp():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(30.0, "C")
    fluid1.setPressure(1.0, "bara")
    fluid1.addComponent("n-pentane", 1.0, "kg/sec")
    fluid1.addComponent("n-hexane", 1.0, "kg/sec")
    fluid1.setMixingRule(2)

    stream1 = neqsim.processsimulation.processequipment.stream.Stream(
        "stream1", fluid1
    )
    stream1.setFlowRate(30000, "kg/hr")

    meas1 = ExampleMeasurement()
    meas1.setName("example measurement 1")
    meas1.setInputStream(stream1)

    oilprocess = neqsim.processsimulation.processsystem.ProcessSystem()
    oilprocess.add(stream1)
    oilprocess.add(meas1)
    oilprocess.run()

    assert stream1.getPressure("psia") == meas1.getMeasuredValue()
