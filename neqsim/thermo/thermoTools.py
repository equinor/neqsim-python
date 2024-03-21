from typing import List, Union
import jpype
import pandas
from jpype.types import *
from neqsim import has_matplotlib, has_tabulate
from neqsim.neqsimpython import jNeqSim
from neqsim.standards import ISO6976

if has_matplotlib():
    import matplotlib.pyplot as plt

ThermodynamicOperations = jNeqSim.thermodynamicOperations.ThermodynamicOperations
fluidcreator = jNeqSim.thermo.Fluid()
fluid_type = {
    "srk": jNeqSim.thermo.system.SystemSrkEos,
    "SRK-EoS": jNeqSim.thermo.system.SystemSrkEos,
    "Psrk-EoS": jNeqSim.thermo.system.SystemPsrkEos,
    "PSRK-EoS": jNeqSim.thermo.system.SystemPsrkEos,
    "RK-EoS": jNeqSim.thermo.system.SystemRKEos,
    "pr": jNeqSim.thermo.system.SystemPrEos,
    "PR-EoS": jNeqSim.thermo.system.SystemPrEos,
    "pr-umr": jNeqSim.thermo.system.SystemUMRPRUMCEos,
    "srk-s": jNeqSim.thermo.system.SystemSrkSchwartzentruberEos,
    "GERG-water": jNeqSim.thermo.system.SystemGERGwaterEos,
    "SRK-MC": jNeqSim.thermo.system.SystemSrkMathiasCopeman,
    "PR-MC": jNeqSim.thermo.system.SystemPrMathiasCopeman,
    "scrk": jNeqSim.thermo.system.SystemSrkSchwartzentruberEos,
    "ScRK-EoS": jNeqSim.thermo.system.SystemSrkSchwartzentruberEos,
    "nrtl": jNeqSim.thermo.system.SystemNRTL,
    "unifac": jNeqSim.thermo.system.SystemUNIFAC,
    "electrolyte": jNeqSim.thermo.system.SystemFurstElectrolyteEos,
    "Electrolyte-ScRK-EoS": jNeqSim.thermo.system.SystemFurstElectrolyteEos,
    "Electrolyte-CPA-EoS": jNeqSim.thermo.system.SystemElectrolyteCPAstatoil,
    "cpa-el": jNeqSim.thermo.system.SystemElectrolyteCPA,
    "cpa-s": jNeqSim.thermo.system.SystemSrkCPAs,
    "cpa-statoil": jNeqSim.thermo.system.SystemSrkCPAstatoil,
    "cpa": jNeqSim.thermo.system.SystemSrkCPAstatoil,
    "CPA-SRK-EoS": jNeqSim.thermo.system.SystemSrkCPA,
    "cpa-srk": jNeqSim.thermo.system.SystemSrkCPA,
    "srk-twoCoon": jNeqSim.thermo.system.SystemSrkTwuCoonParamEos,
    "cpa-pr": jNeqSim.thermo.system.SystemPrCPA,
    "CPA-PR-EoS": jNeqSim.thermo.system.SystemPrCPA,
    "SRK-TwuCoon-EOS": jNeqSim.thermo.system.SystemSrkTwuCoonStatoilEos,
}


def fluid(name="srk", temperature=298.15, pressure=1.01325):
    fluid_function = fluid_type.get(name, jNeqSim.thermo.system.SystemSrkEos)
    return fluid_function(temperature, pressure)


def readEclipseFluid(filename, wellName=""):
    jNeqSim.thermo.util.readwrite.EclipseFluidReadWrite.pseudoName = wellName
    fluid1 = jNeqSim.thermo.util.readwrite.EclipseFluidReadWrite.read(filename)
    return fluid1


def setEclipseComposition(fluid, filename, wellName=""):
    jNeqSim.thermo.util.readwrite.EclipseFluidReadWrite.pseudoName = wellName
    jNeqSim.thermo.util.readwrite.EclipseFluidReadWrite.setComposition(fluid, filename)


def addFluids(fluids):
    fluid = fluids[0].clone()
    numberOfFluids = len(fluids)
    for i in range(numberOfFluids - 1):
        fluid.addFluid(fluids[i + 1])
    return fluid


def fluid_df(
    reservoirFluiddf,
    lastIsPlusFraction=False,
    autoSetModel=False,
    modelName="",
    lumpComponents=True,
    numberOfLumpedComponents=12,
    add_all_components=True,
):
    if autoSetModel:
        fluidcreator.setAutoSelectModel(True)
    else:
        fluidcreator.setAutoSelectModel(False)
    if modelName:
        fluidcreator.setThermoModel(modelName)
    else:
        fluidcreator.setAutoSelectModel(False)
    TBPComponentsFrame = reservoirFluiddf.dropna()
    if not add_all_components:
        reservoirFluiddf = reservoirFluiddf[
            reservoirFluiddf["MolarComposition[-]"] != 0.0
        ]
        TBPComponentsFrame = TBPComponentsFrame[
            TBPComponentsFrame["MolarComposition[-]"] > 0
        ]
    else:
        TBPComponentsFrame = reservoirFluiddf.dropna()
    if "MolarMass[kg/mol]" in reservoirFluiddf:
        definedComponentsFrame = reservoirFluiddf[
            reservoirFluiddf["MolarMass[kg/mol]"].isnull()
        ]
    else:
        definedComponentsFrame = reservoirFluiddf
    if not add_all_components:
        definedComponentsFrame = definedComponentsFrame[
            definedComponentsFrame["MolarComposition[-]"] > 0.0
        ]
    if definedComponentsFrame.size > 0:
        fluid7 = createfluid2(
            definedComponentsFrame["ComponentName"].tolist(),
            definedComponentsFrame["MolarComposition[-]"].tolist(),
        )
    else:
        fluid7 = fluid("srk")
    if not TBPComponentsFrame.equals(reservoirFluiddf) and TBPComponentsFrame.size > 0:
        addOilFractions(
            fluid7,
            TBPComponentsFrame["ComponentName"].tolist(),
            TBPComponentsFrame["MolarComposition[-]"].tolist(),
            TBPComponentsFrame["MolarMass[kg/mol]"].tolist(),
            TBPComponentsFrame["RelativeDensity[-]"].tolist(),
            lastIsPlusFraction,
            lumpComponents,
            numberOfLumpedComponents,
        )
    return fluid7


def createfluid(fluid_type="dry gas"):
    return fluidcreator.create(fluid_type)


def createfluid2(names, molefractions=None, unit="mol/sec"):
    if molefractions is None:
        fluidcreator.create2(JString[:](names))
    return fluidcreator.create2(JString[:](names), JDouble[:](molefractions), unit)


def addOilFractions(
    fluid,
    charNames,
    molefractions,
    molarMass,
    density,
    lastIsPlusFraction=False,
    lumpComponents=True,
    numberOfPseudoComponents=12,
):
    fluid.addOilFractions(
        JString[:](charNames),
        JDouble[:](molefractions),
        JDouble[:](molarMass),
        JDouble[:](density),
        lastIsPlusFraction,
        lumpComponents,
        numberOfPseudoComponents,
    )


def newdatabase(system):
    system.createDatabase(1)


def tunewaxmodel(fluid, experimentaldata, maxiterations=5):
    tempList = [x + 273.15 for x in experimentaldata["temperature"]]
    presList = experimentaldata["pressure"]
    expList = [[x * 100.0 for x in experimentaldata["experiment"]]]

    waxsim = jNeqSim.PVTsimulation.simulation.WaxFractionSim(fluid)
    waxsim.setTemperaturesAndPressures(JDouble[:](tempList), JDouble[:](presList))
    waxsim.setExperimentalData(JDouble[:, :](expList))
    waxsim.getOptimizer().setNumberOfTuningParameters(3)
    waxsim.getOptimizer().setMaxNumberOfIterations(maxiterations)
    waxsim.runTuning()
    waxsim.runCalc()

    results = {
        "temperature": tempList,
        "pressure": presList,
        "experiment": expList,
        "results": list(waxsim.getWaxFraction()),
        "parameters": list(
            waxsim.getOptimizer()
            .getSampleSet()
            .getSample(0)
            .getFunction()
            .getFittingParams()
        ),
    }
    return results


def data(system):
    a = system.getResultTable()
    return a


def table(system):
    # todo: convert to class method
    return system.createTable("")


def dataFrame(system):
    # todo: convert to class method
    return pandas.DataFrame(table(system)).astype(str)


def calcproperties(gascondensateFluid, inputDict):
    properties = jNeqSim.util.generator.PropertyGenerator(
        gascondensateFluid,
        JDouble[:](inputDict["temperature"]),
        JDouble[:](inputDict["pressure"]),
    )
    props = properties.calculate()
    calculatedProperties = {k: list(v) for k, v in props.items()}
    df = pandas.DataFrame(calculatedProperties)
    return df


def fluidflashproperties(
    spec1: pandas.Series,
    spec2: pandas.Series,
    mode: Union[int, str] = 1,
    system=None,
    components: List[str] = None,
    fractions: list = None,
):
    """Perform flash and return fluid properties for a series of process properties.


    Args:
        spec1 (pandas.Series): Process condition to perform flash at. Type depends on mode argument, see below for units.
        spec2 (pandas.Series): Process condition to perform flash at. Type depends on mode argument, see below for units.
        mode (int, str): Supported flash modes: PT or TP (1), PH (2) and PS (3). Defaults to 1.
        system (_type_, optional): A default system is created if not passed and components and fractions can specify it.
        components (list, optional): List of component names. Defaults to None, which requires a system input.
        fractions (list, optional): List of fractions if same for all flashes or list of list of fractions per flash. Defaults to None, which requires a system input..

    Raises:
        ValueError: Invalid Mode input
        ValueError: Invalid combination of system, components and fractions.
        TypeError: Fraction must be list if provided.
        NotImplementedError: _description_
        NotImplementedError: _description_

    Returns:
        _type_: _description_


        Input units:
            - Flash pressure in bar absolute.
            - Temperature in Kelvin
            - Entalphy in J/mol
            - Entropy in J/molK.

    Pressure shall be specified as bara,
    Fractions can be a single list of component fractions to use for all flashes or a list of lists where the first dimension the different components and the second dimension is the fraction per flash.
    Same component list is used for all flashes.
    """
    if isinstance(mode, int):
        if mode == 1:
            # Convert to PT
            temp = spec1
            spec1 = spec2
            spec2 = temp
    elif isinstance(mode, str):
        if mode == "PT":
            mode = 1
        elif mode == "TP":
            mode = 1
            # Convert to PT
            temp = spec1
            spec1 = spec2
            spec2 = temp
        elif mode == "PH":
            mode = 2
        elif mode == "PS":
            mode = 3

    if not isinstance(mode, int) or mode < 1 or mode > 3:
        raise ValueError("Mode must be in 'TP' or 1, 'PH' or 2 or 'PS' or 3")

    if system is None:
        if components is None or fractions is None:
            raise ValueError(
                "if system is not specified, components and fractions must be specified."
            )

        system = jNeqSim.thermo.system.SystemSrkEos(273.15, 1.01325)
        if not isinstance(components, list):
            components = [components]

        system.addComponents(components)

        # Single component
        if not isinstance(fractions, list):
            fractions = [fractions]

        if not all([isinstance(x, list) for x in fractions]):
            system.setTotalNumberOfMoles(1)
            system.setMolarComposition(fractions)

    thermoOps = jNeqSim.thermodynamicOperations.ThermodynamicOperations(system)

    if isinstance(spec1, pandas.Series):
        spec1 = spec1.to_list()
    elif not isinstance(spec1, list):
        spec1 = [spec1]
    jSpec1 = jpype.java.util.ArrayList()
    [jSpec1.add(float(x)) for x in spec1]

    if isinstance(spec2, pandas.Series):
        spec2 = spec2.to_list()
    elif not isinstance(spec2, list):
        spec2 = [spec2]
    jSpec2 = jpype.java.util.ArrayList()
    [jSpec2.add(float(x)) for x in spec2]

    if fractions is not None:
        if not isinstance(fractions, list):
            raise TypeError("Fractions must be a list if provided")
        if components is not None:
            if not isinstance(components, list):
                components = [components]

            if all([isinstance(x, list) for x in components]):
                raise NotImplementedError("Component list must be fixed if provided")
            elif any([isinstance(x, list) for x in components]):
                raise NotImplementedError("Component list must be fixed if provided")
            else:
                components = None

        if all([isinstance(x, list) for x in fractions]):
            # pivot fractions
            num_components = len(fractions)
            jFractions = jpype.java.util.ArrayList()
            for k_comp in range(0, num_components):
                jComp = jpype.java.util.ArrayList()
                [jComp.add(x) for x in fractions[k_comp]]
                jFractions.add(jComp)

            fractions = jFractions
        elif any([isinstance(x, list) for x in fractions]):
            pass
            # raise NotImplementedError
        else:
            fractions = None

    return thermoOps.propertyFlash(jSpec1, jSpec2, mode, components, fractions)


def separatortest(fluid, pressure, temperature, GOR=None, Bo=None, display=False):
    if GOR is None:
        GOR = []

    if Bo is None:
        Bo = []

    length = len(pressure)
    sepSim = jNeqSim.PVTsimulation.simulation.SeparatorTest(fluid)
    sepSim.setSeparatorConditions(JDouble[:](temperature), JDouble[:](pressure))
    sepSim.runCalc()
    for i in range(0, length):
        GOR.append(sepSim.getGOR()[i])
        Bo.append(sepSim.getBofactor()[i])
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, Bo, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("Bo [m3/Sm3]")
            plt.figure()
            plt.plot(pressure, GOR, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("GOR [Sm3/Sm3]")
            plt.figure()
        else:
            raise Exception("Package matplotlib is not installed")


def CVD(
    fluid,
    pressure,
    temperature,
    relativeVolume=None,
    liquidrelativevolume=None,
    Zgas=None,
    Zmix=None,
    cummulativemolepercdepleted=None,
    display=False,
):
    if relativeVolume is None:
        relativeVolume = []

    if liquidrelativevolume is None:
        liquidrelativevolume = []

    if Zgas is None:
        Zgas = []

    if Zmix is None:
        Zmix = []

    if cummulativemolepercdepleted is None:
        cummulativemolepercdepleted = []

    length = len(pressure)
    cvdSim = jNeqSim.PVTsimulation.simulation.ConstantVolumeDepletion(fluid)
    cvdSim.setPressures(JDouble[:](pressure))
    cvdSim.setTemperature(temperature)
    cvdSim.runCalc()
    for i in range(0, length):
        Zgas.append(cvdSim.getZgas()[i])
        Zmix.append(cvdSim.getZmix()[i])
        liquidrelativevolume.append(cvdSim.getLiquidRelativeVolume()[i])
        relativeVolume.append(cvdSim.getRelativeVolume()[i])
        cummulativemolepercdepleted.append(cvdSim.getCummulativeMolePercDepleted()[i])
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, Zgas, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("Zgas [-]")
            plt.figure()
            plt.plot(pressure, relativeVolume, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("relativeVolume [-]")
            plt.figure()
        else:
            raise Exception("Package matplotlib is not installed")


def viscositysim(
    fluid,
    pressure,
    temperature,
    gasviscosity=None,
    oilviscosity=None,
    aqueousviscosity=None,
    display=False,
):
    if gasviscosity is None:
        gasviscosity = []

    if oilviscosity is None:
        oilviscosity = []

    if aqueousviscosity is None:
        aqueousviscosity = []
    length = len(pressure)
    cmeSim = jNeqSim.PVTsimulation.simulation.ViscositySim(fluid)
    cmeSim.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    cmeSim.runCalc()
    for i in range(0, length):
        gasviscosity.append(cmeSim.getGasViscosity()[i])
        oilviscosity.append(cmeSim.getOilViscosity()[i])
        aqueousviscosity.append(cmeSim.getAqueousViscosity()[i])
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, gasviscosity, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("gasviscosity [kg/msec]")
            plt.figure()
            plt.plot(pressure, oilviscosity, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("oilviscosity [kg/msec]")
            plt.figure()
        else:
            raise Exception("Package matplotlib is not installed")


def CME(
    fluid,
    pressure,
    temperature,
    saturationPressure,
    relativeVolume=None,
    liquidrelativevolume=None,
    Zgas=None,
    Yfactor=None,
    isothermalcompressibility=None,
    density=None,
    Bg=None,
    viscosity=None,
    display=False,
):
    if relativeVolume is None:
        relativeVolume = []

    if liquidrelativevolume is None:
        liquidrelativevolume = []

    if Zgas is None:
        Zgas = []

    if Yfactor is None:
        Yfactor = []

    if isothermalcompressibility is None:
        isothermalcompressibility = []

    if density is None:
        density = []

    if Bg is None:
        Bg = []

    if viscosity is None:
        viscosity = []

    length = len(pressure)
    cvdSim = jNeqSim.PVTsimulation.simulation.ConstantMassExpansion(fluid)
    cvdSim.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    cvdSim.runCalc()
    saturationPressure = cvdSim.getSaturationPressure()
    for i in range(0, length):
        Zgas.append(cvdSim.getZgas()[i])
        relativeVolume.append(cvdSim.getRelativeVolume()[i])
        liquidrelativevolume.append(cvdSim.getLiquidRelativeVolume()[i])
        Yfactor.append(cvdSim.getYfactor()[i])
        isothermalcompressibility.append(cvdSim.getIsoThermalCompressibility()[i])
        Bg.append(cvdSim.getBg()[i])
        density.append(cvdSim.getDensity()[i])
        viscosity.append(cvdSim.getViscosity()[i])
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, Zgas, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("Zgas [-]")
            plt.figure()
            plt.plot(pressure, relativeVolume, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("relativeVolume [-]")
            plt.figure()
        else:
            raise Exception("Package matplotlib is not installed")


def difflib(
    fluid,
    pressure,
    temperature,
    relativeVolume=None,
    Bo=None,
    Bg=None,
    relativegravity=None,
    Zgas=None,
    gasstandardvolume=None,
    Rs=None,
    oildensity=None,
    gasgravity=None,
    display=False,
):
    if relativeVolume is None:
        relativeVolume = []

    if Bo is None:
        Bo = []

    if Bg is None:
        Bg = []

    if relativegravity is None:
        relativegravity = []

    if Zgas is None:
        Zgas = []

    if gasstandardvolume is None:
        gasstandardvolume = []

    if Rs is None:
        Rs = []

    if oildensity is None:
        oildensity = []

    if gasgravity is None:
        gasgravity = []

    length = len(pressure)
    cvdSim = jNeqSim.PVTsimulation.simulation.DifferentialLiberation(fluid)
    cvdSim.setPressures(JDouble[:](pressure))
    cvdSim.setTemperature(temperature)
    cvdSim.runCalc()
    for i in range(0, length):
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
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, Zgas, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("Zgas [-]")
            plt.figure()
            plt.plot(pressure, relativeVolume, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("relativeVolume [-]")
            plt.figure()
        else:
            raise Exception("Package matplotlib is not installed")


def GOR(fluid, pressure, temperature, GORdata=None, Bo=None, display=False):
    if GORdata is None:
        GORdata = []

    if Bo is None:
        Bo = []

    length = len(pressure)
    jGOR = jNeqSim.PVTsimulation.simulation.GOR(fluid)
    jGOR.setTemperaturesAndPressures(JDouble[:](temperature), JDouble[:](pressure))
    jGOR.runCalc()
    for i in range(0, length):
        GORdata.append(jGOR.getGOR()[i])
        Bo.append(jGOR.getBofactor()[i])
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, GORdata, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("GOR [Sm3/Sm3]")
        else:
            raise Exception("Package matplotlib is not installed")


def saturationpressure(fluid, temperature=-1.0):
    if temperature > 0:
        fluid.setTemperature(temperature)
    cvdSim = jNeqSim.PVTsimulation.simulation.SaturationPressure(fluid)
    cvdSim.run()
    return cvdSim.getSaturationPressure()


def swellingtest(
    fluid,
    fluid2,
    temperature,
    cummulativeMolePercentGasInjected,
    pressure=None,
    relativeoilvolume=None,
    display=False,
):
    if pressure is None:
        pressure = []

    if relativeoilvolume is None:
        relativeoilvolume = []
    length2 = len(cummulativeMolePercentGasInjected)
    cvdSim = jNeqSim.PVTsimulation.simulation.SwellingTest(fluid)
    cvdSim.setInjectionGas(fluid2)
    cvdSim.setTemperature(temperature)
    cvdSim.setCummulativeMolePercentGasInjected(
        JDouble[:](cummulativeMolePercentGasInjected)
    )
    cvdSim.runCalc()
    for i in range(0, length2):
        relativeoilvolume.append(cvdSim.getRelativeOilVolume()[i])
        pressure.append(cvdSim.getPressures()[i])
        i = i + 1
    if display:
        if has_matplotlib():
            plt.figure()
            plt.plot(pressure, relativeoilvolume, "o")
            plt.xlabel("Pressure [bara]")
            plt.ylabel("relativeoilvolume [-]")
        else:
            raise Exception("Package matplotlib is not installed")


def printFrame(system):
    if has_tabulate():
        print(dataFrame(system).to_markdown(index=False))
    else:
        print(dataFrame(system))


def printFluid(system):
    a = system.getResultTable()
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end="\t")
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


def mixingRule(thermoSystem, mixRule="classic", GEmodel=""):
    if GEmodel == "":
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
    numberUnit = "mass"
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


def TPflash(testSystem, temperature=None, tUnit=None, pressure=None, pUnit=None):
    if temperature is not None:
        if tUnit is None:
            tUnit = "K"
        testSystem.setTemperature(temperature, tUnit)
    if pressure is not None:
        if pUnit is None:
            pUnit = "bara"
        testSystem.setPressure(pressure, pUnit)
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPflash()
    testSystem.init(3)


def TPgradientFlash(testSystem, height, temperature):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPgradientFlash(height, temperature)


def TVflash(testSystem, volume, unit="m3"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TVflash(volume, unit)
    testSystem.init(3)


def TSflash(testSystem, entropy, unit="J/K"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TSflash(entropy, unit)
    testSystem.init(3)


def VSflash(testSystem, volume, entropy, unitVol="m3", unit="J/K"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VSflash(volume, entropy, unitVol, unit)
    testSystem.init(3)


def VHflash(testSystem, volume, enthalpy, unitVol="m3", unit="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VHflash(volume, enthalpy, unitVol, unit)
    testSystem.init(3)


def VUflash(testSystem, volume, energy, unitVol="m3", unit="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.VUflash(volume, energy, unitVol, unit)
    testSystem.init(3)


def PUflash(testSystem, pressure, energy, unitPressure="bara", unitEnergy="J"):
    testFlash = ThermodynamicOperations(testSystem)
    testSystem.setPressure(pressure, unitPressure)
    testFlash.PUflash(energy, unitEnergy)
    testSystem.init(3)


def PVTpropTable(
    fluid1,
    fileName,
    lowTemperature,
    highTemperature,
    Tsteps,
    lowPressure,
    highPressure,
    Psteps,
):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.OLGApropTable(
        lowTemperature,
        highTemperature,
        Tsteps,
        lowPressure,
        highPressure,
        Psteps,
        fileName,
        0,
    )
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
    return jNeqSim.thermo.system.SystemInterface.addFluids(fluid1, fluid2)


def hydt(testSystem, type=1):
    if not testSystem.getHydrateCheck():
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
        print("error calculating bublepoint")
    return testSystem.getPressure()


def bubt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.bubblePointTemperatureFlash()
    except:
        print("error calculating bublepoint")
    return testSystem.getTemperature()


def dewp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointPressureFlash()
    except:
        print("error could not calculate")
    return testSystem.getPressure()


def dewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointTemperatureFlash()
    except:
        print("error could not calculate")
    return testSystem.getTemperature()


def waterdewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.waterDewPointTemperatureFlash()
    except:
        print("error could not calculate")
    return testSystem.getTemperature()


def phaseenvelope(testSystem, display=False):
    testFlash = ThermodynamicOperations(testSystem.clone())
    testFlash.calcPTphaseEnvelope()
    data = testFlash
    if display:
        if has_matplotlib():
            plt.plot(
                list(data.getOperation().get("dewT")),
                list(data.getOperation().get("dewP")),
                label="dew point",
            )
            plt.plot(
                list(data.getOperation().get("bubT")),
                list(data.getOperation().get("bubP")),
                label="bubble point",
            )

            try:
                plt.plot(
                    list(data.getOperation().get("dewT2")),
                    list(data.getOperation().get("dewP2")),
                    label="dew point2",
                )
            except:
                pass

            try:
                plt.plot(
                    list(data.getOperation().get("bubT2")),
                    list(data.getOperation().get("bubP2")),
                    label="bubble point2",
                )
            except:
                pass

            plt.title("PT envelope")
            plt.xlabel("Temperature [K]")
            plt.ylabel("Pressure [bar]")
            plt.legend()
            plt.show()
        else:
            raise Exception("Package matplotlib is not installed")
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
    if thermoSystem.getNumberOfPhases() == 1:
        if thermoSystem.getPhase(0).getPhaseType == 1:
            nargout[1] = (
                function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            )
            nargout[2] = 0
        else:
            nargout[2] = (
                function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            )
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
    if thermoSystem.getNumberOfPhases() == 1:
        if thermoSystem.getPhase(0).getPhaseType == 1:
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
    if thermoSystem.getNumberOfPhases() == 1:
        if thermoSystem.getPhase(0).getPhaseType == 1:
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
    GERG2008 = jNeqSim.thermo.util.GERG.NeqSimGERG2008()
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
