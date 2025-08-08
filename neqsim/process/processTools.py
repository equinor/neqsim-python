import json

from jpype.types import JDouble
from jpype.types import *

from neqsim.neqsimpython import jneqsim

processoperations = jneqsim.process.processmodel.ProcessSystem()
_loop_mode = False


def newProcess(name=""):
    """
    Create a new process object
    """
    global processoperations
    processoperations = jneqsim.process.processmodel.ProcessSystem(name)
    return processoperations


def set_loop_mode(loop_mode):
    """
    Set the loop mode for process operations.

    Parameters:
    loop_mode (bool): If True, sets the loop mode to allow multiple runs without clearing the process.
    """
    global _loop_mode
    _loop_mode = loop_mode


def stream(name, thermoSystem, t=0, p=0):
    """
    Create a stream with the given name and thermodynamic system, optionally setting temperature and pressure.

    Parameters:
    name (str): The name of the stream.
    thermoSystem (ThermoSystem): The thermodynamic system to be used in the stream.
    t (float, optional): The temperature to set for the thermodynamic system. Defaults to 0.
    p (float, optional): The pressure to set for the thermodynamic system. Defaults to 0.

    Returns:
    Stream: The created stream object.
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jneqsim.process.equipment.stream.Stream(name, thermoSystem)
    if not _loop_mode:
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
    stream = jneqsim.process.equipment.stream.VirtualStream(name, streamIn)
    if not _loop_mode:
        processoperations.add(stream)
    return stream


def neqstream(name, thermoSystem, t=0, p=0):
    """
    Create a NeqStream with the specified name and thermodynamic system, optionally setting temperature and pressure.

    Parameters:
    name (str): The name of the stream.
    thermoSystem (ThermodynamicSystem): The thermodynamic system to be used in the stream.
    t (float, optional): The temperature to set for the thermodynamic system. Defaults to 0.
    p (float, optional): The pressure to set for the thermodynamic system. Defaults to 0.

    Returns:
    NeqStream: The created NeqStream object.
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jneqsim.process.equipment.stream.NeqStream(name, thermoSystem)
    stream.setName(name)
    if not _loop_mode:
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
    recycle1 = jneqsim.process.equipment.util.Recycle(name)
    if not stream is None:
        recycle1.addStream(stream)
    if not _loop_mode:
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
    streamsaturator = jneqsim.process.equipment.util.StreamSaturatorUtil(
        name, teststream
    )
    if not _loop_mode:
        processoperations.add(streamsaturator)
    return streamsaturator


def glycoldehydrationlmodule(name, teststream):
    dehydrationlmodule = (
        jneqsim.process.processmodel.processModules.GlycolDehydrationlModule(name)
    )
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    if not _loop_mode:
        processoperations.add(dehydrationlmodule)
    return dehydrationlmodule


def openprocess(filename):
    processoperations = jneqsim.process.processmodel.ProcessSystem.open(filename)
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
    separator = jneqsim.process.equipment.separator.Separator(name, teststream)
    separator.setName(name)
    if not _loop_mode:
        processoperations.add(separator)
    return separator


def GORfitter(name, teststream):
    """
    Create and configure a GORfitter process equipment.

    Parameters:
    name (str): The name of the GORfitter.
    teststream (Stream): The test stream to be used by the GORfitter.

    Returns:
    GORfitter: The configured GORfitter object.
    """
    GORfitter1 = jneqsim.process.equipment.util.GORfitter(name, teststream)
    GORfitter1.setName(name)
    if not _loop_mode:
        processoperations.add(GORfitter1)
    return GORfitter1


def simpleTEGAbsorber(name):
    absorber = jneqsim.process.equipment.absorber.SimpleTEGAbsorber(name)
    absorber.setName(name)
    if not _loop_mode:
        processoperations.add(absorber)
    return absorber


def waterStripperColumn(name):
    stripper = jneqsim.process.equipment.absorber.WaterStripperColumn(name)
    stripper.setName(name)
    if not _loop_mode:
        processoperations.add(stripper)
    return stripper


def gasscrubber(name, teststream):
    separator = jneqsim.process.equipment.separator.GasScrubber(name, teststream)
    separator.setName(name)
    if not _loop_mode:
        processoperations.add(separator)
    return separator


def separator3phase(name, teststream):
    """
    Create a three-phase separator and add it to the process operations.

    Parameters:
    name (str): The name of the separator.
    teststream (Stream): The input stream to be separated.

    Returns:
    ThreePhaseSeparator: The created three-phase separator object.
    """
    separator = jneqsim.process.equipment.separator.ThreePhaseSeparator(
        name, teststream
    )
    separator.setName(name)
    if not _loop_mode:
        processoperations.add(separator)
    return separator


def valve(name, teststream, p=1.0):
    """
    Create a throttling valve in the process simulation.

    Parameters:
    name (str): The name of the valve.
    teststream (Stream): The stream that passes through the valve.
    p (float, optional): The outlet pressure of the valve. Default is 1.0.

    Returns:
    ThrottlingValve: The created throttling valve object.
    """
    valve = jneqsim.process.equipment.valve.ThrottlingValve(name, teststream)
    valve.setOutletPressure(p)
    valve.setName(name)
    if not _loop_mode:
        processoperations.add(valve)
    return valve


def calculator(name):
    calc2 = jneqsim.process.equipment.util.Calculator(name)
    if not _loop_mode:
        processoperations.add(calc2)
    return calc2


def setpoint(name1, unit1, name2, unit2):
    setp = jneqsim.process.equipment.util.SetPoint(name1, unit1, name2, unit2)
    if not _loop_mode:
        processoperations.add(setp)
    return setp


def filters(name, teststream):
    filter2 = jneqsim.process.equipment.filter.Filter(name, teststream)
    if not _loop_mode:
        processoperations.add(filter2)
    return filter2


def compressor(name, teststream, pres=10.0):
    """
    Create and configure a compressor for a given stream.

    Parameters:
    name (str): The name of the compressor.
    teststream: The stream to be compressed.
    pres (float, optional): The outlet pressure of the compressor. Default is 10.0.

    Returns:
    Compressor: The configured compressor object.
    """
    compressor = jneqsim.process.equipment.compressor.Compressor(name, teststream)
    compressor.setOutletPressure(pres)
    if not _loop_mode:
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
    """
    Create a pump process equipment and add it to the process operations.

    Parameters:
    name (str): The name of the pump.
    teststream (Stream): The stream to be pumped.
    p (float, optional): The outlet pressure of the pump. Default is 1.0.

    Returns:
    Pump: The created pump object.
    """
    pump = jneqsim.process.equipment.pump.Pump(name, teststream)
    pump.setOutletPressure(p)
    if not _loop_mode:
        processoperations.add(pump)
    return pump


def expander(name, teststream, p):
    """
    Create and configure an expander for the process simulation.

    Parameters:
    name (str): The name of the expander.
    teststream (Stream): The stream to be expanded.
    p (float): The outlet pressure of the expander.

    Returns:
    Expander: The configured expander object.
    """
    expander = jneqsim.process.equipment.expander.Expander(name, teststream)
    expander.setOutletPressure(p)
    expander.setName(name)
    if not _loop_mode:
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
    mixer = jneqsim.process.equipment.mixer.Mixer(name)
    if not _loop_mode:
        processoperations.add(mixer)
    return mixer


def phasemixer(name):
    mixer = jneqsim.process.equipment.mixer.StaticPhaseMixer(name)
    if not _loop_mode:
        processoperations.add(mixer)
    return mixer


def nequnit(
    teststream, equipment="pipeline", flowpattern="stratified", numberOfNodes=100
):
    neqUn = jneqsim.process.equipment.util.NeqSimUnit(
        teststream, equipment, flowpattern
    )
    neqUn.setNumberOfNodes(numberOfNodes)
    if not _loop_mode:
        processoperations.add(neqUn)
    return neqUn


def compsplitter(name, teststream, splitfactors):
    compSplitter = jneqsim.process.equipment.splitter.ComponentSplitter(
        name, teststream
    )
    compSplitter.setSplitFactors(splitfactors)
    if not _loop_mode:
        processoperations.add(compSplitter)
    return compSplitter


def splitter(name, teststream, splitfactors=[]):
    """
    Create a splitter process equipment and add it to the process operations.

    Parameters:
    name (str): The name of the splitter.
    teststream (Stream): The stream to be split.
    splitfactors (list of float, optional): The factors by which to split the stream.
                                            If provided, the length of this list determines
                                            the number of splits, and the values determine
                                            the split ratios.

    Returns:
    Splitter: The created splitter object.
    """
    splitter = jneqsim.process.equipment.splitter.Splitter(name, teststream)
    if len(splitfactors) > 0:
        splitter.setSplitNumber(len(splitfactors))
        splitter.setSplitFactors(JDouble[:](splitfactors))
    if not _loop_mode:
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
    heater = jneqsim.process.equipment.heatexchanger.Heater(name, teststream)
    heater.setName(name)
    if not _loop_mode:
        processoperations.add(heater)
    return heater


def simplereservoir(
    name,
    fluid,
    gasvolume=10.0 * 1e7,
    oilvolume=120.0 * 1e6,
    watervolume=10.0e6,
):
    reserv = jneqsim.process.equipment.reservoir.SimpleReservoir(name)
    reserv.setReservoirFluid(fluid, gasvolume, oilvolume, watervolume)
    if not _loop_mode:
        processoperations.add(reserv)
    return reserv


def cooler(name, teststream):
    """
    Create and configure a cooler process equipment.

    Parameters:
    name (str): The name of the cooler.
    teststream (Stream): The stream to be cooled.

    Returns:
    Cooler: The configured cooler object.
    """
    cooler = jneqsim.process.equipment.heatexchanger.Cooler(name, teststream)
    cooler.setName(name)
    if not _loop_mode:
        processoperations.add(cooler)
    return cooler


def heatExchanger(name, stream1, stream2=None):
    """
    Create a heat exchanger process unit.

    Parameters:
    name (str): The name of the heat exchanger.
    stream1: The first input stream for the heat exchanger.
    stream2 (optional): The second input stream for the heat exchanger. If not provided, a single stream heat exchanger is created.

    Returns:
    HeatExchanger: The created heat exchanger object.
    """
    if stream2 is None:
        heater = jneqsim.process.equipment.heatexchanger.HeatExchanger(name, stream1)
    else:
        heater = jneqsim.process.equipment.heatexchanger.HeatExchanger(
            name, stream1, stream2
        )
    heater.setName(name)
    if not _loop_mode:
        processoperations.add(heater)
    return heater


def distillationColumn(name, trays=5, reboil=True, condenser=True):
    distillationColumn = jneqsim.process.equipment.distillation.DistillationColumn(
        name, trays, reboil, condenser
    )
    if not _loop_mode:
        processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(name, teststream):
    neqheater = jneqsim.process.equipment.heatexchanger.NeqHeater(name, teststream)
    if not _loop_mode:
        processoperations.add(neqheater)
    return neqheater


def twophasepipe(name, teststream, position, diameter, height, outTemp, rough):
    pipe = jneqsim.process.equipment.pipeline.TwoPhasePipeLine(name, teststream)
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
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def pipe(name, teststream, length, deltaElevation, diameter, rough):
    pipe = jneqsim.process.equipment.pipeline.AdiabaticPipe(name, teststream)
    pipe.setDiameter(diameter)
    pipe.setLength(length)
    pipe.setPipeWallRoughness(rough)
    pipe.setInletElevation(0.0)
    pipe.setOutletElevation(deltaElevation)
    if not _loop_mode:
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
    pipe = jneqsim.process.equipment.pipeline.OnePhasePipeLine(name, teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(position)
    pipe.setHeightProfile(height)
    pipe.setPipeDiameters(diameter)
    pipe.setPipeWallRoughness(rough)
    pipe.setPipeOuterHeatTransferCoefficients(outerHeatTransferCoefficients)
    pipe.setPipeWallHeatTransferCoefficients(pipeWallHeatTransferCoefficients)
    pipe.setOuterTemperatures(outTemp)
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def clear():
    """
    Clear all process operations.

    This function calls the `clearAll` method from the `processoperations` module
    to remove all existing process operations.
    """
    processoperations.clearAll()


def run():
    """
    Execute the process operations.

    This function calls the `run` method of the `processoperations` module to
    perform the necessary process operations.
    """
    processoperations.run()


def clearProcess():
    """
    Clear all process operations.

    This function clears all the process operations by calling the clearAll method
    from the processoperations module.
    """
    clear()


def runProcess():
    """
    Execute the process operations.

    This function triggers the execution of the process operations by calling
    the `run` method from the `processoperations` module.
    """
    run()


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
    waterDewPointAnalyser = jneqsim.process.measurementdevice.WaterDewPointAnalyser(
        teststream
    )
    waterDewPointAnalyser.setName(name)
    if not _loop_mode:
        processoperations.add(waterDewPointAnalyser)
    return waterDewPointAnalyser


def hydrateEquilibriumTemperatureAnalyser(name, teststream):
    hydrateEquilibriumTemperatureAnalyser = (
        jneqsim.process.measurementdevice.HydrateEquilibriumTemperatureAnalyser(
            name, teststream
        )
    )
    hydrateEquilibriumTemperatureAnalyser.setName(name)
    if not _loop_mode:
        processoperations.add(hydrateEquilibriumTemperatureAnalyser)
    return hydrateEquilibriumTemperatureAnalyser


def results_json(process, filename=None):
    """
    Generate a JSON report from the process and optionally save it to a file.

    Parameters:
    process: The process object to generate the report from.
    filename (str, optional): The file path to save the JSON report. If None, the report is not saved.

    Returns:
    dict: The JSON report as a Python dictionary.
    """
    try:
        # Generate the JSON report
        json_report = str(process.getReport_json())
        results = json.loads(json_report)

        # Save to file if a filename is provided
        if filename:
            with open(filename, "w") as json_file:
                json.dump(results, json_file, indent=4)
            print(f"JSON report saved to {filename}")

        return results
    except Exception as e:
        print(f"Error generating JSON report: {e}")
        return None
