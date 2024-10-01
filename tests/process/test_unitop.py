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
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.inputstream = None
        self.outputstream = None

    def setInputStream(self, stream):
        self.inputstream = stream
        self.outputstream = stream.clone()

    def getOutputStream(self):
        return self.outputstream

    @JOverride
    def run(self, id):
        print("here2")
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

    stream1 = jNeqSim.processSimulation.processEquipment.stream.Stream('stream 1', fluid1)
    stream1.setFlowRate(30000, "kg/hr")

    uop = ExampleCompressor(name='compressor 1')
    uop.setName("example operation 1")
    uop.setInputStream(stream1)

    stream2 = jNeqSim.processSimulation.processEquipment.stream.Stream('stream2',
        uop.getOutputStream()
    )

    oilprocess = jNeqSim.processSimulation.processSystem.ProcessSystem()
    oilprocess.add(stream1)
    oilprocess.add(uop)
    oilprocess.add(stream2)

    oilprocess.run()

    assert stream2.getPressure() == 2 * stream1.getPressure()
