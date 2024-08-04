from neqsim.process.unitop import unitop
from neqsim.process.processTools import (
    pump,
    stream,
    clearProcess,
    runProcess,
    pumpChart,
)
from neqsim.thermo import fluid
from neqsim import jNeqSim
from jpype import JImplements, JOverride


class ExampleCompressor(unitop):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.inputstream = None
        self.outputstream = None

    def setInputStream(self, stream):
        self.inputstream = stream
        self.outputstream = stream.clone()

    def getOutputStream(self):
        return self.outputstream

    @JOverride
    def run(self):
        fluid2 = self.inputstream.getFluid().clone()
        fluid2.setPressure(fluid2.getPressure() * 2.0)
        self.outputstream.setFluid(fluid2)
        self.outputstream.run()


def test_addPythonUnitOp():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(30.0, "C")
    fluid1.setPressure(1.0, "bara")
    fluid1.addComponent("n-pentane", 1.0, "kg/sec")
    fluid1.addComponent("n-hexane", 1.0, "kg/sec")
    fluid1.setMixingRule(2)

    stream1 = jNeqSim.processSimulation.processEquipment.stream.Stream(fluid1)
    stream1.setFlowRate(30000, "kg/hr")
    stream1.run()

    uop = ExampleCompressor()
    uop.setName("example operation 1")
    uop.setInputStream(stream1)
    uop.run()

    stream2 = jNeqSim.processSimulation.processEquipment.stream.Stream(
        uop.getOutputStream()
    )
    stream2.run()

    assert stream2.getPressure() == 2 * stream1.getPressure()

    oilprocess = jNeqSim.processSimulation.processSystem.ProcessSystem()
    oilprocess.add(stream1)
    oilprocess.add(uop)
    oilprocess.add(stream2)

    oilprocess.run()

    assert stream2.getPressure() == 2 * stream1.getPressure()
