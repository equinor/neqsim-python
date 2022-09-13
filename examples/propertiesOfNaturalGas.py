# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:01:36 2019

The current python script demonstrates use of neqsim in python
A fluid is created and multiphase equilibrium is calculated
Various properties are reported for the fluid

@author: esol
"""

from neqsim.thermo import TPflash, fluid

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(10.0, "bara")
fluid1.addComponent("methane", 10.0, "mol/sec")
fluid1.addComponent("n-heptane", 5.0, "mol/sec")
fluid1.addComponent("water", 1.0, "kg/sec")
fluid1.setMixingRule(2)
fluid1.setMultiPhaseCheck(True)

# Calculate equilibrium at given temperature and pressure
TPflash(fluid1)

# Caclulate thermodynamic and physical properties of the fluid
fluid1.initThermoProperties()
fluid1.initPhysicalProperties()

# Read overall mixture properties
mixnumberOfPhases = fluid1.getNumberOfPhases()
mixMolarVolume = 1.0 / fluid1.getDensity("mol/m3")
mixDensity = fluid1.getDensity("kg/m3")
mixZfactor = fluid1.getZ()
mixEnthalpy = fluid1.getEnthalpy("Jmol")
mixEntropy = fluid1.getEntropy("JmolK")
mixCp = fluid1.getCp("J/molK")
mixCv = fluid1.getCv("J/molK")
mixKappa = fluid1.getKappa()
mixViscosity = fluid1.getViscosity("kg/msec")
mixThermalConductivity = fluid1.getConductivity("W/mK")

# read properties of individual phases
if fluid1.hasPhaseType("gas"):
    phaseNumber = fluid1.getPhaseNumberOfPhase("gas")
    gasFractionc = fluid1.getMoleFraction(phaseNumber) * 100
    gasMolarVolume = 1.0 / fluid1.getPhase(phaseNumber).getDensity("mol/m3")
    gasVolumeFraction = fluid1.getCorrectedVolumeFraction(phaseNumber) * 100
    gasDensity = fluid1.getPhase(phaseNumber).getDensity("kg/m3")
    gasZ = fluid1.getPhase(phaseNumber).getZ()
    gasMolarMass = fluid1.getPhase(phaseNumber).getMolarMass() * 1000
    gasEnthalpy = fluid1.getPhase(phaseNumber).getEnthalpy("J/mol")
    gasWtFraction = fluid1.getWtFraction(phaseNumber) * 100
    gasKappa = fluid1.getPhase(phaseNumber).getGamma()
    gasViscosity = fluid1.getPhase(phaseNumber).getViscosity("kg/msec")
    gasThermalConductivity = fluid1.getPhase(
        phaseNumber).getConductivity("W/mK")
    gasSoundSpeed = fluid1.getPhase(phaseNumber).getSoundSpeed()
    gasJouleThomsonCoefficient = fluid1.getPhase(
        phaseNumber).getJouleThomsonCoefficient() / 1e5

if fluid1.hasPhaseType("oil"):
    phaseNumber = fluid1.getPhaseNumberOfPhase("oil")
    oilFractionc = fluid1.getMoleFraction(phaseNumber) * 100
    oilMolarVolume = 1.0 / fluid1.getPhase(phaseNumber).getDensity("mol/m3")
    oilVolumeFraction = fluid1.getCorrectedVolumeFraction(phaseNumber) * 100
    oilDensity = fluid1.getPhase(phaseNumber).getDensity("kg/m3")
    oilZ = fluid1.getPhase(phaseNumber).getZ()
    oilMolarMass = fluid1.getPhase(phaseNumber).getMolarMass() * 1000
    oilEnthalpy = fluid1.getPhase(phaseNumber).getEnthalpy("J/mol")
    oilWtFraction = fluid1.getWtFraction(phaseNumber) * 100
    oilKappa = fluid1.getPhase(phaseNumber).getGamma()
    oilViscosity = fluid1.getPhase(phaseNumber).getViscosity("kg/msec")
    oilThermalConductivity = fluid1.getPhase(
        phaseNumber).getConductivity("W/mK")
    oilSoundSpeed = fluid1.getPhase(phaseNumber).getSoundSpeed()
    oilJouleThomsonCoefficient = fluid1.getPhase(
        phaseNumber).getJouleThomsonCoefficient() / 1e5

if fluid1.hasPhaseType("aqueous"):
    phaseNumber = fluid1.getPhaseNumberOfPhase("aqueous")
    aqueousFractionc = fluid1.getMoleFraction(phaseNumber) * 100
    aqueousMolarVolume = 1.0 / \
        fluid1.getPhase(phaseNumber).getDensity("mol/m3")
    aqueousVolumeFraction = fluid1.getCorrectedVolumeFraction(
        phaseNumber) * 100
    aqueousDensity = fluid1.getPhase(phaseNumber).getDensity("kg/m3")
    aqueousZ = fluid1.getPhase(phaseNumber).getZ()
    aqueousMolarMass = fluid1.getPhase(phaseNumber).getMolarMass() * 1000
    aqueousEnthalpy = fluid1.getPhase(phaseNumber).getEnthalpy("J/mol")
    aqueousWtFraction = fluid1.getWtFraction(phaseNumber) * 100
    aqueousKappa = fluid1.getPhase(phaseNumber).getGamma()
    aqueousViscosity = fluid1.getPhase(phaseNumber).getViscosity("kg/msec")
    aqueousThermalConductivity = fluid1.getPhase(
        phaseNumber).getConductivity("W/mK")
    aqueousSoundSpeed = fluid1.getPhase(phaseNumber).getSoundSpeed()
    aqueousJouleThomsonCoefficient = fluid1.getPhase(
        phaseNumber).getJouleThomsonCoefficient() / 1e5

# Examples of how to read component properties of a fluid
molFracComp1inPhase1 = fluid1.getPhase(0).getComponent(0).getx()
molarMasscComp1inPhase1 = fluid1.getPhase(0).getComponent(0).getMolarMass()
molesOfComp1inPhase1 = fluid1.getPhase(
    0).getComponent(0).getNumberOfMolesInPhase()
TCComp1inPhase1 = fluid1.getPhase(0).getComponent(0).getTC()
PCComp1inPhase1 = fluid1.getPhase(0).getComponent(0).getPC()
# a numer of properties can be read for both components and phases


# Example of how to read interfacial tension
if fluid1.hasPhaseType("gas") and fluid1.hasPhaseType("oil"):
    interfacialtensiongasoil = fluid1.getInterfacialTension('gas', 'oil')

if fluid1.hasPhaseType("gas") and fluid1.hasPhaseType("aqueous"):
    interfacialtensiongasaqueous = fluid1.getInterfacialTension(
        'gas', 'aqueous')

if fluid1.hasPhaseType("oil") and fluid1.hasPhaseType("aqueous"):
    interfacialtensionoilaqueous = fluid1.getInterfacialTension(
        'oil', 'aqueous')
# Display the fluid properties
# fluid1.display()
