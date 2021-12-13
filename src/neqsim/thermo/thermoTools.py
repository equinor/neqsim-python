import pandas
from neqsim.standards import ISO6976
import matplotlib.pyplot as plt
import jpype
import jpype.imports
from jpype.types import *
import numpy 
from neqsim.neqsimpython import neqsim

ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations
fluidcreator = neqsim.thermo.Fluid
fluid_type = {
    'srk': neqsim.thermo.system.SystemSrkEos,
    'SRK-EoS': neqsim.thermo.system.SystemSrkEos,
    'Psrk-EoS': neqsim.thermo.system.SystemPsrkEos,
    'PSRK-EoS': neqsim.thermo.system.SystemPsrkEos,
    'RK-EoS': neqsim.thermo.system.SystemRKEos,
    'pr': neqsim.thermo.system.SystemPrEos,
    'PR-EoS': neqsim.thermo.system.SystemPrEos,
    'pr-umr': neqsim.thermo.system.SystemUMRPRUMCEos,
    'srk-s': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'GERG-water': neqsim.thermo.system.SystemGERGwaterEos,
    'SRK-MC': neqsim.thermo.system.SystemSrkMathiasCopeman,
    'PR-MC': neqsim.thermo.system.SystemPrMathiasCopeman,
    'scrk': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'ScRK-EoS': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'nrtl': neqsim.thermo.system.SystemNRTL,
    'unifac': neqsim.thermo.system.SystemUNIFAC,
    'electrolyte': neqsim.thermo.system.SystemFurstElectrolyteEos,
    'Electrolyte-ScRK-EoS': neqsim.thermo.system.SystemFurstElectrolyteEos,
    'Electrolyte-CPA-EoS': neqsim.thermo.system.SystemElectrolyteCPAstatoil,
    'cpa-el': neqsim.thermo.system.SystemElectrolyteCPA,
    'cpa-s': neqsim.thermo.system.SystemSrkCPAs,
    'cpa-statoil': neqsim.thermo.system.SystemSrkCPAstatoil,
    'cpa': neqsim.thermo.system.SystemSrkCPAstatoil,
    'CPA-SRK-EoS': neqsim.thermo.system.SystemSrkCPA,
    'cpa-srk': neqsim.thermo.system.SystemSrkCPA,
    'srk-twoCoon': neqsim.thermo.system.SystemSrkTwuCoonParamEos,
    'cpa-pr': neqsim.thermo.system.SystemPrCPA,
    'CPA-PR-EoS': neqsim.thermo.system.SystemPrCPA,
    'SRK-TwuCoon-EOS': neqsim.thermo.system.SystemSrkTwuCoonStatoilEos
}


def fluid(name='srk', temperature=298.15, pressure=1.01325):
    fluid_function = fluid_type.get(name, neqsim.thermo.system.SystemSrkEos)
    return fluid_function(temperature, pressure)

def readEclipseFluid(filename):
    fluid1 = neqsim.thermo.util.readwrite.EclipseFluidReadWrite.read(filename)
    return fluid1

def fluid_df(reservoirFluiddf,lastIsPlusFraction=False, autoSetModel=False, modelName=''):
    if(autoSetModel):
        fluidcreator.setAutoSelectModel(True)
    else:
        fluidcreator.setAutoSelectModel(False)
    if(modelName):
        fluidcreator.setThermoModel(modelName)
    else:
        fluidcreator.setAutoSelectModel(False)
    if 'MolarMass[kg/mol]' in reservoirFluiddf:
        definedComponentsFrame = reservoirFluiddf[reservoirFluiddf['MolarMass[kg/mol]'].isnull()]
    else:
        definedComponentsFrame = reservoirFluiddf
    fluid7 = createfluid2(definedComponentsFrame['ComponentName'].tolist(), definedComponentsFrame['MolarComposition[-]'].tolist())
    TBPComponentsFrame = reservoirFluiddf.dropna()
    if not TBPComponentsFrame.equals(reservoirFluiddf):
        addOilFractions(fluid7, TBPComponentsFrame['ComponentName'].tolist(),TBPComponentsFrame['MolarComposition[-]'].tolist(),TBPComponentsFrame['MolarMass[kg/mol]'].tolist(), TBPComponentsFrame['RelativeDensity[-]'].tolist(),lastIsPlusFraction);
    return fluid7

def createfluid(fluid_type='dry gas'):
    return fluidcreator.create(fluid_type)

def createfluid2(names, molefractions, unit="mol/sec"):
    return fluidcreator.create2(JString[:](names), JDouble[:](molefractions), unit)

def addOilFractions(fluid, charNames,molefractions,molarMass,  density, lastIsPlusFraction=False):
    clonedfluid = fluid.clone()
    clonedfluid = fluidcreator.addOilFractions(JString[:](charNames), JDouble[:](molefractions), JDouble[:](molarMass), JDouble[:](density),lastIsPlusFraction)
    return clonedfluid

def newdatabase(system):
    system.createDatabase(1)

def tunewaxmodel(fluid, experimentaldata):
    tempList = [x+273.15 for x in experimentaldata['temperature']]
    presList = experimentaldata['pressure']
    expList = [x*100.0 for x in experimentaldata['experiment']]
   
    waxsim = neqsim.PVTsimulation.simulation.WaxFractionSim(fluid)
    waxsim.setTemperaturesAndPressures(JDouble[:](tempList),JDouble[:](presList))
    waxsim.setExperimentalData(JDouble[:](expList))
    waxsim.getOptimizer().setNumberOfTuningParameters(3)
    waxsim.getOptimizer().setMaxNumberOfIterations(20)
    waxsim.runTuning()
    waxsim.runCalc()
    
    results = {'temperature':  tempList, 
        'pressure':  presList,
        'experiment':  expList,
        'results': list(waxsim.getWaxFraction()),
        'parameters': list(waxsim.getOptimizer().getSampleSet().getSample(0).getFunction().getFittingParams())
    }    
    return results

def data(system):
    a = system.getResultTable()
    return a

def table(system):
    return system.createTable("")

def dataFrame(system):
    system.createTable("")
    return pandas.DataFrame(system.createTable(""))

def calcproperties(gascondensateFluid, inputDict):
    properties = neqsim.util.generator.PropertyGenerator(gascondensateFluid, JDouble[:](inputDict['temperature']), JDouble[:](inputDict['pressure']))
    props = properties.calculate()
    calculatedProperties= ({k: list(v) for k, v in props.items()})
    df = pandas.DataFrame(calculatedProperties)
    return df

def separatortest(fluid, pressure, temperature, GOR=[], Bo=[], display=False):
    length =len(pressure)
    sepSim = neqsim.PVTsimulation.simulation.SeparatorTest(fluid)
    sepSim.setSeparatorConditions(JDouble[:](temperature), JDouble[:](pressure))
    sepSim.runCalc()
    for i in range(0,length):
        GOR.append(sepSim.getGOR()[i])
        Bo.append(sepSim.getBofactor()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, Bo, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('Bo [m3/Sm3]')
        plt.figure()
        plt.plot(pressure, GOR, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('GOR [Sm3/Sm3]')
        plt.figure()

def CVD(fluid, pressure, temperature, relativeVolume=[],liquidrelativevolume=[], Zgas=[],Zmix=[],cummulativemolepercdepleted=[], display=False):
    length =len(pressure)
    cvdSim = neqsim.PVTsimulation.simulation.ConstantVolumeDepletion(fluid)
    cvdSim.setPressures(JDouble[:](pressure))
    cvdSim.setTemperature(temperature)
    cvdSim.runCalc()
    for i in range(0,length):
        Zgas.append(cvdSim.getZgas()[i])
        Zmix.append(cvdSim.getZmix()[i])
        liquidrelativevolume.append(cvdSim.getLiquidRelativeVolume()[i])
        relativeVolume.append(cvdSim.getRelativeVolume()[i])
        cummulativemolepercdepleted.append(cvdSim.getCummulativeMolePercDepleted()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, Zgas, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('Zgas [-]')
        plt.figure()
        plt.plot(pressure, relativeVolume, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('relativeVolume [-]')
        plt.figure()

def viscositysim(fluid, pressure, temperature, gasviscosity=[], oilviscosity=[],aqueousviscosity=[], display=False):
    length =len(pressure)
    cmeSim = neqsim.PVTsimulation.simulation.ViscositySim(fluid)
    cmeSim.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    cmeSim.runCalc()
    for i in range(0,length):
        gasviscosity.append(cmeSim.getGasViscosity()[i])
        oilviscosity.append(cmeSim.getOilViscosity()[i])
        aqueousviscosity.append(cmeSim.getAqueousViscosity()[i])
    if display:
        plt.figure()
        plt.plot(pressure, gasviscosity, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('gasviscosity [kg/msec]')
        plt.figure()
        plt.plot(pressure, oilviscosity, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('oilviscosity [kg/msec]')
        plt.figure()

def CME(fluid, pressure, temperature, saturationPressure, relativeVolume=[], liquidrelativevolume=[], Zgas=[], Yfactor=[], isothermalcompressibility=[], density=[],Bg=[], viscosity=[], display=False):
    length =len(pressure)
    cvdSim = neqsim.PVTsimulation.simulation.ConstantMassExpansion(fluid)    
    cvdSim.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    cvdSim.runCalc()
    saturationPressure=cvdSim.getSaturationPressure()
    for i in range(0,length):
        Zgas.append(cvdSim.getZgas()[i])
        relativeVolume.append(cvdSim.getRelativeVolume()[i])
        liquidrelativevolume.append(cvdSim.getLiquidRelativeVolume()[i])
        Yfactor.append(cvdSim.getYfactor()[i])
        isothermalcompressibility.append(cvdSim.getIsoThermalCompressibility()[i])
        Bg.append(cvdSim.getBg()[i])
        density.append(cvdSim.getDensity()[i])
        viscosity.append(cvdSim.getViscosity()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, Zgas, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('Zgas [-]')
        plt.figure()
        plt.plot(pressure, relativeVolume, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('relativeVolume [-]')
        plt.figure()

def difflib(fluid, pressure, temperature, relativeVolume = [], Bo=[], Bg=[], relativegravity=[], Zgas=[], gasstandardvolume=[], Rs=[], oildensity=[], gasgravity=[], display=False):
    length =len(pressure)
    cvdSim = neqsim.PVTsimulation.simulation.DifferentialLiberation(fluid)
    cvdSim.setPressures(JDouble[:](pressure))
    cvdSim.setTemperature(temperature)
    cvdSim.runCalc()
    for i in range(0,length):
        Zgas.append(cvdSim.getZgas()[i])
        Bo.append(cvdSim.getBo()[i])
        Bg.append(cvdSim.getBg()[i])
        Zgas.append(cvdSim.getZgas()[i])
        relativegravity.append(cvdSim.getRelGasGravity()[i])
        relativeVolume.append(cvdSim.getRelativeVolume())
        gasstandardvolume.append(cvdSim.getGasStandardVolume()[i])
        Rs.append(cvdSim.getRs()[i])
        oildensity.append(cvdSim.getOilDensity()[i])
        gasgravity.append(cvdSim.getRelGasGravity()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, Zgas, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('Zgas [-]')
        plt.figure()
        plt.plot(pressure, relativeVolume, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('relativeVolume [-]')
        plt.figure()

def GOR(fluid, pressure, temperature, GORdata=[], Bo=[],  display=False):
    length =len(pressure)
    GOR = neqsim.PVTsimulation.simulation.GOR(fluid)
    GOR.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    GOR.runCalc()
    for i in range(0,length):
        GORdata.append(GOR.getGOR()[i])
        Bo.append(GOR.getBofactor()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, GOR, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('GOR [Sm3/Sm3]')

def saturationpressure(fluid, temperature=-1.0):
    if(temperature>0):
         fluid.setTemperature(temperature)
    cvdSim = neqsim.PVTsimulation.simulation.SaturationPressure(fluid)
    cvdSim.run()
    return cvdSim.getSaturationPressure()

def swellingtest(fluid, fluid2, temperature, cummulativeMolePercentGasInjected, pressure = [], relativeoilvolume=[], display=False):
    length2 =len(cummulativeMolePercentGasInjected)
    cvdSim = neqsim.PVTsimulation.simulation.SwellingTest(fluid)
    cvdSim.setInjectionGas(fluid2)
    cvdSim.setTemperature(temperature)
    cvdSim.setCummulativeMolePercentGasInjected(JDouble[:](cummulativeMolePercentGasInjected))
    cvdSim.runCalc()
    for i in range(0,length2):
        relativeoilvolume.append(cvdSim.getRelativeOilVolume()[i])
        pressure.append(cvdSim.getPressures()[i])
        i = i+1
    if display:
        plt.figure()
        plt.plot(pressure, relativeoilvolume, "o")
        plt.xlabel('Pressure [bara]')
        plt.ylabel('relativeoilvolume [-]')

def printFrame(system):
    system.createTable("")
    print(pandas.DataFrame(system.createTable("")).to_string(header=False, index=False))

def printFluid(system):
    a = system.getResultTable()
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end='\t')
    print()

def volumecorrection(system, use=1):
    system.useVolumeCorrection(use)


def write(system, filename, newfile=0):
    system.write(filename, filename, newfile)


def appenddatabase(system):
    system.createDatabase(0)


def show(system):
    system.display()


def showPDF(system):
    system.generatePDF()
    system.displayPDF()


def addComponent(thermoSystem, name, moles, unit="no", phase=-10):
    if phase == -10 and unit == "no":
        thermoSystem.addComponent(name, moles)
    elif phase == -10:
        thermoSystem.addComponent(name, moles, unit)
    elif unit == "no":
        thermoSystem.addComponent(name, moles, phase)
    else:
        thermoSystem.addComponent(name, moles, unit, phase)


def temperature(thermoSystem, temp, phase=-1):
    if phase == -1:
        thermoSystem.setTemperature(temp)
    else:
        thermoSystem.getPhase(phase).setTemperature(temp)


def pressure(thermoSystem, pres, phase=-1):
    if phase == -1:
        thermoSystem.setPressure(pres)
    else:
        thermoSystem.getPhase(phase).setPressure(pres)


def reactionCheck(thermoSystem):
    thermoSystem.chemicalReactionInit()


def mixingRule(thermoSystem, mixRule='classic', GEmodel=''):
    if GEmodel == '':
        thermoSystem.setMixingRule(mixRule)
    else:
        thermoSystem.setMixingRule(mixRule, GEmodel)


def multiphase(testSystem, multiphase=1):
    testSystem.setMultiPhaseCheck(multiphase)


def solidcheck(testSystem, solid=1):
    testSystem.setSolidPhaseCheck(solid)


def solid(testSystem, solid=1):
    testSystem.setSolidPhaseCheck(solid)

def GCV(testSystem, unit):
    referenceTemperatureVolume = 15.0
    referenceTemperatureCombustion = 15.0
    numberUnit = 'mass'
    iso6976 = ISO6976(testSystem)
    iso6976.setReferenceType(numberUnit)
    iso6976.setVolRefT(referenceTemperatureVolume)
    iso6976.setEnergyRefT(referenceTemperatureCombustion)
    iso6976.calculate()
    return iso6976.getValue("SuperiorCalorificValue")

def watersaturate(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.saturateWithWater()
    testSystem.init(3)

def TPflash(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPflash()
    testSystem.init(3)

def TPgradientFlash(testSystem, height, temperature):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPgradientFlash(height,temperature)
    
def TVflash(testSystem, volume, unit="m3"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TVflash(volume, unit)
    testSystem.init(3)

def TSflash(testSystem, entropy, unit="J/K"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TSflash(entropy, unit)
    testSystem.init(3)
    
def VSflash(testSystem, volume, entropy, unitVol= "m3", unit="J/K"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VSflash(volume, entropy, unitVol, unit)
    testSystem.init(3)
    
def VHflash(testSystem, volume, enthalpy, unitVol= "m3", unit="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VHflash(volume, enthalpy, unitVol, unit)
    testSystem.init(3)

def VUflash(testSystem, volume, energy, unitVol= "m3", unit="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VUflash(volume, energy, unitVol, unit)
    testSystem.init(3)
    
def PUflash(testSystem, pressure, energy, unitPressure= "bara", unitEnergy="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testSystem.setPressure(pressure, unitPressure) 
    testFlash.PUflash(energy, unitEnergy)
    testSystem.init(3)
    
def PVTpropTable(fluid1, fileName, lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.OLGApropTable(lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps, fileName, 0)
    testFlash.displayResult()

def TPsolidflash(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPSolidflash()

def PHflash(testSystem, enthalpy, unit="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PHflash(enthalpy, unit)
    
def PHsolidflash(testSystem, enthalpy):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PHsolidFlash(enthalpy)

def PSflash(testSystem, entropy, unit="J/K"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PSflash(entropy, unit)

def freeze(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.freezingPointTemperatureFlash()
    
def scaleCheck(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.checkScalePotential(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()

def ionComposition(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.calcIonComposition(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()


def hydp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.hydrateFormationPressure()

def addfluids(fluid1, fluid2):
    return neqsim.thermo.system.SystemInterface.addFluids(fluid1,fluid2)

def hydt(testSystem, type=1):
    if not testSystem.doHydrateCheck():
        testSystem.setHydrateCheck(True)
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.hydrateFormationTemperature(type)
    return testSystem.getTemperature()

def calcIonComposition(fluid1):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.calcIonComposition(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()
    
def checkScalePotential(fluid1):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.checkScalePotential(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()

def bubp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.bubblePointPressureFlash(0)
    except:
        print('error calculating bublepoint')
    return testSystem.getPressure()

def bubt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.bubblePointTemperatureFlash()
    except:
        print('error calculating bublepoint')
    return testSystem.getTemperature()


def dewp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointPressureFlash()
    except:
        print('error could not calculate')
    return testSystem.getPressure()


def dewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointTemperatureFlash()
    except:
        print('error could not calculate')
    return testSystem.getTemperature()


def waterdewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.waterDewPointTemperatureFlash()
    except:
        print('error could not calculate')
    return testSystem.getTemperature()


def phaseenvelope(testSystem, plot=False):
    testFlash = ThermodynamicOperations(testSystem.clone())
    testFlash.calcPTphaseEnvelope()
    data = testFlash
    if(plot):
        plt.plot(list(data.getOperation().get("dewT") ),list(data.getOperation().get("dewP")), label="dew point")
        plt.plot(list(data.getOperation().get("bubT")),list(data.getOperation().get("bubP")), label="bubble point")

        try:
            plt.plot(list(data.getOperation().get("dewT2")),list(data.getOperation().get("dewP2")), label="dew point2")
        except:
            pass
            #print("An exception occurred")

        try:
            plt.plot(list(data.getOperation().get("bubT2")),list(data.getOperation().get("bubP2")), label="bubble point2")
        except:
            pass
            #print("An exception occurred")
        
        plt.title('PT envelope')
        plt.xlabel('Temperature [K]')
        plt.ylabel('Pressure [bar]')
        plt.legend()
        plt.show()
    return testFlash

def fluidComposition(testSystem, composition):
    testSystem.setMolarComposition(JDouble[:](composition))
    testSystem.init(0)

def fluidCompositionPlus(testSystem, composition):
    testSystem.setMolarCompositionPlus(JDouble[:](composition))
    testSystem.init(0)

def getExtThermProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    nargout[0] = function[0]() / thermoSystem.getNumberOfMoles()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            nargout[2] = 0
        else:
            nargout[2] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            nargout[1] = 0
    else:
        nargout[1] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
        nargout[2] = function[2]() / thermoSystem.getPhase(1).getNumberOfMolesInPhase()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def getIntThermProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    nargout[0] = function[0]()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]()
            nargout[2] = 0
        else:
            nargout[2] = function[1]()
            nargout[1] = 0
    else:
        nargout[1] = function[1]()
        nargout[2] = function[2]()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def getPhysProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    thermoSystem.initPhysicalProperties()
    nargout[0] = function[0]()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]()
            nargout[2] = 0
        else:
            nargout[2] = function[1]()
            nargout[1] = 0
    else:
        nargout[1] = function[1]()
        nargout[2] = function[2]()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def enthalpy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getEnthalpy)
    func.append(thermoSystem.getPhase(0).getEnthalpy)
    func.append(thermoSystem.getPhase(1).getEnthalpy)
    return getExtThermProp(func, thermoSystem, t, p)


def entropy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getEntropy)
    func.append(thermoSystem.getPhase(0).getEntropy)
    func.append(thermoSystem.getPhase(1).getEntropy)
    return getExtThermProp(func, thermoSystem, t, p)

def densityGERG2008(phase):
    GERG2008 = neqsim.thermo.util.GERG.NeqSimGERG2008()
    return GERG2008.getDensity(phase)

def molvol(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getMolarVolume)
    func.append(thermoSystem.getPhase(0).getMolarVolume)
    func.append(thermoSystem.getPhase(1).getMolarVolume)
    return getIntThermProp(func, thermoSystem, t, p)


def energy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getInternalEnergy)
    func.append(thermoSystem.getPhase(0).getInternalEnergy)
    func.append(thermoSystem.getPhase(1).getInternalEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def gibbsenergy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getGibbsEnergy)
    func.append(thermoSystem.getPhase(0).getGibbsEnergy)
    func.append(thermoSystem.getPhase(1).getGibbsEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def helmholtzenergy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(0).getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(1).getHelmholtzEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def molefrac(thermoSystem, comp, t=0, p=0):
    func = []
    func.append(thermoSystem.getPhase(0).getComponent(comp).getz)
    func.append(thermoSystem.getPhase(0).getComponent(comp).getx)
    func.append(thermoSystem.getPhase(1).getComponent(comp).getx)
    return getIntThermProp(func, thermoSystem, t, p)


def moles(thermoSystem, phase=0):
    if phase == 0:
        return thermoSystem.getNumberOfMoles()
    else:
        return thermoSystem.getPhase(phase).getNumberOfMolesInPhase()


def beta(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getBeta)
    func.append(thermoSystem.getPhase(0).getBeta)
    func.append(thermoSystem.getPhase(1).getBeta)
    return getIntThermProp(func, thermoSystem, t, p)


def molarmass(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getMolarMass)
    func.append(thermoSystem.getPhase(0).getMolarMass)
    func.append(thermoSystem.getPhase(1).getMolarMass)
    return getIntThermProp(func, thermoSystem, t, p)


def Z(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getZ)
    func.append(thermoSystem.getPhase(0).getZ)
    func.append(thermoSystem.getPhase(1).getZ)
    return getIntThermProp(func, thermoSystem, t, p)


def density(thermoSystem, volcor=1, t=0, p=0):
    func = []
    func.append(thermoSystem.getDensity)
    if volcor == 1:
        thermoSystem.initPhysicalProperties()
        func.append(thermoSystem.getPhase(0).getPhysicalProperties().getDensity)
        func.append(thermoSystem.getPhase(1).getPhysicalProperties().getDensity)
    else:
        func.append(thermoSystem.getPhase(0).getDensity)
        func.append(thermoSystem.getPhase(1).getDensity)
    return getPhysProp(func, thermoSystem, t, p)


def viscosity(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(1).getPhysicalProperties().getViscosity)
    return getPhysProp(func, thermoSystem, t, p)

def WAT(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.calcWAT()
    testSystem.init(3)
    return testSystem.getTemperature()