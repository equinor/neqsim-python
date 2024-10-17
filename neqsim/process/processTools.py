import jpype
import jpype.imports
from jpype.types import *
from jneqsim import neqsim

processoperations = neqsim.processsimulation.processsystem.ProcessSystem()


def newProcess():
    """
    Create a new process object
    """
    global processoperations
    processoperations = neqsim.processsimulation.processsystem.ProcessSystem()


def stream(name, thermoSystem, t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = neqsim.processsimulation.processequipment.stream.Stream(name, thermoSystem)
    processoperations.add(stream)
    return stream


def virtualstream(name, streamIn):
    stream = neqsim.processsimulation.processequipment.stream.VirtualStream(
        name, streamIn
    )
    processoperations.add(stream)
    return stream


def neqstream(name, thermoSystem, t=0, p=0):
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = neqsim.processsimulation.processequipment.stream.NeqStream(
        name, thermoSystem
    )
    stream.setName(name)
    processoperations.add(stream)
    return stream


def recycle(name, stream=None):
    recycle1 = neqsim.processsimulation.processequipment.util.Recycle(name)
    if not stream is None:
        recycle1.addStream(stream)
    processoperations.add(recycle1)
    return recycle1


def saturator(name, teststream):
    streamsaturator = (
        neqsim.processsimulation.processequipment.util.StreamSaturatorUtil(
            name, teststream
        )
    )
    processoperations.add(streamsaturator)
    return streamsaturator


def glycoldehydrationlmodule(name, teststream):
    dehydrationlmodule = (
        neqsim.processsimulation.processsystem.processModules.GlycolDehydrationlModule(
            name
        )
    )
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    processoperations.add(dehydrationlmodule)
    return dehydrationlmodule


def openprocess(filename):
    processoperations = neqsim.processsimulation.processsystem.ProcessSystem.open(
        filename
    )
    return processoperations


def separator(name, teststream):
    separator = neqsim.processsimulation.processequipment.separator.Separator(
        name, teststream
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def GORfitter(name, teststream):
    GORfitter1 = neqsim.processsimulation.processequipment.util.GORfitter(
        name, name, teststream
    )
    GORfitter1.setName(name)
    processoperations.add(GORfitter1)
    return GORfitter1


def simpleTEGAbsorber(name):
    absorber = neqsim.processsimulation.processequipment.absorber.SimpleTEGAbsorber(
        name
    )
    absorber.setName(name)
    processoperations.add(absorber)
    return absorber


def waterStripperColumn(name):
    stripper = neqsim.processsimulation.processequipment.absorber.WaterStripperColumn(
        name
    )
    stripper.setName(name)
    processoperations.add(stripper)
    return stripper


def gasscrubber(name, teststream):
    separator = neqsim.processsimulation.processequipment.separator.GasScrubber(
        name, teststream
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def separator3phase(name, teststream):
    separator = neqsim.processsimulation.processequipment.separator.ThreePhaseSeparator(
        name, teststream
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def valve(name, teststream, p=1.0):
    valve = neqsim.processsimulation.processequipment.valve.ThrottlingValve(
        name, teststream
    )
    valve.setOutletPressure(p)
    valve.setName(name)
    processoperations.add(valve)
    return valve


def calculator(name):
    calc2 = neqsim.processsimulation.processequipment.util.Calculator(name)
    processoperations.add(calc2)
    return calc2


def setpoint(name1, unit1, name2, unit2):
    setp = neqsim.processsimulation.processequipment.util.SetPoint(
        name1, unit1, name2, unit2
    )
    processoperations.add(setp)
    return setp


def filters(name, teststream):
    filter2 = neqsim.processsimulation.processequipment.filter.Filter(name, teststream)
    processoperations.add(filter2)
    return filter2


def compressor(name, teststream, pres=10.0):
    compressor = neqsim.processsimulation.processequipment.compressor.Compressor(
        name, teststream
    )
    compressor.setOutletPressure(pres)
    processoperations.add(compressor)
    return compressor


def compressorChart(compressor, curveConditions, speed, flow, head, polyEff):
    compressor.getCompressorChart().setCurves(
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def pumpChart(pump, curveConditions, speed, flow, head, polyEff):
    pump.getPumpChart().setCurves(
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    compressor.getCompressorChart().getSurgeCurve().setCurve(
        JDouble[:](curveConditions), JDouble[:](surgeflow), JDouble[:](surgehead)
    )


def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    compressor.getCompressorChart().getStoneWallCurve().setCurve(
        JDouble[:](curveConditions),
        JDouble[:](stoneWallflow),
        JDouble[:](stoneWallHead),
    )


def pump(name, teststream, p=1.0):
    pump = neqsim.processsimulation.processequipment.pump.Pump(name, teststream)
    pump.setOutletPressure(p)
    processoperations.add(pump)
    return pump


def expander(name, teststream, p):
    expander = neqsim.processsimulation.processequipment.expander.Expander(
        name, teststream
    )
    expander.setOutletPressure(p)
    expander.setName(name)
    processoperations.add(expander)
    return expander


def mixer(name=""):
    mixer = neqsim.processsimulation.processequipment.mixer.Mixer(name)
    processoperations.add(mixer)
    return mixer


def phasemixer(name):
    mixer = neqsim.processsimulation.processequipment.mixer.StaticPhaseMixer(name)
    processoperations.add(mixer)
    return mixer


def nequnit(
    teststream, equipment="pipeline", flowpattern="stratified", numberOfNodes=100
):
    neqUn = neqsim.processsimulation.processequipment.util.NeqSimUnit(
        teststream, equipment, flowpattern
    )
    neqUn.setNumberOfNodes(numberOfNodes)
    processoperations.add(neqUn)
    return neqUn


def compsplitter(name, teststream, splitfactors):
    compSplitter = neqsim.processsimulation.processequipment.splitter.ComponentSplitter(
        name, teststream
    )
    compSplitter.setSplitFactors(splitfactors)
    processoperations.add(compSplitter)
    return compSplitter


def splitter(name, teststream, splitfactors=[]):
    splitter = neqsim.processsimulation.processequipment.splitter.Splitter(
        name, teststream
    )
    if len(splitfactors) > 0:
        splitter.setSplitNumber(len(splitfactors))
        splitter.setSplitFactors(JDouble[:](splitfactors))
    processoperations.add(splitter)
    return splitter


def heater(name, teststream):
    heater = neqsim.processsimulation.processequipment.heatExchanger.Heater(
        name, teststream
    )
    heater.setName(name)
    processoperations.add(heater)
    return heater


def simplereservoir(
    name,
    fluid,
    gasvolume=10.0 * 1e7,
    oilvolume=120.0 * 1e6,
    watervolume=10.0e6,
):
    reserv = neqsim.processsimulation.processequipment.reservoir.SimpleReservoir(name)
    reserv.setReservoirFluid(fluid, gasvolume, oilvolume, watervolume)
    processoperations.add(reserv)
    return reserv


def cooler(name, teststream):
    cooler = neqsim.processsimulation.processequipment.heatExchanger.Cooler(
        name, teststream
    )
    cooler.setName(name)
    processoperations.add(cooler)
    return cooler


def heatExchanger(name, stream1, stream2=None):
    if stream2 is None:
        heater = neqsim.processsimulation.processequipment.heatExchanger.HeatExchanger(
            name, stream1
        )
    else:
        heater = neqsim.processsimulation.processequipment.heatExchanger.HeatExchanger(
            name, stream1, stream2
        )
    heater.setName(name)
    processoperations.add(heater)
    return heater


def distillationColumn(name, trays=5, reboil=True, condenser=True):
    distillationColumn = (
        neqsim.processsimulation.processequipment.distillation.DistillationColumn(
            name, trays, reboil, condenser
        )
    )
    processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(name, teststream):
    neqheater = neqsim.processsimulation.processequipment.heatExchanger.NeqHeater(
        name, teststream
    )
    processoperations.add(neqheater)
    return neqheater


def twophasepipe(name, teststream, position, diameter, height, outTemp, rough):
    pipe = neqsim.processsimulation.processequipment.pipeline.TwoPhasePipeLine(
        name, teststream
    )
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


def pipe(name, teststream, length, deltaElevation, diameter, rough):
    pipe = neqsim.processsimulation.processequipment.pipeline.AdiabaticPipe(
        name, teststream
    )
    pipe.setDiameter(diameter)
    pipe.setLength(length)
    pipe.setPipeWallRoughness(rough)
    pipe.setInletElevation(0.0)
    pipe.setOutletElevation(deltaElevation)
    processoperations.add(pipe)
    return pipe


def pipeline(
    name,
    teststream,
    position,
    diameter,
    height,
    outTemp,
    rough,
    outerHeatTransferCoefficients,
    pipeWallHeatTransferCoefficients,
    numberOfNodesInLeg=50,
):
    pipe = neqsim.processsimulation.processequipment.pipeline.OnePhasePipeLine(
        name, teststream
    )
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(JDouble[:](position))
    pipe.setHeightProfile(JDouble[:](height))
    pipe.setPipeDiameters(JDouble[:](diameter))
    pipe.setPipeWallRoughness(JDouble[:](rough))
    pipe.setPipeOuterHeatTransferCoefficients(JDouble[:](outerHeatTransferCoefficients))
    pipe.setPipeWallHeatTransferCoefficients(
        JDouble[:](pipeWallHeatTransferCoefficients)
    )
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


def waterDewPointAnalyser(name, teststream):
    waterDewPointAnalyser = (
        neqsim.processsimulation.measurementdevice.WaterDewPointAnalyser(teststream)
    )
    waterDewPointAnalyser.setName(name)
    processoperations.add(waterDewPointAnalyser)
    return waterDewPointAnalyser


def hydrateEquilibriumTemperatureAnalyser(name, teststream):
    hydrateEquilibriumTemperatureAnalyser = neqsim.processsimulation.measurementdevice.HydrateEquilibriumTemperatureAnalyser(
        teststream
    )
    hydrateEquilibriumTemperatureAnalyser.setName(name)
    processoperations.add(hydrateEquilibriumTemperatureAnalyser)
    return hydrateEquilibriumTemperatureAnalyser
