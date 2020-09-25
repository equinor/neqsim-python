from neqsim import java_gateway
from neqsim import javaGateway
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

def recycle(teststream, name="recycle ?"):
    recycle1 = neqsim.processSimulation.processEquipment.util.Recycle()
    recycle1.addStream(teststream)
    processoperations.add(recycle1)
    return recycle1

def saturator(teststream, name="water saturator"):
    streamsaturator = neqsim.processSimulation.processEquipment.util.StreamSaturatorUtil(teststream)
    processoperations.add(streamsaturator)
    return streamsaturator

def glycoldehydrationlmodule(teststream, name="TEG process"):
    dehydrationlmodule = neqsim.processSimulation.processSystem.processModules.GlycolDehydrationlModule()
    dehydrationlmodule.setName(name)
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    processoperations.add(dehydrationlmodule)
    return dehydrationlmodule

def openprocess(filename):
    processoperations = neqsim.processSimulation.processSystem.ProcessSystem.open(filename)
    return processoperations

def separator(teststream, name="separator ?"):
    separator = neqsim.processSimulation.processEquipment.separator.Separator(teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator

def gasscrubber(teststream, name="scrubber ?"):
    separator = neqsim.processSimulation.processEquipment.separator.GasScrubber(teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator

def separator3phase(teststream, name="separator ?"):
    separator = neqsim.processSimulation.processEquipment.separator.ThreePhaseSeparator(teststream)
    separator.setName(name)
    processoperations.add(separator)
    return separator

def valve(teststream, p=1.0, name="valve ?"):
    valve = neqsim.processSimulation.processEquipment.valve.ThrottlingValve(teststream)
    valve.setOutletPressure(p)
    valve.setName(name)
    processoperations.add(valve)
    return valve


def compressor(teststream, pres=10.0, name="compressor ?"):
    compressor = neqsim.processSimulation.processEquipment.compressor.Compressor(teststream)
    compressor.setOutletPressure(pres)
    compressor.setName(name)
    processoperations.add(compressor)
    return compressor


def compressorChart(compressor, curveConditions, speed, flow, head, polyEff ):
    gateway = java_gateway
    double_class = gateway.jvm.double  

    curveConditionsJava = gateway.new_array(double_class,len(curveConditions))
    for i in range(len(curveConditionsJava)):
        curveConditionsJava[i]=curveConditions[i]

    speedJava = gateway.new_array(double_class,len(speed))
    for i in range(len(speed)):
        speedJava[i]=speed[i]
    
    flowJava = gateway.new_array(double_class,len(flow), len(flow[0]))
    headJava = gateway.new_array(double_class,len(head), len(head[0]))
    polyEffJava = gateway.new_array(double_class,len(polyEff), len(polyEff[0]))
    for i in range(len(flow)):
        for j in range(len(flow[0])):
            flowJava[i][j] = flow[i][j]
            headJava[i][j] = head[i][j]
            polyEffJava[i][j] = polyEff[i][j]
    
    compressor.getCompressorChart().setCurves(curveConditionsJava, speedJava, flowJava, headJava, polyEffJava)

def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    gateway = java_gateway
    double_class = gateway.jvm.double  
    
    curveConditionsJava = gateway.new_array(double_class,len(curveConditions))
    for i in range(len(curveConditionsJava)):
        curveConditionsJava[i]=curveConditions[i]
        
    surgeflowJava = gateway.new_array(double_class,len(surgeflow))
    surgeheadJava = gateway.new_array(double_class,len(surgehead))
    
    for i in range(len(surgeflow)):
            surgeflowJava[i] = surgeflow[i]
            surgeheadJava[i] = surgehead[i]
    
    compressor.getCompressorChart().getSurgeCurve().setCurve(curveConditionsJava, surgeflowJava, surgeheadJava)
    
def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    gateway = java_gateway
    double_class = gateway.jvm.double  
    
    curveConditionsJava = gateway.new_array(double_class,len(curveConditions))
    for i in range(len(curveConditionsJava)):
        curveConditionsJava[i]=curveConditions[i]
        
    stoneWallFlowJava = gateway.new_array(double_class,len(stoneWallflow))
    stoneWallHeadJava = gateway.new_array(double_class,len(stoneWallHead))
    
    for i in range(len(stoneWallflow)):
            stoneWallFlowJava[i] = stoneWallflow[i]
            stoneWallHeadJava[i] = stoneWallHead[i]
    
    compressor.getCompressorChart().getStoneWallCurve().setCurve(curveConditionsJava, stoneWallFlowJava, stoneWallHeadJava)
    


def pump(teststream, p, name="pump ?"):
    pump = neqsim.processSimulation.processEquipment.pump.Pump(teststream)
    pump.setOutletPressure(p)
    pump.setName(name)
    processoperations.add(pump)
    return pump

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

def phasemixer(name=""):
    mixer = neqsim.processSimulation.processEquipment.mixer.StaticPhaseMixer()
    mixer.setName(name)
    processoperations.add(mixer)
    return mixer

def nequnit(teststream, equipment="pipeline", flowpattern="stratified"):
    neqUn = neqsim.processSimulation.processEquipment.util.NeqSimUnit(teststream, equipment, flowpattern)
    processoperations.add(neqUn)
    return neqUn

def splitter(teststream, splitfactors, name=""):
    gateway = java_gateway
    double_class = gateway.jvm.double  
    splitfactorsJava = gateway.new_array(double_class,len(splitfactors))
    for i in range(0,len(splitfactors)):
        splitfactorsJava[i] = splitfactors[i]
    splitter = neqsim.processSimulation.processEquipment.splitter.Splitter(teststream)
    splitter.setSplitNumber(len(splitfactors))
    splitter.setSplitFactors(splitfactorsJava)
    splitter.setName(name)
    processoperations.add(splitter)
    return splitter

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

def pipe(teststream, length, deltaElevation, diameter, rough):
    pipe = neqsim.processSimulation.processEquipment.pipeline.AdiabaticPipe(teststream)
    pipe.setDiameter(diameter)
    pipe.setLength(length)
    pipe.setPipeWallRoughness(rough)
    pipe.setInletElevation(0.0)
    pipe.setOutletElevation(deltaElevation)
    processoperations.add(pipe)
    return pipe

def pipeline(teststream, position, diameter, height, outTemp, rough, outerHeatTransferCoefficients, pipeWallHeatTransferCoefficients):
    gateway = java_gateway
    double_class = gateway.jvm.double
    numberOfComponents =len(position)    
    positionJavaArray = gateway.new_array(double_class,numberOfComponents)
    diameterJavaArray = gateway.new_array(double_class,numberOfComponents)
    heightJavaArray = gateway.new_array(double_class,numberOfComponents)
    outTempJavaArray = gateway.new_array(double_class,numberOfComponents)
    roughJavaArray = gateway.new_array(double_class,numberOfComponents)
    javaouterHeatTransferCoefficients = gateway.new_array(double_class,numberOfComponents)
    javapipeWallHeatTransferCoefficients = gateway.new_array(double_class,numberOfComponents)
    i = 0
    for i in range(0,numberOfComponents):
        positionJavaArray[i] = position[i]
        diameterJavaArray[i] = diameter[i]
        heightJavaArray[i] = height[i]
        outTempJavaArray[i] = outTemp[i]
        roughJavaArray[i] = rough[i]
        javaouterHeatTransferCoefficients[i]=outerHeatTransferCoefficients[i]
        javapipeWallHeatTransferCoefficients[i]=pipeWallHeatTransferCoefficients[i]
        
        i = i+1
        
    pipe = neqsim.processSimulation.processEquipment.pipeline.OnePhasePipeLine(teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    numberOfNodesInLeg = 100
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(positionJavaArray)
    pipe.setHeightProfile(heightJavaArray)
    pipe.setPipeDiameters(diameterJavaArray)
    pipe.setPipeWallRoughness(roughJavaArray)
    pipe.setPipeOuterHeatTransferCoefficients(javaouterHeatTransferCoefficients)
    pipe.setPipeWallHeatTransferCoefficients(javapipeWallHeatTransferCoefficients)
    pipe.setOuterTemperatures(outTempJavaArray)
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

def runProcessAsThread(process):
    threadProcess = java_gateway.jvm.java.lang.Thread(process)
    threadProcess.run()
    return threadProcess

def getProcess():
    return processoperations

def runtrans():
    processoperations.runTransient()


def view():
    processoperations.displayResult()


def viewProcess():
    processoperations.displayResult()
