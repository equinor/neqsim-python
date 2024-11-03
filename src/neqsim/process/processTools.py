import jpype
import jpype.imports
from jpype.types import *
from neqsim.neqsimpython import jneqsim

processoperations = jneqsim.processsimulation.processsystem.ProcessSystem()


def newProcess():
    """
    Create a new process object
    """
    global processoperations
    processoperations = jneqsim.processsimulation.processsystem.ProcessSystem()


def stream(name, thermoSystem, t=0, p=0):
    """
    Create a stream with the given name and thermodynamic system, optionally setting temperature and pressure.

    Parameters:
    name (str): The name of the stream.
    thermoSystem: The thermodynamic system to be used in the stream.
    t (float, optional): The temperature to set for the thermodynamic system. Defaults to 0.
    p (float, optional): The pressure to set for the thermodynamic system. Defaults to 0.

    Returns:
    Stream: The created stream object.
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jneqsim.processsimulation.processequipment.stream.Stream(
        name, thermoSystem
    )
    processoperations.add(stream)
    return stream


def virtualstream(name, streamIn):
    """
    Create a virtual stream in the process simulation.

    Parameters:
    name (str): The name of the virtual stream.
    streamIn (Stream): The input stream to be virtualized.

    Returns:
    VirtualStream: The created virtual stream object.
    """
    stream = jneqsim.processsimulation.processequipment.stream.VirtualStream(
        name, streamIn
    )
    processoperations.add(stream)
    return stream


def neqstream(name, thermoSystem, t=0, p=0):
    """
    Create a NeqStream with the specified name and thermodynamic system, optionally setting temperature and pressure.

    Parameters:
    name (str): The name of the stream.
    thermoSystem (ThermoSystem): The thermodynamic system to be used in the stream.
    t (float, optional): The temperature to set for the thermodynamic system. Defaults to 0.
    p (float, optional): The pressure to set for the thermodynamic system. Defaults to 0.

    Returns:
    NeqStream: The created NeqStream object.
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jneqsim.processsimulation.processequipment.stream.NeqStream(
        name, thermoSystem
    )
    stream.setName(name)
    processoperations.add(stream)
    return stream


def recycle(name, stream=None):
    """
    Create a recycle process unit and optionally add a stream to it.

    Parameters:
    name (str): The name of the recycle unit.
    stream (optional): The stream to be added to the recycle unit. Default is None.

    Returns:
    Recycle: The created recycle process unit.
    """
    recycle1 = jneqsim.processsimulation.processequipment.util.Recycle(name)
    if not stream is None:
        recycle1.addStream(stream)
    processoperations.add(recycle1)
    return recycle1


def saturator(name, teststream):
    """
    Create a StreamSaturatorUtil object and add it to the process operations.

    Parameters:
    name (str): The name of the saturator.
    teststream (Stream): The stream to be saturated.

    Returns:
    StreamSaturatorUtil: The created StreamSaturatorUtil object.
    """
    streamsaturator = (
        jneqsim.processsimulation.processequipment.util.StreamSaturatorUtil(
            name, teststream
        )
    )
    processoperations.add(streamsaturator)
    return streamsaturator


def glycoldehydrationlmodule(name, teststream):
    dehydrationlmodule = (
        jneqsim.processsimulation.processsystem.processModules.GlycolDehydrationlModule(
            name
        )
    )
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    processoperations.add(dehydrationlmodule)
    return dehydrationlmodule


def openprocess(filename):
    processoperations = jneqsim.processsimulation.processsystem.ProcessSystem.open(
        filename
    )
    return processoperations


def separator(name, teststream):
    """
    Create a two phase separator process equipment and add it to the process operations.

    Parameters:
    name (str): The name of the separator.
    teststream (Stream): The test stream to be separated.

    Returns:
    Separator: The created separator object.
    """
    separator = jneqsim.processsimulation.processequipment.separator.Separator(
        name, teststream
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def GORfitter(name, teststream):
    """
    Create and configure a GORfitter process equipment.

    Parameters:
    name (str): The name of the GORfitter.
    teststream (Stream): The test stream to be used by the GORfitter.

    Returns:
    GORfitter: The configured GORfitter process equipment.
    """
    GORfitter1 = jneqsim.processsimulation.processequipment.util.GORfitter(
        name, name, teststream
    )
    GORfitter1.setName(name)
    processoperations.add(GORfitter1)
    return GORfitter1


def simpleTEGAbsorber(name):
    """
    Create and configure a SimpleTEGAbsorber with the given name.

    This function initializes a SimpleTEGAbsorber object from the jneqsim
    library, sets its name, adds it to the process operations, and returns
    the configured absorber.

    Parameters:
    name (str): The name to assign to the SimpleTEGAbsorber.

    Returns:
    SimpleTEGAbsorber: The configured SimpleTEGAbsorber object.
    """
    absorber = jneqsim.processsimulation.processequipment.absorber.SimpleTEGAbsorber(
        name
    )
    absorber.setName(name)
    processoperations.add(absorber)
    return absorber


def waterStripperColumn(name):
    """
    Create and configure a water stripper column.

    This function initializes a WaterStripperColumn object with the given name,
    sets its name, adds it to the process operations, and returns the configured
    stripper column.

    Parameters:
    name (str): The name of the water stripper column.

    Returns:
    WaterStripperColumn: The configured water stripper column object.
    """
    stripper = jneqsim.processsimulation.processequipment.absorber.WaterStripperColumn(
        name
    )
    stripper.setName(name)
    processoperations.add(stripper)
    return stripper


def gasscrubber(name, teststream):
    """
    Create a gas scrubber separator and add it to the process operations.

    Parameters:
    name (str): The name of the gas scrubber.
    teststream: The test stream to be processed by the gas scrubber.

    Returns:
    separator: The created GasScrubber object.
    """
    separator = jneqsim.processsimulation.processequipment.separator.GasScrubber(
        name, teststream
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def separator3phase(name, teststream):
    """
    Create a three-phase separator and add it to the process operations.

    Parameters:
    name (str): The name of the separator.
    teststream (Stream): The stream to be separated.

    Returns:
    ThreePhaseSeparator: The created three-phase separator object.
    """
    separator = (
        jneqsim.processsimulation.processequipment.separator.ThreePhaseSeparator(
            name, teststream
        )
    )
    separator.setName(name)
    processoperations.add(separator)
    return separator


def valve(name, teststream, p=1.0):
    """
    Create a throttling valve in the process simulation.

    Parameters:
    name (str): The name of the valve.
    teststream: The stream to which the valve is connected.
    p (float, optional): The outlet pressure of the valve. Default is 1.0.

    Returns:
    ThrottlingValve: The created throttling valve object.
    """
    valve = jneqsim.processsimulation.processequipment.valve.ThrottlingValve(
        name, teststream
    )
    valve.setOutletPressure(p)
    valve.setName(name)
    processoperations.add(valve)
    return valve


def calculator(name):
    """
    Create a Calculator object and add it to the process operations.

    Parameters:
    name (str): The name of the calculator.

    Returns:
    Calculator: The created Calculator object.
    """
    calc2 = jneqsim.processsimulation.processequipment.util.Calculator(name)
    processoperations.add(calc2)
    return calc2


def setpoint(name1, unit1, name2, unit2):
    """
    Create a setpoint for process simulation and add it to process operations.

    Parameters:
    name1 (str): The name of the first variable.
    unit1 (str): The unit of the first variable.
    name2 (str): The name of the second variable.
    unit2 (str): The unit of the second variable.

    Returns:
    SetPoint: The created setpoint object.
    """
    setp = jneqsim.processsimulation.processequipment.util.SetPoint(
        name1, unit1, name2, unit2
    )
    processoperations.add(setp)
    return setp


def filters(name, teststream):
    """
    Create a filter process equipment and add it to the process operations.

    Parameters:
    name (str): The name of the filter.
    teststream (Stream): The stream to be filtered.

    Returns:
    Filter: The created filter process equipment.
    """
    filter2 = jneqsim.processsimulation.processequipment.filter.Filter(name, teststream)
    processoperations.add(filter2)
    return filter2


def compressor(name, teststream, pres=10.0):
    """
    Create and configure a compressor for a given test stream.

    Parameters:
    name (str): The name of the compressor.
    teststream: The test stream to be compressed.
    pres (float, optional): The outlet pressure of the compressor. Default is 10.0.

    Returns:
    Compressor: The configured compressor object.
    """
    compressor = jneqsim.processsimulation.processequipment.compressor.Compressor(
        name, teststream
    )
    compressor.setOutletPressure(pres)
    processoperations.add(compressor)
    return compressor


def compressorChart(compressor, curveConditions, speed, flow, head, polyEff):
    """
    Set the compressor chart data for a given compressor.

    Parameters:
    compressor (Compressor): The compressor object for which the chart is being set.
    curveConditions (list of float): Conditions for the curves.
    speed (list of float): Speed values for the compressor.
    flow (list of list of float): Flow values for the compressor.
    head (list of list of float): Head values for the compressor.
    polyEff (list of list of float): Polytropic efficiency values for the compressor.

    Returns:
    None
    """
    compressor.getCompressorChart().setCurves(
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def pumpChart(pump, curveConditions, speed, flow, head, polyEff):
    """
    Set the pump chart with the given parameters.

    Parameters:
    pump (Pump): The pump object for which the chart is being set.
    curveConditions (list of float): Conditions under which the pump curves are defined.
    speed (list of float): List of pump speeds.
    flow (list of list of float): 2D list representing flow rates for different conditions and speeds.
    head (list of list of float): 2D list representing head values corresponding to the flow rates.
    polyEff (list of list of float): 2D list representing the polytropic efficiency corresponding to the flow rates and head values.

    Returns:
    None
    """
    pump.getPumpChart().setCurves(
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    """
    Set the surge curve for a given compressor.

    Parameters:
    compressor (Compressor): The compressor object for which the surge curve is being set.
    curveConditions (list of float): The conditions at which the surge curve is defined.
    surgeflow (list of float): The flow values corresponding to the surge curve.
    surgehead (list of float): The head values corresponding to the surge curve.

    Returns:
    None
    """
    compressor.getCompressorChart().getSurgeCurve().setCurve(
        JDouble[:](curveConditions), JDouble[:](surgeflow), JDouble[:](surgehead)
    )


def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    """
    Set the stone wall curve for a given compressor.

    Parameters:
    compressor (Compressor): The compressor object for which the stone wall curve is being set.
    curveConditions (list of float): The conditions at which the stone wall curve is defined.
    stoneWallflow (list of float): The flow values corresponding to the stone wall curve.
    stoneWallHead (list of float): The head values corresponding to the stone wall curve.

    Returns:
    None
    """
    compressor.getCompressorChart().getStoneWallCurve().setCurve(
        JDouble[:](curveConditions),
        JDouble[:](stoneWallflow),
        JDouble[:](stoneWallHead),
    )


def pump(name, teststream, p=1.0):
    """
    Create a pump process equipment and set its outlet pressure.

    Parameters:
    name (str): The name of the pump.
    teststream (Stream): The stream to be pumped.
    p (float, optional): The outlet pressure of the pump. Defaults to 1.0.

    Returns:
    Pump: The created pump object.
    """
    pump = jneqsim.processsimulation.processequipment.pump.Pump(name, teststream)
    pump.setOutletPressure(p)
    processoperations.add(pump)
    return pump


def expander(name, teststream, p):
    """
    Create and configure an expander for a process simulation.

    Parameters:
    name (str): The name of the expander.
    teststream (Stream): The stream to be expanded.
    p (float): The outlet pressure of the expander.

    Returns:
    Expander: The configured expander object.
    """
    expander = jneqsim.processsimulation.processequipment.expander.Expander(
        name, teststream
    )
    expander.setOutletPressure(p)
    expander.setName(name)
    processoperations.add(expander)
    return expander


def mixer(name=""):
    """
    Create and add a mixer to the process operations.

    Parameters:
    name (str): The name of the mixer. Default is an empty string.

    Returns:
    Mixer: An instance of the Mixer class.
    """
    mixer = jneqsim.processsimulation.processequipment.mixer.Mixer(name)
    processoperations.add(mixer)
    return mixer


def phasemixer(name):
    mixer = jneqsim.processsimulation.processequipment.mixer.StaticPhaseMixer(name)
    processoperations.add(mixer)
    return mixer


def nequnit(
    teststream, equipment="pipeline", flowpattern="stratified", numberOfNodes=100
):
    """
    Create and configure a NeqSim unit operation.

    Parameters:
    teststream (Stream): The stream to be processed.
    equipment (str, optional): The type of equipment to be used. Default is "pipeline".
    flowpattern (str, optional): The flow pattern in the equipment. Default is "stratified".
    numberOfNodes (int, optional): The number of nodes for the simulation. Default is 100.

    Returns:
    NeqSimUnit: The configured NeqSim unit operation.
    """
    neqUn = jneqsim.processsimulation.processequipment.util.NeqSimUnit(
        teststream, equipment, flowpattern
    )
    neqUn.setNumberOfNodes(numberOfNodes)
    processoperations.add(neqUn)
    return neqUn


def compsplitter(name, teststream, splitfactors):
    """
    Create and configure a component splitter.

    Parameters:
    name (str): The name of the component splitter.
    teststream (Stream): The stream to be split.
    splitfactors (list of float): The split factors for each component in the stream.

    Returns:
    ComponentSplitter: The configured component splitter.
    """
    compSplitter = (
        jneqsim.processsimulation.processequipment.splitter.ComponentSplitter(
            name, teststream
        )
    )
    compSplitter.setSplitFactors(splitfactors)
    processoperations.add(compSplitter)
    return compSplitter


def splitter(name, teststream, splitfactors=[]):
    """
    Create a splitter process equipment.

    Parameters:
    name (str): The name of the splitter.
    teststream (Stream): The stream to be split.
    splitfactors (list of float, optional): The factors by which to split the stream. 
                                            If provided, the length of this list determines 
                                            the number of splits and the values determine 
                                            the split ratios.

    Returns:
    Splitter: The created splitter object.
    """
    splitter = jneqsim.processsimulation.processequipment.splitter.Splitter(
        name, teststream
    )
    if len(splitfactors) > 0:
        splitter.setSplitNumber(len(splitfactors))
        splitter.setSplitFactors(JDouble[:](splitfactors))
    processoperations.add(splitter)
    return splitter


def heater(name, teststream):
    """
    Create a heater process equipment and add it to the process operations.

    Parameters:
    name (str): The name of the heater.
    teststream (Stream): The stream to be heated.

    Returns:
    Heater: The created heater object.
    """
    heater = jneqsim.processsimulation.processequipment.heatexchanger.Heater(
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
    reserv = jneqsim.processsimulation.processequipment.reservoir.SimpleReservoir(name)
    reserv.setReservoirFluid(fluid, gasvolume, oilvolume, watervolume)
    processoperations.add(reserv)
    return reserv


def cooler(name, teststream):
    cooler = jneqsim.processsimulation.processequipment.heatexchanger.Cooler(
        name, teststream
    )
    cooler.setName(name)
    processoperations.add(cooler)
    return cooler


def heatExchanger(name, stream1, stream2=None):
    if stream2 is None:
        heater = jneqsim.processsimulation.processequipment.heatexchanger.HeatExchanger(
            name, stream1
        )
    else:
        heater = jneqsim.processsimulation.processequipment.heatexchanger.HeatExchanger(
            name, stream1, stream2
        )
    heater.setName(name)
    processoperations.add(heater)
    return heater


def distillationColumn(name, trays=5, reboil=True, condenser=True):
    distillationColumn = (
        jneqsim.processsimulation.processequipment.distillation.DistillationColumn(
            name, trays, reboil, condenser
        )
    )
    processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(name, teststream):
    neqheater = jneqsim.processsimulation.processequipment.heatexchanger.NeqHeater(
        name, teststream
    )
    processoperations.add(neqheater)
    return neqheater


def twophasepipe(name, teststream, position, diameter, height, outTemp, rough):
    pipe = jneqsim.processsimulation.processequipment.pipeline.TwoPhasePipeLine(
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
    pipe = jneqsim.processsimulation.processequipment.pipeline.AdiabaticPipe(
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
    pipe = jneqsim.processsimulation.processequipment.pipeline.OnePhasePipeLine(
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
        jneqsim.processsimulation.measurementdevice.WaterDewPointAnalyser(teststream)
    )
    waterDewPointAnalyser.setName(name)
    processoperations.add(waterDewPointAnalyser)
    return waterDewPointAnalyser


def hydrateEquilibriumTemperatureAnalyser(name, teststream):
    hydrateEquilibriumTemperatureAnalyser = jneqsim.processsimulation.measurementdevice.HydrateEquilibriumTemperatureAnalyser(
        name, teststream
    )
    hydrateEquilibriumTemperatureAnalyser.setName(name)
    processoperations.add(hydrateEquilibriumTemperatureAnalyser)
    return hydrateEquilibriumTemperatureAnalyser
