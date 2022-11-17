import jpype
import jpype.imports
from jpype.types import *
from neqsim.neqsimpython import jNeqSim

processoperations = jNeqSim.processSimulation.processSystem.ProcessSystem()

def newProcess():
    """
    Create a new process object
    """
    global processoperations
    processoperations = jNeqSim.processSimulation.processSystem.ProcessSystem()


def stream(thermoSystem, name="stream ?", t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jNeqSim.processSimulation.processEquipment.stream.Stream(
        thermoSystem)
    stream.setName(name)
    processoperations.add(stream)
    return stream

def virtualstream(streamIn, name="stream ?"):
    stream = jNeqSim.processSimulation.processEquipment.stream.VirtualStream(name, 
        streamIn)
    processoperations.add(stream)
    return stream

def neqstream(thermoSystem, name="stream ?", t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jNeqSim.processSimulation.processEquipment.stream.NeqStream(
        thermoSystem)
    stream.setName(name)
    processoperations.add(stream)
    return stream


def recycle(teststream, name="recycle ?"):
    recycle1 = jNeqSim.processSimulation.processEquipment.util.Recycle()
    recycle1.addStream(teststream)
    processoperations.add(recycle1)
    return recycle1


def saturator(teststream, name="water saturator"):
    streamsaturator = jNeqSim.processSimulation.processEquipment.util.StreamSaturatorUtil(
        teststream)
    processoperations.add(streamsaturator)
    return streamsaturator


def glycoldehydrationlmodule(teststream, name="TEG process"):
    dehydrationlmodule = jNeqSim.processSimulation.processSystem.processModules.GlycolDehydrationlModule()
    dehydrationlmodule.setName(name)
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    processoperations.add(dehydrationlmodule)
    return dehydrationlmodule


def openprocess(filename):
    processoperations = jNeqSim.processSimulation.processSystem.ProcessSystem.open(
        filename)
    return processoperations


def separator(teststream, name="separator ?"):
    separator = jNeqSim.processSimulation.processEquipment.separator.Separator(
        teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator


def GORfitter(teststream, name="GOR fitter ?"):
    GORfitter1 = jNeqSim.processSimulation.processEquipment.util.GORfitter(
        name, teststream)
    GORfitter1.setName(name)
    processoperations.add(GORfitter1)
    return GORfitter1


def simpleTEGAbsorber(name="TEG absorber ?"):
    absorber = jNeqSim.processSimulation.processEquipment.absorber.SimpleTEGAbsorber()
    absorber.setName(name)
    processoperations.add(absorber)
    return absorber


def waterStripperColumn(name="water stripper ?"):
    stripper = jNeqSim.processSimulation.processEquipment.absorber.WaterStripperColumn()
    stripper.setName(name)
    processoperations.add(stripper)
    return stripper


def gasscrubber(teststream, name="scrubber ?"):
    separator = jNeqSim.processSimulation.processEquipment.separator.GasScrubber(
        teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator


def separator3phase(teststream, name="separator ?"):
    separator = jNeqSim.processSimulation.processEquipment.separator.ThreePhaseSeparator(
        teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator


def valve(teststream, p=1.0, name="valve ?"):
    valve = jNeqSim.processSimulation.processEquipment.valve.ThrottlingValve(
        teststream)
    valve.setOutletPressure(p)
    valve.setName(name)
    processoperations.add(valve)
    return valve


def recycle2(name="recycle ?"):
    recyc = jNeqSim.processSimulation.processEquipment.util.Recycle(name)
    processoperations.add(recyc)
    return recyc


def calculator(name="calculator ?"):
    calc2 = jNeqSim.processSimulation.processEquipment.util.Calculator(name)
    processoperations.add(calc2)
    return calc2


def setpoint(name1, unit1, name2, unit2):
    setp = jNeqSim.processSimulation.processEquipment.util.SetPoint(
        name1, unit1, name2, unit2)
    processoperations.add(setp)
    return setp


def filters(teststream):
    filter2 = jNeqSim.processSimulation.processEquipment.filter.Filter(
        teststream)
    processoperations.add(filter2)
    return filter2


def compressor(teststream, pres=10.0, name="compressor ?"):
    compressor = jNeqSim.processSimulation.processEquipment.compressor.Compressor(
        teststream)
    compressor.setOutletPressure(pres)
    compressor.setName(name)
    processoperations.add(compressor)
    return compressor


def compressorChart(compressor, curveConditions, speed, flow, head, polyEff):
    compressor.getCompressorChart().setCurves(JDouble[:](curveConditions), JDouble[:](
        speed), JDouble[:][:](flow), JDouble[:][:](head), JDouble[:][:](polyEff))


def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    compressor.getCompressorChart().getSurgeCurve().setCurve(
        JDouble[:](curveConditions), JDouble[:](surgeflow), JDouble[:](surgehead))


def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    compressor.getCompressorChart().getStoneWallCurve().setCurve(JDouble[:](
        curveConditions), JDouble[:](stoneWallflow), JDouble[:](stoneWallHead))


def pump(teststream, p=1.0, name="pump ?"):
    pump = jNeqSim.processSimulation.processEquipment.pump.Pump(teststream)
    pump.setOutletPressure(p)
    pump.setName(name)
    processoperations.add(pump)
    return pump


def expander(teststream, p, name="expander ?"):
    expander = jNeqSim.processSimulation.processEquipment.expander.Expander(
        teststream)
    expander.setOutletPressure(p)
    expander.setName(name)
    processoperations.add(expander)
    return expander


def mixer(name=""):
    mixer = jNeqSim.processSimulation.processEquipment.mixer.Mixer()
    mixer.setName(name)
    processoperations.add(mixer)
    return mixer


def phasemixer(name=""):
    mixer = jNeqSim.processSimulation.processEquipment.mixer.StaticPhaseMixer()
    mixer.setName(name)
    processoperations.add(mixer)
    return mixer


def nequnit(teststream, equipment="pipeline", flowpattern="stratified", numberOfNodes=100):
    neqUn = jNeqSim.processSimulation.processEquipment.util.NeqSimUnit(
        teststream, equipment, flowpattern)
    neqUn.setNumberOfNodes(numberOfNodes)
    processoperations.add(neqUn)
    return neqUn


def compsplitter(teststream, splitfactors, name=""):
    compSplitter = jNeqSim.processSimulation.processEquipment.splitter.ComponentSplitter(
    name, teststream)
    compSplitter.setSplitFactors(splitfactors)
    processoperations.add(compSplitter)
    return compSplitter

def splitter(teststream, splitfactors=[], name=""):
    splitter = jNeqSim.processSimulation.processEquipment.splitter.Splitter(
        teststream)
    if(len(splitfactors)>0):
        splitter.setSplitNumber(len(splitfactors))
        splitter.setSplitFactors(JDouble[:](splitfactors))
    splitter.setName(name)
    processoperations.add(splitter)
    return splitter


def heater(teststream, name=""):
    heater = jNeqSim.processSimulation.processEquipment.heatExchanger.Heater(
        teststream)
    heater.setName(name)
    processoperations.add(heater)
    return heater


def simplereservoir(fluid, name="Reservoir 1",  gasvolume=10.0 * 1e7, oilvolume=120.0 * 1e6, watervolume=10.0e6):
    reserv = jNeqSim.processSimulation.processEquipment.reservoir.SimpleReservoir(
        name)
    reserv.setReservoirFluid(fluid, gasvolume, oilvolume, watervolume)
    processoperations.add(reserv)
    return reserv


def cooler(teststream, name=""):
    cooler = jNeqSim.processSimulation.processEquipment.heatExchanger.Cooler(
        teststream)
    cooler.setName(name)
    processoperations.add(cooler)
    return cooler


def heatExchanger(stream1, stream2=None, name=""):
    if stream2 is None:
        heater = jNeqSim.processSimulation.processEquipment.heatExchanger.HeatExchanger(
            stream1)
    else:
        heater = jNeqSim.processSimulation.processEquipment.heatExchanger.HeatExchanger(
            stream1, stream2)
    heater.setName(name)
    processoperations.add(heater)
    return heater


def distillationColumn(trays=5, reboil=True, condenser=True, name="destColumn"):
    distillationColumn = jNeqSim.processSimulation.processEquipment.distillation.DistillationColumn(
        trays, reboil, condenser)
    distillationColumn.setName(name)
    processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(teststream, name=""):
    neqheater = jNeqSim.processSimulation.processEquipment.heatExchanger.NeqHeater(
        teststream)
    neqheater.setName(name)
    processoperations.add(neqheater)
    return neqheater


def twophasepipe(teststream, position, diameter, height, outTemp, rough):
    pipe = jNeqSim.processSimulation.processEquipment.pipeline.TwoPhasePipeLine(
        teststream)
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


def pipe(teststream, length, deltaElevation, diameter, rough):
    pipe = jNeqSim.processSimulation.processEquipment.pipeline.AdiabaticPipe(
        teststream)
    pipe.setDiameter(diameter)
    pipe.setLength(length)
    pipe.setPipeWallRoughness(rough)
    pipe.setInletElevation(0.0)
    pipe.setOutletElevation(deltaElevation)
    processoperations.add(pipe)
    return pipe


def pipeline(teststream, position, diameter, height, outTemp, rough, outerHeatTransferCoefficients, pipeWallHeatTransferCoefficients, numberOfNodesInLeg=50):
    pipe = jNeqSim.processSimulation.processEquipment.pipeline.OnePhasePipeLine(
        teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(JDouble[:](position))
    pipe.setHeightProfile(JDouble[:](height))
    pipe.setPipeDiameters(JDouble[:](diameter))
    pipe.setPipeWallRoughness(JDouble[:](rough))
    pipe.setPipeOuterHeatTransferCoefficients(
        JDouble[:](outerHeatTransferCoefficients))
    pipe.setPipeWallHeatTransferCoefficients(
        JDouble[:](pipeWallHeatTransferCoefficients))
    pipe.setOuterTemperatures(JDouble[:](outTemp))
    processoperations.add(pipe)
    return pipe


def clear():
    processoperations.clearAll()


def run():
    processoperations.run()


def clearProcess():
    processoperations.clearAll()


def runProcess():
    processoperations.run()


def runProcessAsThread():
    return processoperations.runAsThread()


def getProcess():
    return processoperations


def runtrans():
    processoperations.runTransient()


def view():
    processoperations.displayResult()


def viewProcess():
    processoperations.displayResult()


def waterDewPointAnalyser(teststream, name=""):
    waterDewPointAnalyser = jNeqSim.processSimulation.measurementDevice.WaterDewPointAnalyser(
        teststream)
    waterDewPointAnalyser.setName(name)
    processoperations.add(waterDewPointAnalyser)
    return waterDewPointAnalyser

def hydrateEquilibriumTemperatureAnalyser(teststream, name=""):
    hydrateEquilibriumTemperatureAnalyser = jNeqSim.processSimulation.measurementDevice.HydrateEquilibriumTemperatureAnalyser(
        teststream)
    hydrateEquilibriumTemperatureAnalyser.setName(name)
    processoperations.add(hydrateEquilibriumTemperatureAnalyser)
    return hydrateEquilibriumTemperatureAnalyser