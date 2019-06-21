from neqsim import java_gateway

neqsim = java_gateway.jvm.neqsim

processoperations = neqsim.processSimulation.processSystem.ProcessSystem()


def stream(thermoSystem, name="stream ?", t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = neqsim.processSimulation.processEquipment.stream.Stream(thermoSystem)
    stream.setName(name)
    processoperations.add(stream)
    return stream


def neqstream(thermoSystem, name="stream ?", t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = neqsim.processSimulation.processEquipment.stream.NeqStream(thermoSystem)
    stream.setName(name)
    processoperations.add(stream)
    return stream


def separator(teststream, name="separator ?"):
    separator = neqsim.processSimulation.processEquipment.separator.Separator(teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator


def valve(teststream, p, name="valve ?"):
    valve = neqsim.processSimulation.processEquipment.valve.ThrottlingValve(teststream)
    valve.setOutletPressure(p)
    valve.setName(name)
    processoperations.add(valve)
    return valve


def compressor(teststream, p, name="compressor ?"):
    compressor = neqsim.processSimulation.processEquipment.compressor.Compressor(teststream)
    compressor.setOutletPressure(p)
    compressor.setName(name)
    processoperations.add(compressor)
    return compressor


def expander(teststream, p, name="expander ?"):
    expander = neqsim.processSimulation.processEquipment.expander.Expander(teststream)
    expander.setOutletPressure(p)
    expander.setName(name)
    processoperations.add(expander)
    return expander


def mixer(name=""):
    mixer = neqsim.processSimulation.processEquipment.mixer.StaticMixer()
    mixer.setName(name)
    processoperations.add(mixer)
    return mixer


def heater(teststream, name=""):
    heater = neqsim.processSimulation.processEquipment.heatExchanger.Heater(teststream)
    heater.setName(name)
    processoperations.add(heater)
    return heater

def cooler(teststream, name=""):
    cooler = neqsim.processSimulation.processEquipment.heatExchanger.Cooler(teststream)
    cooler.setName(name)
    processoperations.add(cooler)
    return cooler

def heatExchanger(stream1, stream2, name=""):
    heater = neqsim.processSimulation.processEquipment.heatExchanger.HeatExchanger(stream1, stream2)
    heater.setName(name)
    processoperations.add(heater)
    return heater


def distillationColumn(trays=5, name="destColumn"):
    distillationColumn = neqsim.processSimulation.processEquipment.distillation.DistillationColumn(trays, 1, 1)
    distillationColumn.setName(name)
    processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(teststream, name=""):
    neqheater = neqsim.processSimulation.processEquipment.heatExchanger.NeqHeater(teststream)
    neqheater.setName(name)
    processoperations.add(neqheater)
    return neqheater


def splitter(teststream, numb, name=""):
    splitter = neqsim.processSimulation.processEquipment.splitter.Splitter(name, teststream, numb)
    processoperations.add(splitter)
    return splitter


def twophasepipe(teststream, position, diameter, height, outTemp, rough):
    pipe = neqsim.processSimulation.processEquipment.pipeline.TwoPhasePipeLine(teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    pipe.setInitialFlowPattern("annular")
    numberOfLegs = len(position) - 1
    numberOfNodesInLeg = 60
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(position)
    pipe.setHeightProfile(height)
    pipe.setPipeDiameters(diameter)
    pipe.setPipeWallRoughness(rough)
    pipe.setOuterTemperatures(outTemp)
    pipe.setEquilibriumMassTransfer(0)
    pipe.setEquilibriumHeatTransfer(1)
    processoperations.add(pipe)
    return pipe


def pipeline(teststream, position, diameter, height, outTemp, rough):
    pipe = neqsim.processSimulation.processEquipment.pipeline.OnePhasePipeLine(teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    numberOfNodesInLeg = 100
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(position)
    pipe.setHeightProfile(height)
    pipe.setPipeDiameters(diameter)
    pipe.setPipeWallRoughness(rough)
    pipe.setOuterTemperatures(outTemp)
    processoperations.add(pipe)
    return pipe


def clear():
    processoperations.clearAll


def run():
    processoperations.run()


def clearProcess():
    processoperations.clearAll


def runProcess():
    processoperations.run()


def runtrans():
    processoperations.runTransient()


def view():
    processoperations.displayResult()


def viewProcess():
    processoperations.displayResult()
