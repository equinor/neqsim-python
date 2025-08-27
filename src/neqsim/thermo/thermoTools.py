"""
This module provides various functions for thermodynamic operations and fluid property calculations using the NeqSim library.

Functions:
    fluid(name="srk", temperature=298.15, pressure=1.01325):
        Create a fluid object with the specified thermodynamic model, temperature, and pressure.

    readEclipseFluid(filename, wellName=""):
        Read fluid data from an Eclipse file.

    setEclipseComposition(fluid, filename, wellName=""):
        Set the composition of a fluid object using data from an Eclipse file.

    addFluids(fluids):
        Combine multiple fluid objects into one.

    fluid_df(reservoirFluiddf, lastIsPlusFraction=False, autoSetModel=False, modelName="", lumpComponents=True, numberOfLumpedComponents=12, add_all_components=True):
        Create a fluid object from a DataFrame containing reservoir fluid data.

    createfluid(fluid_type="dry gas"):
        Create a fluid object using a predefined fluid type.

    createfluid2(names, molefractions=None, unit="mol/sec"):
        Create a fluid object using specified component names and mole fractions.

    addOilFractions(fluid, charNames, molefractions, molarMass, density, lastIsPlusFraction=False, lumpComponents=True, numberOfPseudoComponents=12):
        Add oil fractions to a fluid object.

    newdatabase(system):
        Create a new database for the specified system.

    tunewaxmodel(fluid, experimentaldata, maxiterations=5):
        Tune the wax model for a fluid object using experimental data.

    data(system):
        Get the result table from a system object.

    table(system):
        Create a table from a system object.

    dataFrame(system):
        Convert the result table of a system object to a pandas DataFrame.

    calcproperties(gascondensateFluid, inputDict):
        Calculate properties of a gas condensate fluid using specified input conditions.

    fluidflashproperties(spec1, spec2, mode=1, system=None, components=None, fractions=None):
        Perform a flash calculation and return fluid properties for a series of process conditions.

    separatortest(fluid, pressure, temperature, GOR=None, Bo=None, display=False):
        Perform a separator test on a fluid object and optionally display the results.

    CVD(fluid, pressure, temperature, relativeVolume=None, liquidrelativevolume=None, Zgas=None, Zmix=None, cummulativemolepercdepleted=None, display=False):
        Perform a Constant Volume Depletion (CVD) test on a fluid object and optionally display the results.

    viscositysim(fluid, pressure, temperature, gasviscosity=None, oilviscosity=None, aqueousviscosity=None, display=False):
        Simulate the viscosity of a fluid object under specified conditions and optionally display the results.

    CME(fluid, pressure, temperature, saturationPressure, relativeVolume=None, liquidrelativevolume=None, Zgas=None, Yfactor=None, isothermalcompressibility=None, density=None, Bg=None, viscosity=None, display=False):
        Perform a Constant Mass Expansion (CME) test on a fluid object and optionally display the results.

    difflib(fluid, pressure, temperature, relativeVolume=None, Bo=None, Bg=None, relativegravity=None, Zgas=None, gasstandardvolume=None, Rs=None, oildensity=None, gasgravity=None, display=False):
        Perform a Differential Liberation (DL) test on a fluid object and optionally display the results.

    GOR(fluid, pressure, temperature, GORdata=None, Bo=None, display=False):
        Calculate the Gas-Oil Ratio (GOR) of a fluid object under specified conditions and optionally display the results.

    saturationpressure(fluid, temperature=-1.0):
        Calculate the saturation pressure of a fluid object at a specified temperature.

    swellingtest(fluid, fluid2, temperature, cummulativeMolePercentGasInjected, pressure=None, relativeoilvolume=None, display=False):
        Perform a swelling test on a fluid object and optionally display the results.

    printFrame(system):
        Print the result table of a system object as a markdown table.

    printFluid(system):
        Print the result table of a system object.

    volumecorrection(system, use=1):
        Apply volume correction to a system object.

    write(system, filename, newfile=0):
        Write the data of a system object to a file.

    appenddatabase(system):
        Append data to the database of a system object.

    show(system):
        Display the system object.

    showPDF(system):
        Generate and display a PDF of the system object.

    addComponent(thermoSystem, name, moles, unit="no", phase=-10):
        Add a component to a thermodynamic system object.

    temperature(thermoSystem, temp, phase=-1):
        Set the temperature of a thermodynamic system object.

    pressure(thermoSystem, pres, phase=-1):
        Set the pressure of a thermodynamic system object.

    reactionCheck(thermoSystem):
        Initialize chemical reactions in a thermodynamic system object.

    mixingRule(thermoSystem, mixRule="classic", GEmodel=""):
        Set the mixing rule for a thermodynamic system object.

    multiphase(testSystem, multiphase=1):
        Enable or disable multiphase check for a test system object.

    solidcheck(testSystem, solid=1):
        Enable or disable solid phase check for a test system object.

    solid(testSystem, solid=1):
        Enable or disable solid phase check for a test system object.

    GCV(testSystem, unit):
        Calculate the Gross Calorific Value (GCV) of a test system object.

    watersaturate(testSystem):
        Saturate a test system object with water.

    TPflash(testSystem, temperature=None, tUnit=None, pressure=None, pUnit=None):
        Perform a temperature-pressure flash calculation on a test system object.

    TPgradientFlash(testSystem, height, temperature):
        Perform a temperature-pressure gradient flash calculation on a test system object.

    TVflash(testSystem, volume, unit="m3"):
        Perform a temperature-volume flash calculation on a test system object.

    TSflash(testSystem, entropy, unit="J/K"):
        Perform a temperature-entropy flash calculation on a test system object.

    VSflash(testSystem, volume, entropy, unitVol="m3", unit="J/K"):
        Perform a volume-entropy flash calculation on a test system object.

    VHflash(testSystem, volume, enthalpy, unitVol="m3", unit="J"):
        Perform a volume-enthalpy flash calculation on a test system object.

    VUflash(testSystem, volume, energy, unitVol="m3", unit="J"):
        Perform a volume-internal energy flash calculation on a test system object.

    PUflash(testSystem, pressure, energy, unitPressure="bara", unitEnergy="J"):
        Perform a pressure-internal energy flash calculation on a test system object.

    PVTpropTable(fluid1, fileName, lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps):
        Generate a PVT property table for a fluid object and save it to a file.

    TPsolidflash(testSystem):
        Perform a temperature-pressure solid flash calculation on a test system object.

    PHflash(testSystem, enthalpy, unit="J"):
        Perform a pressure-enthalpy flash calculation on a test system object.

    PHsolidflash(testSystem, enthalpy):
        Perform a pressure-enthalpy solid flash calculation on a test system object.

    PSflash(testSystem, entropy, unit="J/K"):
        Perform a pressure-entropy flash calculation on a test system object.

    freeze(testSystem):
        Perform a freezing point temperature flash calculation on a test system object.

    scaleCheck(testSystem):
        Check the scale potential of a test system object.

    ionComposition(testSystem):
        Calculate the ion composition of a test system object.

    hydp(testSystem):
        Calculate the hydrate formation pressure of a test system object.

    addfluids(fluid1, fluid2):
        Add two fluid objects together.

    hydt(testSystem, type=1):
        Calculate the hydrate formation temperature of a test system object.

    calcIonComposition(fluid1):
        Calculate the ion composition of a fluid object.

    checkScalePotential(fluid1):
        Check the scale potential of a fluid object.

    bubp(testSystem):
        Calculate the bubble point pressure of a test system object.

    bubt(testSystem):
        Calculate the bubble point temperature of a test system object.

    dewp(testSystem):
        Calculate the dew point pressure of a test system object.

    dewt(testSystem):
        Calculate the dew point temperature of a test system object.

    waterdewt(testSystem):
        Calculate the water dew point temperature of a test system object.

    phaseenvelope(testSystem, display=False):
        Calculate the phase envelope of a test system object and optionally display the results.

    fluidComposition(testSystem, composition):
        Set the molar composition of a test system object.

    fluidCompositionPlus(testSystem, composition):
        Set the molar composition of a test system object with plus fractions.

    getExtThermProp(function, thermoSystem, t=0, p=0):
        Get extensive thermodynamic properties of a thermodynamic system object.

    getIntThermProp(function, thermoSystem, t=0, p=0):
        Get intensive thermodynamic properties of a thermodynamic system object.

    getPhysProp(function, thermoSystem, t=0, p=0):
        Get physical properties of a thermodynamic system object.

    enthalpy(thermoSystem, t=0, p=0):
        Get the enthalpy of a thermodynamic system object.

    entropy(thermoSystem, t=0, p=0):
        Get the entropy of a thermodynamic system object.

    densityGERG2008(phase):
        Get the density of a phase using the GERG-2008 model.

    molvol(thermoSystem, t=0, p=0):
        Get the molar volume of a thermodynamic system object.

    energy(thermoSystem, t=0, p=0):
        Get the internal energy of a thermodynamic system object.

    gibbsenergy(thermoSystem, t=0, p=0):
        Get the Gibbs energy of a thermodynamic system object.

    helmholtzenergy(thermoSystem, t=0, p=0):
        Get the Helmholtz energy of a thermodynamic system object.

    molefrac(thermoSystem, comp, t=0, p=0):
        Get the mole fraction of a component in a thermodynamic system object.

    moles(thermoSystem, phase=0):
        Get the number of moles in a thermodynamic system object.

    beta(thermoSystem, t=0, p=0):
        Get the phase fraction (beta) of a thermodynamic system object.

    molarmass(thermoSystem, t=0, p=0):
        Get the molar mass of a thermodynamic system object.

    Z(thermoSystem, t=0, p=0):
        Get the compressibility factor (Z) of a thermodynamic system object.

    density(thermoSystem, volcor=1, t=0, p=0):
        Get the density of a thermodynamic system object.

    viscosity(thermoSystem, t=0, p=0):
        Get the viscosity of a thermodynamic system object.

    WAT(testSystem):
        Calculate the Wax Appearance Temperature (WAT) of a test system object.

"""

import logging
from typing import List, Optional, Union
import jpype
import pandas
from jpype.types import *
from neqsim import has_matplotlib, has_tabulate
from neqsim.neqsimpython import jneqsim
from neqsim.standards import ISO6976
import math

logger = logging.getLogger(__name__)

if has_matplotlib():
    import matplotlib.pyplot as plt

thermodynamicoperations = jneqsim.thermodynamicoperations.ThermodynamicOperations
fluidcreator = jneqsim.thermo.Fluid()
fluid_type = {
    "srk": jneqsim.thermo.system.SystemSrkEos,
    "SRK-EoS": jneqsim.thermo.system.SystemSrkEos,
    "Psrk-EoS": jneqsim.thermo.system.SystemPsrkEos,
    "PSRK-EoS": jneqsim.thermo.system.SystemPsrkEos,
    "RK-EoS": jneqsim.thermo.system.SystemRKEos,
    "pr": jneqsim.thermo.system.SystemPrEos,
    "PR-EoS": jneqsim.thermo.system.SystemPrEos,
    "pr-umr": jneqsim.thermo.system.SystemUMRPRUMCEos,
    "srk-s": jneqsim.thermo.system.SystemSrkSchwartzentruberEos,
    "GERG-water": jneqsim.thermo.system.SystemGERGwaterEos,
    "SRK-MC": jneqsim.thermo.system.SystemSrkMathiasCopeman,
    "PR-MC": jneqsim.thermo.system.SystemPrMathiasCopeman,
    "scrk": jneqsim.thermo.system.SystemSrkSchwartzentruberEos,
    "ScRK-EoS": jneqsim.thermo.system.SystemSrkSchwartzentruberEos,
    "nrtl": jneqsim.thermo.system.SystemNRTL,
    "unifac": jneqsim.thermo.system.SystemUNIFAC,
    "electrolyte": jneqsim.thermo.system.SystemFurstElectrolyteEos,
    "Electrolyte-ScRK-EoS": jneqsim.thermo.system.SystemFurstElectrolyteEos,
    "Electrolyte-CPA-EoS": jneqsim.thermo.system.SystemElectrolyteCPAstatoil,
    "cpa-el": jneqsim.thermo.system.SystemElectrolyteCPA,
    "cpa-s": jneqsim.thermo.system.SystemSrkCPAs,
    "cpa-statoil": jneqsim.thermo.system.SystemSrkCPAstatoil,
    "cpa": jneqsim.thermo.system.SystemSrkCPAstatoil,
    "CPA-SRK-EoS": jneqsim.thermo.system.SystemSrkCPA,
    "cpa-srk": jneqsim.thermo.system.SystemSrkCPA,
    "srk-twoCoon": jneqsim.thermo.system.SystemSrkTwuCoonParamEos,
    "cpa-pr": jneqsim.thermo.system.SystemPrCPA,
    "CPA-PR-EoS": jneqsim.thermo.system.SystemPrCPA,
    "SRK-TwuCoon-EOS": jneqsim.thermo.system.SystemSrkTwuCoonStatoilEos,
}


def fluid(name="srk", temperature=298.15, pressure=1.01325):
    """
    Create a thermodynamic fluid system.

    Parameters:
    name (str): The name of the equation of state to use. Default is "srk".
    temperature (float): The temperature of the fluid in Kelvin. Default is 298.15 K.
    pressure (float): The pressure of the fluid in bar. Default is 1.01325 bar.

    Returns:
    object: An instance of the specified thermodynamic fluid system.
    """
    fluid_function = fluid_type.get(name, jneqsim.thermo.system.SystemSrkEos)
    return fluid_function(temperature, pressure)


def readEclipseFluid(filename, wellName=""):
    """
    Reads an Eclipse fluid file and returns the fluid object.

    Parameters:
    filename (str): The path to the Eclipse fluid file.
    wellName (str, optional): The name of the well. Defaults to an empty string.

    Returns:
    Fluid: The fluid object read from the file.
    """
    jneqsim.thermo.util.readwrite.EclipseFluidReadWrite.pseudoName = wellName
    fluid1 = jneqsim.thermo.util.readwrite.EclipseFluidReadWrite.read(filename)
    return fluid1


def setEclipseComposition(fluid, filename, wellName=""):
    jneqsim.thermo.util.readwrite.EclipseFluidReadWrite.pseudoName = wellName
    jneqsim.thermo.util.readwrite.EclipseFluidReadWrite.setComposition(fluid, filename)


def addFluids(fluids):
    """
    Combine multiple fluid objects into a single fluid object.

    This function takes a list of fluid objects, clones the first fluid object,
    and then adds each subsequent fluid object to the cloned fluid object.

    Parameters:
    fluids (list): A list of fluid objects to be combined. The first fluid object
                   in the list will be cloned, and the rest will be added to this clone.

    Returns:
    Fluid: A single fluid object that is the result of combining all the fluid objects
           in the input list.
    """
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
    """
    Create a fluid object from a DataFrame containing reservoir fluid composition data.

    Parameters:
    reservoirFluiddf (pd.DataFrame): DataFrame containing the reservoir fluid composition.
    lastIsPlusFraction (bool, optional): Indicates if the last component is a plus fraction. Defaults to False.
    autoSetModel (bool, optional): If True, automatically selects the thermodynamic model. Defaults to False.
    modelName (str, optional): Name of the thermodynamic model to use. Defaults to an empty string.
    lumpComponents (bool, optional): If True, lumps components together. Defaults to True.
    numberOfLumpedComponents (int, optional): Number of lumped components to create. Defaults to 12.
    add_all_components (bool, optional): If True, adds all components regardless of their molar composition. Defaults to True.

    Returns:
    fluid: A fluid object created based on the provided composition data.
    """
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
    """
    Create a fluid object based on the specified fluid type.

    Parameters:
    fluid_type (str): The type of fluid to create. Default is "dry gas".

    Returns:
    Fluid: A fluid object created based on the specified fluid type.
    """
    return fluidcreator.create(fluid_type)


def createfluid2(names, molefractions=None, unit="mol/sec"):
    """
    Create a fluid with specified component names and mole fractions.

    Parameters:
    names (list of str): List of component names.
    molefractions (list of float, optional): List of mole fractions corresponding to the component names. Defaults to None.
    unit (str, optional): Unit of the mole fractions. Defaults to "mol/sec".

    Returns:
    Fluid: The created fluid object.
    """
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

    waxsim = jneqsim.pvtsimulation.simulation.WaxFractionSim(fluid)
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
    """
    Calculate properties of a gas condensate fluid using the jneqsim PropertyGenerator.

    Parameters:
    gascondensateFluid (object): The gas condensate fluid object to be analyzed.
    inputDict (dict): A dictionary containing the input parameters:
        - "temperature" (list of float): List of temperatures at which to calculate properties.
        - "pressure" (list of float): List of pressures at which to calculate properties.

    Returns:
    pandas.DataFrame: A DataFrame containing the calculated properties with keys as column names.
    """
    properties = jneqsim.util.generator.PropertyGenerator(
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
    components: Optional[List[str]] = None,
    fractions: Optional[list] = None,
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

        system = jneqsim.thermo.system.SystemSrkEos(273.15, 1.01325)
        if not isinstance(components, list):
            components = [components]

        system.addComponents(components)

        # Single component
        if not isinstance(fractions, list):
            fractions = [fractions]

        if not all([isinstance(x, list) for x in fractions]):
            system.setTotalNumberOfMoles(1)
            system.setMolarComposition(fractions)

    thermoOps = jneqsim.thermodynamicoperations.ThermodynamicOperations(system)

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
    sepSim = jneqsim.pvtsimulation.simulation.SeparatorTest(fluid)
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
    cvdSim = jneqsim.pvtsimulation.simulation.ConstantVolumeDepletion(fluid)
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
    cmeSim = jneqsim.pvtsimulation.simulation.ViscositySim(fluid)
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
    cvdSim = jneqsim.pvtsimulation.simulation.ConstantMassExpansion(fluid)
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
    cvdSim = jneqsim.pvtsimulation.simulation.DifferentialLiberation(fluid)
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
    jGOR = jneqsim.pvtsimulation.simulation.GOR(fluid)
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
    cvdSim = jneqsim.pvtsimulation.simulation.SaturationPressure(fluid)
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
    cvdSim = jneqsim.pvtsimulation.simulation.SwellingTest(fluid)
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
    """
    Print the thermodynamic system data in a tabular format.

    If the 'tabulate' library is available, the data will be printed in a markdown table format.
    Otherwise, it will be printed in a default DataFrame format.

    Parameters:
    system : object
        The thermodynamic system object containing the data to be printed.

    Returns:
    None
    """
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
    """
    Add a component to the thermoSystem.

    Parameters:
    thermoSystem (object): The thermodynamic system to which the component will be added.
    name (str): The name of the component to be added.
    moles (float): The amount of the component to be added in moles.
    unit (str, optional): The unit of the amount (default is "no").
    phase (int, optional): The phase of the component (default is -10).

    Returns:
    None
    """
    if phase == -10 and unit == "no":
        thermoSystem.addComponent(name, moles)
    elif phase == -10:
        thermoSystem.addComponent(name, moles, unit)
    elif unit == "no":
        thermoSystem.addComponent(name, moles, phase)
    else:
        thermoSystem.addComponent(name, moles, unit, phase)


def temperature(thermoSystem, temp, phase=-1):
    """
    Set the temperature of the specified phase in the thermoSystem.

    Parameters:
    thermoSystem (ThermoSystem): The thermodynamic system to modify.
    temp (float): The temperature to set.
    phase (int, optional): The phase index to set the temperature for.
                           If -1, set the temperature for the entire system.
                           Defaults to -1.
    Returns:
    None
    """
    if phase == -1:
        thermoSystem.setTemperature(temp)
    else:
        thermoSystem.getPhase(phase).setTemperature(temp)


def pressure(thermoSystem, pres, phase=-1):
    """
    Set the pressure of the given thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system to modify.
    pres (float): The pressure to set.
    phase (int, optional): The phase index to set the pressure for.
                           If -1, sets the pressure for the entire system.
                           Defaults to -1.

    Returns:
    None
    """
    if phase == -1:
        thermoSystem.setPressure(pres)
    else:
        thermoSystem.getPhase(phase).setPressure(pres)


def reactionCheck(thermoSystem):
    thermoSystem.chemicalReactionInit()


def mixingRule(thermoSystem, mixRule="classic", GEmodel=""):
    """
    Set the mixing rule for the given thermodynamic system.

    Parameters:
    thermoSystem (ThermoSystem): The thermodynamic system to set the mixing rule for.
    mixRule (str, optional): The mixing rule to use. Defaults to "classic".
    GEmodel (str, optional): The GE model to use. If not provided, only the mixing rule is set. Defaults to "".

    Returns:
    None
    """
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


()


def GCV(testSystem, unit):
    """
    Calculate the Gross Calorific Value (GCV) of a given test system.

    Parameters:
    testSystem (object): The test system for which the GCV is to be calculated.
    unit (str): The unit of measurement for the GCV.

    Returns:
    float: The calculated Gross Calorific Value (GCV) in the specified unit.
    """
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
    """
    Saturates the given thermodynamic system with water.

    This function takes a thermodynamic system as input, performs a water saturation
    operation on it, and then reinitializes the system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to be saturated with water.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.saturateWithWater()
    testSystem.init(3)


def TPflash(testSystem, temperature=None, tUnit=None, pressure=None, pUnit=None):
    """
    Perform a temperature and pressure flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the flash calculation on.
    temperature (float, optional): The temperature to set for the system. Defaults to None.
    tUnit (str, optional): The unit of the temperature. Defaults to "K" if temperature is provided.
    pressure (float, optional): The pressure to set for the system. Defaults to None.
    pUnit (str, optional): The unit of the pressure. Defaults to "bara" if pressure is provided.

    Returns:
    None
    """
    if temperature is not None:
        if tUnit is None:
            tUnit = "K"
        testSystem.setTemperature(temperature, tUnit)
    if pressure is not None:
        if pUnit is None:
            pUnit = "bara"
        testSystem.setPressure(pressure, pUnit)
    testFlash = thermodynamicoperations(testSystem)
    testFlash.TPflash()
    testSystem.init(3)


def TPgradientFlash(testSystem, height, temperature):
    """
    Perform a TP gradient flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the flash calculation on.
    height (float): The height at which the flash calculation is to be performed.
    temperature (float): The temperature at which the flash calculation is to be performed.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    return testFlash.TPgradientFlash(height, temperature)


def TVflash(testSystem, volume, unit="m3"):
    """
    Perform a temperature-volume (TV) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem : neqsim.thermo.system.SystemInterface
        The thermodynamic system to perform the flash calculation on.
    volume : float
        The volume to be used in the flash calculation.
    unit : str, optional
        The unit of the volume (default is "m3").

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.TVflash(volume, unit)
    testSystem.init(3)


def TSflash(testSystem, entropy, unit="J/K"):
    """
    Perform a temperature-entropy (TS) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem : neqsim.thermo.system.SystemInterface
        The thermodynamic system to perform the TS flash calculation on.
    entropy : float
        The entropy value to use for the TS flash calculation.
    unit : str, optional
        The unit of the entropy value (default is "J/K").

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.TSflash(entropy, unit)
    testSystem.init(3)


def VSflash(testSystem, volume, entropy, unitVol="m3", unit="J/K"):
    """
    Perform a volume-entropy (VS) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the flash calculation on.
    volume (float): The volume to be used in the flash calculation.
    entropy (float): The entropy to be used in the flash calculation.
    unitVol (str, optional): The unit of the volume. Default is "m3".
    unit (str, optional): The unit of the entropy. Default is "J/K".

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.VSflash(volume, entropy, unitVol, unit)
    testSystem.init(3)


def VHflash(testSystem, volume, enthalpy, unitVol="m3", unit="J"):
    """
    Perform a volume-enthalpy (VH) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem : neqsim.thermo.system.SystemInterface
        The thermodynamic system to perform the flash calculation on.
    volume : float
        The volume to be used in the flash calculation.
    enthalpy : float
        The enthalpy to be used in the flash calculation.
    unitVol : str, optional
        The unit of the volume (default is "m3").
    unit : str, optional
        The unit of the enthalpy (default is "J").

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.VHflash(volume, enthalpy, unitVol, unit)
    testSystem.init(3)


def VUflash(testSystem, volume, energy, unitVol="m3", unit="J"):
    """
    Perform a volume-energy (VU) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the flash calculation on.
    volume (float): The volume to be used in the flash calculation.
    energy (float): The energy to be used in the flash calculation.
    unitVol (str, optional): The unit of the volume. Default is "m3".
    unit (str, optional): The unit of the energy. Default is "J".

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.VUflash(volume, energy, unitVol, unit)
    testSystem.init(3)


def PUflash(testSystem, pressure, energy, unitPressure="bara", unitEnergy="J"):
    """
    Perform a pressure-energy (PU) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the flash calculation on.
    pressure (float): The pressure value for the flash calculation.
    energy (float): The energy value for the flash calculation.
    unitPressure (str, optional): The unit of the pressure value. Default is "bara".
    unitEnergy (str, optional): The unit of the energy value. Default is "J".

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
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
    """
    Generate a PVT property table for a given fluid and save it to a file.

    Parameters:
    fluid1 : neqsim.thermo.system.SystemInterface
        The fluid system for which the PVT properties are to be calculated.
    fileName : str
        The name of the file where the PVT property table will be saved.
    lowTemperature : float
        The lower bound of the temperature range (in Kelvin).
    highTemperature : float
        The upper bound of the temperature range (in Kelvin).
    Tsteps : int
        The number of temperature steps between lowTemperature and highTemperature.
    lowPressure : float
        The lower bound of the pressure range (in bar).
    highPressure : float
        The upper bound of the pressure range (in bar).
    Psteps : int
        The number of pressure steps between lowPressure and highPressure.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(fluid1)
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
    """
    Perform a temperature and pressure solid flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system on which to perform the solid flash calculation.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.TPSolidflash()


def PHflash(testSystem, enthalpy, unit="J"):
    """
    Perform a pressure-enthalpy (PH) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem : neqsim.thermo.system.SystemInterface
        The thermodynamic system on which to perform the PH flash calculation.
    enthalpy : float
        The enthalpy value for the PH flash calculation.
    unit : str, optional
        The unit of the enthalpy value (default is "J").

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.PHflash(enthalpy, unit)


def PHsolidflash(testSystem, enthalpy):
    """
    Perform a pressure-enthalpy flash calculation for a solid phase.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to be used for the flash calculation.
    enthalpy (float): The enthalpy value for the flash calculation.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.PHsolidFlash(enthalpy)


def PSflash(testSystem, entropy, unit="J/K"):
    """
    Perform a pressure-entropy (PS) flash calculation on the given thermodynamic system.

    Parameters:
    testSystem : object
        The thermodynamic system on which to perform the PS flash calculation.
    entropy : float
        The entropy value to be used in the PS flash calculation.
    unit : str, optional
        The unit of the entropy value (default is "J/K").

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.PSflash(entropy, unit)


def freeze(testSystem):
    """
    Perform a freezing point temperature flash calculation on the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to perform the freezing point calculation on.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.freezingPointTemperatureFlash()


def scaleCheck(testSystem):
    """
    Perform a mineral scale potential check on the given thermodynamic system.

    This function creates a thermodynamic operations object for the provided
    test system, checks the scale potential for the aqueous phase, and displays
    the results.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to be checked.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.checkScalePotential(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()


def ionComposition(testSystem):
    """
    Calculate and display the ion composition of the aqueous phase in the given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the ion composition is to be calculated.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.calcIonComposition(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()


def hydp(testSystem):
    """
    Calculate the hydrate equilibrium pressure for a given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the hydrate formation pressure is to be calculated.

    Returns:
    None
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.hydrateFormationPressure()


def addfluids(fluid1, fluid2):
    """
    Add two fluid systems together using the jneqsim library.

    Parameters:
    fluid1 (SystemInterface): The first fluid system to be added.
    fluid2 (SystemInterface): The second fluid system to be added.

    Returns:
    SystemInterface: A new fluid system that is the result of adding fluid1 and fluid2.
    """
    return jneqsim.thermo.system.SystemInterface.addFluids(fluid1, fluid2)


def hydt(testSystem, type=1):
    """
    Calculate the hydrate equilibrium temperature for a given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to be tested for hydrate formation.
    type (int, optional): The type of hydrate formation calculation to perform. Defaults to 1.

    Returns:
    float: The temperature at which hydrate formation occurs.
    """
    if not testSystem.getHydrateCheck():
        testSystem.setHydrateCheck(True)
    testFlash = thermodynamicoperations(testSystem)
    testFlash.hydrateFormationTemperature(type)
    return testSystem.getTemperature()


def calcIonComposition(fluid1):
    """
    Calculate the ion composition of the aqueous phase in the given fluid.

    Parameters:
    fluid1 (object): The fluid object for which the ion composition is to be calculated.

    Returns:
    list: A table of results containing the ion composition of the aqueous phase.
    """
    testFlash = thermodynamicoperations(fluid1)
    testFlash.calcIonComposition(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()


def checkScalePotential(fluid1):
    """
    Check the mineral scale potential of a given fluid.

    This function performs a thermodynamic operation to check the scale potential
    of the specified fluid in its aqueous phase. It returns the result in a table format.

    Parameters:
    fluid1 (object): The fluid object to be analyzed. It should have a method
                     `getPhaseNumberOfPhase` to get the phase number of the "aqueous" phase.

    Returns:
    list: A table containing the results of the scale potential check.
    """
    testFlash = thermodynamicoperations(fluid1)
    testFlash.checkScalePotential(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()


def bubp(testSystem):
    """
    Calculate the bubble point pressure of a given thermodynamic system.

    This function performs a bubble point pressure flash calculation on the provided
    thermodynamic system. If the calculation is successful, it returns the pressure
    of the system. If an error occurs during the calculation, it logs an error message
    and returns NaN.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which to calculate
                                      the bubble point pressure.

    Returns:
    float: The pressure of the system after the bubble point pressure flash calculation,
           or NaN if an error occurs.
    """
    testFlash = thermodynamicoperations(testSystem)
    try:
        testFlash.bubblePointPressureFlash(0)
    except:
        logger.error("error calculating bublepoint")
        return math.nan

    return testSystem.getPressure()


def bubt(testSystem):
    """
    Calculate the bubble point temperature of a given thermodynamic system.

    This function performs a bubble point temperature flash calculation on the provided
    thermodynamic system. If the calculation is successful, it returns the temperature
    of the system. If an error occurs during the calculation, it logs an error message
    and returns NaN.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the bubble point
                                      temperature is to be calculated.

    Returns:
    float: The temperature of the system after the bubble point temperature flash calculation,
           or NaN if an error occurs.
    """
    testFlash = thermodynamicoperations(testSystem)
    try:
        testFlash.bubblePointTemperatureFlash()
    except:
        logger.error("error calculating bublepoint")
        return math.nan

    return testSystem.getTemperature()


def dewp(testSystem):
    """
    Calculate the dew point pressure of the given thermodynamic system.

    This function performs a dew point pressure flash calculation on the provided
    thermodynamic system. If the calculation is successful, it returns the pressure
    of the system. If an error occurs during the calculation, it logs an error message
    and returns NaN.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the dew point
                                      pressure is to be calculated.

    Returns:
    float: The dew point pressure of the system if the calculation is successful,
           otherwise NaN.
    """
    testFlash = thermodynamicoperations(testSystem)
    try:
        testFlash.dewPointPressureFlash()
    except:
        logger.error("error could not calculate")
        return math.nan

    return testSystem.getPressure()


def dewt(testSystem):
    """
    Calculate the dew point temperature of a given thermodynamic system.

    This function performs a dew point temperature flash calculation on the provided
    thermodynamic system. If the calculation is successful, it returns the temperature
    of the system. If an error occurs during the calculation, it logs an error message
    and returns NaN.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the dew point
                                      temperature is to be calculated.

    Returns:
    float: The temperature of the system after the dew point calculation, or NaN if
           an error occurred.
    """
    testFlash = thermodynamicoperations(testSystem)
    try:
        testFlash.dewPointTemperatureFlash()
    except:
        logger.error("error could not calculate")
        return math.nan

    return testSystem.getTemperature()


def waterdewt(testSystem):
    """
    Calculate the water dew point temperature of the given thermodynamic system.

    This function performs a water dew point temperature flash calculation on the provided
    thermodynamic system. If the calculation is successful, it returns the temperature of
    the system. If an error occurs during the calculation, it logs an error message and
    returns NaN.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the water dew point
                                      temperature is to be calculated.

    Returns:
    float: The temperature of the system after the water dew point temperature flash
           calculation, or NaN if an error occurs.
    """
    testFlash = thermodynamicoperations(testSystem)
    try:
        testFlash.waterDewPointTemperatureFlash()
    except:
        logger.error("error could not calculate")
        return math.nan

    return testSystem.getTemperature()


def phaseenvelope(testSystem, display=False):
    """
    Calculate and optionally display the phase envelope of a given thermodynamic system.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the phase envelope is to be calculated.
    display (bool, optional): If True, the phase envelope will be plotted using matplotlib. Default is False.

    Returns:
    ThermodynamicOperations: The thermodynamic operations object containing the phase envelope data.

    Raises:
    Exception: If display is True and matplotlib is not installed.

    Notes:
    The function clones the provided thermodynamic system and calculates the PT phase envelope.
    If display is True and matplotlib is available, it plots the dew point and bubble point curves.
    """
    testFlash = thermodynamicoperations(testSystem.clone())
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
    """
    Set the molar composition of a given test system and initialize it.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system to set the composition for.
    composition (list of float): A list of molar fractions for each component in the system.

    Returns:
    None
    """
    testSystem.setMolarComposition(JDouble[:](composition))
    testSystem.init(0)


def fluidCompositionPlus(testSystem, composition):
    """
    Set the molar composition of a test system and initialize it.

    Parameters:
    testSystem (TestSystem): The test system object to set the composition for.
    composition (list of float): A list of molar compositions to set in the test system.

    Returns:
    None
    """
    testSystem.setMolarCompositionPlus(JDouble[:](composition))
    testSystem.init(0)


def getExtThermProp(function, thermoSystem, t=0, p=0):
    """
    Calculate and return external thermodynamic properties of a given thermodynamic system.

    Parameters:
    function (list): A list of functions to calculate properties.
    thermoSystem (object): The thermodynamic system object.
    t (float, optional): Temperature to set for the system. Defaults to 0.
    p (float, optional): Pressure to set for the system. Defaults to 0.

    Returns:
    list: A list containing:
        - Overall property value normalized by the number of moles.
        - Property value of the first phase normalized by the number of moles in the phase.
        - Property value of the second phase normalized by the number of moles in the phase.
        - Number of phases in the system.
    """
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
    """
    Calculate thermodynamic properties of a given thermoSystem.

    Parameters:
    function (list): A list of functions to calculate thermodynamic properties.
    thermoSystem (object): The thermodynamic system to be analyzed.
    t (float, optional): Temperature to set for the thermoSystem. Default is 0.
    p (float, optional): Pressure to set for the thermoSystem. Default is 0.

    Returns:
    list: A list containing the calculated thermodynamic properties and the number of phases.
        - nargout[0]: Result of the first function in the function list.
        - nargout[1]: Result of the second function in the function list if the phase type is 1, otherwise 0.
        - nargout[2]: Result of the second function in the function list if the phase type is not 1, otherwise 0.
        - nargout[3]: Number of phases in the thermoSystem.
    """
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
    """
    Calculate physical properties of a thermodynamic system.

    Parameters:
    function (list): A list of functions to calculate physical properties.
    thermoSystem (ThermoSystem): The thermodynamic system to be analyzed.
    t (float, optional): Temperature to set for the system. Defaults to 0.
    p (float, optional): Pressure to set for the system. Defaults to 0.

    Returns:
    list: A list containing the calculated physical properties:
        - nargout[0]: Result of the first function in the list.
        - nargout[1]: Result of the second function in the list if the phase type is 1, otherwise 0.
        - nargout[2]: Result of the second function in the list if the phase type is not 1, otherwise 0.
        - nargout[3]: Number of phases in the thermodynamic system.
    """
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
    """
    Calculate the enthalpy of the given thermodynamic system.

    Parameters:
    thermoSystem (object): The thermodynamic system for which the enthalpy is to be calculated.
    t (float, optional): Temperature at which the enthalpy is to be calculated. Default is 0.
    p (float, optional): Pressure at which the enthalpy is to be calculated. Default is 0.

    Returns:
    float: The calculated enthalpy of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getEnthalpy)
    func.append(thermoSystem.getPhase(0).getEnthalpy)
    func.append(thermoSystem.getPhase(1).getEnthalpy)
    return getExtThermProp(func, thermoSystem, t, p)


def entropy(thermoSystem, t=0, p=0):
    """
    Calculate the entropy of the given thermodynamic system.

    Parameters:
    thermoSystem (object): The thermodynamic system for which entropy is to be calculated.
    t (float, optional): Temperature at which entropy is to be calculated. Default is 0.
    p (float, optional): Pressure at which entropy is to be calculated. Default is 0.

    Returns:
    float: The entropy of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getEntropy)
    func.append(thermoSystem.getPhase(0).getEntropy)
    func.append(thermoSystem.getPhase(1).getEntropy)
    return getExtThermProp(func, thermoSystem, t, p)


def densityGERG2008(phase):
    """
    Calculate the density of a given phase using the GERG-2008 equation of state.

    Parameters:
    phase (Phase): The phase object for which the density is to be calculated.

    Returns:
    float: The density of the specified phase.
    """
    GERG2008 = jneqsim.thermo.util.GERG.NeqSimGERG2008()
    return GERG2008.getDensity(phase)


def molvol(thermoSystem, t=0, p=0):
    """
    Calculate the molar volume of a thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system for which the molar volume is calculated.
    t (float, optional): Temperature at which the molar volume is calculated. Default is 0.
    p (float, optional): Pressure at which the molar volume is calculated. Default is 0.

    Returns:
    float: The molar volume of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getMolarVolume)
    func.append(thermoSystem.getPhase(0).getMolarVolume)
    func.append(thermoSystem.getPhase(1).getMolarVolume)
    return getIntThermProp(func, thermoSystem, t, p)


def energy(thermoSystem, t=0, p=0):
    """
    Calculate the internal energy of the given thermodynamic system.

    Parameters:
    thermoSystem (object): The thermodynamic system for which the internal energy is to be calculated.
    t (float, optional): Temperature value to be used in the calculation. Default is 0.
    p (float, optional): Pressure value to be used in the calculation. Default is 0.

    Returns:
    float: The calculated internal energy of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getInternalEnergy)
    func.append(thermoSystem.getPhase(0).getInternalEnergy)
    func.append(thermoSystem.getPhase(1).getInternalEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def gibbsenergy(thermoSystem, t=0, p=0):
    """
    Calculate the Gibbs energy of the given thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system for which the Gibbs energy is to be calculated.
    t (float, optional): Temperature at which the Gibbs energy is to be calculated. Default is 0.
    p (float, optional): Pressure at which the Gibbs energy is to be calculated. Default is 0.

    Returns:
    float: The Gibbs energy of the thermodynamic system at the specified temperature and pressure.
    """
    func = []
    func.append(thermoSystem.getGibbsEnergy)
    func.append(thermoSystem.getPhase(0).getGibbsEnergy)
    func.append(thermoSystem.getPhase(1).getGibbsEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def helmholtzenergy(thermoSystem, t=0, p=0):
    """
    Calculate the Helmholtz energy of a thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system for which the Helmholtz energy is calculated.
    t (float, optional): Temperature at which the Helmholtz energy is calculated. Default is 0.
    p (float, optional): Pressure at which the Helmholtz energy is calculated. Default is 0.

    Returns:
    float: The Helmholtz energy of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(0).getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(1).getHelmholtzEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def molefrac(thermoSystem, comp, t=0, p=0):
    """
    Calculate the mole fraction of a component in different phases of a thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system containing the phases and components.
    comp (str): The name of the component for which the mole fraction is to be calculated.
    t (float, optional): Temperature at which the calculation is to be performed. Default is 0.
    p (float, optional): Pressure at which the calculation is to be performed. Default is 0.

    Returns:
    float: The mole fraction of the component in the specified phases.
    """
    func = []
    func.append(thermoSystem.getPhase(0).getComponent(comp).getz)
    func.append(thermoSystem.getPhase(0).getComponent(comp).getx)
    func.append(thermoSystem.getPhase(1).getComponent(comp).getx)
    return getIntThermProp(func, thermoSystem, t, p)


def moles(thermoSystem, phase=0):
    """
    Calculate the number of moles in the specified phase of the thermoSystem.

    Parameters:
    thermoSystem (ThermoSystem): The thermodynamic system object.
    phase (int, optional): The phase index to get the number of moles from. Defaults to 0.

    Returns:
    float: The number of moles in the specified phase of the thermoSystem.
    """
    if phase == 0:
        return thermoSystem.getNumberOfMoles()
    else:
        return thermoSystem.getPhase(phase).getNumberOfMolesInPhase()


def beta(thermoSystem, t=0, p=0):
    """
    Calculate the beta value (gas compressibility) for the given thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system for which to calculate the beta value.
    t (float, optional): Temperature value. Default is 0.
    p (float, optional): Pressure value. Default is 0.

    Returns:
    float: The calculated beta value.
    """
    func = []
    func.append(thermoSystem.getBeta)
    func.append(thermoSystem.getPhase(0).getBeta)
    func.append(thermoSystem.getPhase(1).getBeta)
    return getIntThermProp(func, thermoSystem, t, p)


def molarmass(thermoSystem, t=0, p=0):
    """
    Calculate the molar mass of the given thermodynamic system.

    Parameters:
    thermoSystem (object): The thermodynamic system for which the molar mass is to be calculated.
    t (float, optional): Temperature at which the molar mass is to be calculated. Default is 0.
    p (float, optional): Pressure at which the molar mass is to be calculated. Default is 0.

    Returns:
    float: The molar mass of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getMolarMass)
    func.append(thermoSystem.getPhase(0).getMolarMass)
    func.append(thermoSystem.getPhase(1).getMolarMass)
    return getIntThermProp(func, thermoSystem, t, p)


def Z(thermoSystem, t=0, p=0):
    """
    Calculate the compressibility factor (Z) for a given thermodynamic system.

    Parameters:
    thermoSystem (object): The thermodynamic system for which the compressibility factor is to be calculated.
    t (float, optional): Temperature at which the calculation is to be performed. Default is 0.
    p (float, optional): Pressure at which the calculation is to be performed. Default is 0.

    Returns:
    float: The compressibility factor (Z) of the thermodynamic system.
    """
    func = []
    func.append(thermoSystem.getZ)
    func.append(thermoSystem.getPhase(0).getZ)
    func.append(thermoSystem.getPhase(1).getZ)
    return getIntThermProp(func, thermoSystem, t, p)


def density(thermoSystem, volcor=1, t=0, p=0):
    """
    Calculate the density of the given thermodynamic system.

    Parameters:
    thermoSystem (ThermoSystem): The thermodynamic system for which the density is to be calculated.
    volcor (int, optional): Volume correction flag. If 1, physical properties are initialized and
                            densities of phases are obtained from physical properties. If 0, densities
                            are obtained directly from phases. Default is 1.
    t (float, optional): Temperature at which the density is to be calculated. Default is 0.
    p (float, optional): Pressure at which the density is to be calculated. Default is 0.

    Returns:
    float: The calculated density of the thermodynamic system.
    """
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
    """
    Calculate the viscosity of the given thermodynamic system.

    Parameters:
    thermoSystem (ThermodynamicSystem): The thermodynamic system for which the viscosity is to be calculated.
    t (float, optional): Temperature at which the viscosity is to be calculated. Default is 0.
    p (float, optional): Pressure at which the viscosity is to be calculated. Default is 0.

    Returns:
    float: The viscosity of the thermodynamic system at the specified temperature and pressure.
    """
    func = []
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(1).getPhysicalProperties().getViscosity)
    return getPhysProp(func, thermoSystem, t, p)


def WAT(testSystem):
    """
    Calculate the Wax Appearance Temperature (WAT) of a given thermodynamic system.

    This function initializes a thermodynamic operation on the provided system,
    calculates the WAT, reinitializes the system, and returns the temperature at
    which wax appears.

    Parameters:
    testSystem (ThermodynamicSystem): The thermodynamic system for which the WAT is to be calculated.

    Returns:
    float: The temperature at which wax appears in the system.
    """
    testFlash = thermodynamicoperations(testSystem)
    testFlash.calcWAT()
    testSystem.init(3)
    return testSystem.getTemperature()
