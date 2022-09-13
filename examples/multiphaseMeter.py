import math

import matplotlib
import matplotlib.pyplot as plt
import neqsim
import numpy
import numpy as np
import pandas as pd
from neqsim.thermo.thermoTools import *

# 1. Collection of fluid composition and PVT data from PVTreport. Evaluation of data.


definedComponents = ['nitrogen', 'CO2', 'methane', 'ethane',
                     'propane', 'i-butane', 'n-butane', 'i-pentane', 'n-pentane']
definedmolefractions = [0.972, 0.632, 95.111,
                        2.553, 0.104, 0.121, 0.021, 0.066, 0.02]
oilComponents = ["C6", "C7", "C8", "C9", "C10"]
oilComponentsMoleFractions = [0.058, 0.107, 0.073, 0.044, 0.118]
oilComponentsMolarMass = [86.18/1000.0, 96.0/1000.0,
                          107.0/1000.0, 121.0/1000.0, 202.0/1000.0]  # kg/mol
oilComponentsRelativeDensity = [
    664.0e-3, 738.0e-3, 765.0e-3, 781.0e-3, 813.30e-3]  # gr/cm3

#definedComponentArray = np.asarray([definedComponents,definedmolefractions,Zgas, isothermalcompressibility,liquidrelativevolume])
compositionDataFrame = pd.DataFrame(
    definedmolefractions, index=definedComponents, columns=["mole fraction"])
oilComponentsDataFrame = pd.DataFrame(numpy.transpose([oilComponentsMoleFractions, oilComponentsMolarMass, oilComponentsRelativeDensity]), index=oilComponents, columns=[
                                      "mole fraction", "molar mass [kg/mole]", " density [gr/cm3]"])

print(compositionDataFrame.head(50).to_string())
print(oilComponentsDataFrame.head(50).to_string())


# 2. Data from PVT report
reservoirTemperature = 80.6  # Celius
reservoirPressure = 320.8  # bara

testSeparatorTemperature = 20.6  # Celcius
testSeparatorPressure = 86.8  # bara
GORseparartorConditions = 35000.0  # Sm3 gas/m3 oil

GORstandardConditions = 55000.0  # Sm3 gas/m3 oil


# Define a dictionary containing Students data
PVTdata = {'pressure':  [555.3, 552, 518.5, 484, 449.5, 415.3, 408.1, 401.3, 394.3, 387.3, 380.7, 373.8, 366.7, 360, 352.9, 346.2, 339.3, 332.3, 329.9, 325.6, 320, 315.1, 308.4, 301.3, 294.5, 287.6, 280.6, 273.8, 266.9, 259.9, 253.1, 249.5, 246.1, 242.7, 208.2, 173.6, 139, 104.5, 70, 46.1],
           'relative volume': [0.741, 0.7431, 0.766, 0.7917, 0.821, 0.8551, 0.8631, 0.871, 0.8795, 0.8883, 0.8972, 0.9066, 0.9169, 0.9272, 0.9385, 0.9498, 0.9621, 0.9751, 0.9797, 0.9883, 1, 1.0105, 1.0258, 1.0428, 1.0602, 1.0787, 1.0989, 1.1197, 1.1423, 1.1668, 1.1924, 1.2064, 1.2202, 1.2346, 1.4135, 1.6806, 2.1038, 2.8422, 4.3612, 6.796],
           'Zgas': [1.247, 1.244, 1.204, 1.162, 1.119, 1.077, 1.068, 1.06, 1.051, 1.043, 1.035, 1.027, 1.019, 1.012, 1.004, 0.997, 0.99, 0.982, 0.98, 0.976, 0.97, 0.965, 0.959, 0.952, 0.946, 0.941, 0.935, 0.929, 0.924, 0.919, 0.915, 0.912, 0.91, 0.908, 0.892, 0.884, 0.887, 0.9, 0.926, 0.95],
           'Density': [0.2671, 0.2663, 0.2583, 0.2499, 0.241, 0.2314, 0.2293, 0.2272, 0.225, 0.2227, 0.2206, 0.2183, 0.2158, 0.2134, 0.2108, 0.2083, 0.2057, 0.2029, 0.202, 0.2002, 0.1979, 0.1958, 0.1929, 0.1898, 0.1866, 0.1834, 0.1801, 0.1767, 0.1732, 0.1696, 0.1659, 0.164, 0.1622, 0.1603, 0.14, 0.1177, 0.0941, 0.0696, 0.0454, 0.0291],
           'Bg': [0.0027, 0.0027, 0.0028, 0.0029, 0.003, 0.0032, 0.0032, 0.0032, 0.0032, 0.0033, 0.0033, 0.0033, 0.0034, 0.0034, 0.0035, 0.0035, 0.0036, 0.0036, 0.0036, 0.0036, 0.0037, 0.0037, 0.0038, 0.0038, 0.0039, 0.004, 0.0041, 0.0041, 0.0042, 0.0043, 0.0044, 0.0045, 0.0045, 0.0046, 0.0052, 0.0062, 0.0078, 0.0105, 0.0161, 0.0251],
           'gasexpansionfactor': [365.6, 364.6, 353.7, 342.2, 330, 316.8, 313.9, 311, 308, 305, 302, 298.8, 295.5, 292.2, 288.7, 285.2, 281.6, 277.8, 276.5, 274.1, 270.9, 268.1, 264.1, 259.8, 255.5, 251.1, 246.5, 241.9, 237.2, 232.2, 227.2, 224.6, 222, 219.4, 191.7, 161.2, 128.8, 95.3, 62.1, 39.9],
           'gasviscosity': [0.0325, 0.0324, 0.0313, 0.0301, 0.0288, 0.0276, 0.0273, 0.027, 0.0268, 0.0265, 0.0262, 0.0259, 0.0257, 0.0254, 0.0251, 0.0248, 0.0245, 0.0243, 0.0242, 0.024, 0.0237, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
           }


# Convert the dictionary into DataFrame
CMEdataFrame = pd.DataFrame(PVTdata)
CMEpressures = CMEdataFrame['pressure'].tolist()
CMEtemperature = [80.6+273.15]*len(CMEpressures)
#CMEdataFrame = pd.DataFrame(numpy.transpose([CMEpressures, CMErelativevolume]), columns=["pressure", "relative volume"])
print(CMEdataFrame.head(50).to_string())

print("plotting experimental PVT data.....")
CMEdataFrame.plot(kind='scatter', x='relative volume',
                  y='pressure', color='red')
plt.show()


# Running PVTsimulation with default fluid
fluidDefinedComponents = createfluid2(
    definedComponents, definedmolefractions, "mol/sec")
characterizedFluid = addOilFractions(fluidDefinedComponents, oilComponents,
                                     oilComponentsMoleFractions, oilComponentsMolarMass,  oilComponentsRelativeDensity)

characterizedFluid.setTemperature(15.0, "C")
characterizedFluid.setPressure(1.0, "atm")
TPflash(characterizedFluid)
# printFLuidCharacterisation(characterizedFluid) #print componentnames, TC, PC, acs, molar mass, density,
printFrame(characterizedFluid)
GORcalcstd = characterizedFluid.getPhase("gas").getNumberOfMolesInPhase(
)*8.314*288.15/101325 / (characterizedFluid.getPhase("oil").getVolume("m3"))
print("GOR at standard conditions ", GORcalcstd, " Sm3 gas/m3 oil. ",
      " Deviation from PVT report: ", (GORcalcstd-GORstandardConditions)/GORstandardConditions*100, " %")

characterizedFluid.setTemperature(testSeparatorTemperature, "C")
characterizedFluid.setPressure(testSeparatorPressure, "bara")
TPflash(characterizedFluid)
GORcalc = characterizedFluid.getPhase("gas").getNumberOfMolesInPhase(
)*8.314*288.15/101325 / (characterizedFluid.getPhase("oil").getVolume("m3"))
print("GOR at test separator conditions: ", GORcalc, " Sm3 gas/m3 oil",
      " Deviation from PVT report: ", (GORcalc-GORseparartorConditions)/GORseparartorConditions*100, " %")

# Calculating saturation pressure
#characterizedFluid.setTemperature(reservoirTemperature, "C")
#calcSatPres = saturationpressure(characterizedFluid)
#print("Saturation pressure : ", calcSatPres, " [bara]" , " Deviation from PVT report: ", (calcSatPres-reservoirPressure), " bar")


simrelativevolume = []
simliquidrelativevolume = []
Zgas = []
Bgsim = []
densitysim = []
Yfactor = []
isothermalcompressibility = []
gasviscositysim = []
saturationPressure = None
CME(characterizedFluid, CMEpressures, CMEtemperature, saturationPressure, simrelativevolume,
    simliquidrelativevolume, Zgas, Yfactor, isothermalcompressibility, densitysim, Bgsim, gasviscositysim)
CMEsimdataFrame = pd.DataFrame(numpy.transpose([CMEpressures, simrelativevolume, Zgas, densitysim, Bgsim, gasviscositysim]), columns=[
                               "pressure", "sim relative volume", "Zgassim", "densitysim", "Bgsim", "gasviscositysim"])
print(CMEsimdataFrame.head(50).to_string())
print("saturation pressure simulated ", saturationPressure)
pd.concat([CMEdataFrame['pressure'], CMEdataFrame['relative volume'],
          CMEsimdataFrame['sim relative volume']], axis=1).plot(x='pressure')
pd.concat([CMEdataFrame['pressure'], CMEdataFrame['Zgas'],
          CMEsimdataFrame['Zgassim']], axis=1).plot(x='pressure')
pd.concat([CMEdataFrame['pressure'], CMEdataFrame['Density']*1e3,
          CMEsimdataFrame['densitysim']], axis=1).plot(x='pressure')
pd.concat([CMEdataFrame['pressure'], CMEdataFrame['Bg'],
          CMEsimdataFrame['Bgsim']], axis=1).plot(x='pressure')
pd.concat([CMEdataFrame['pressure'], CMEdataFrame['gasviscosity'],
          CMEsimdataFrame['gasviscositysim']*1e3], axis=1).plot(x='pressure', kind="line")

matplotlib.pyplot.show()

devanalysisframe = pd.concat([CMEdataFrame['pressure'], (CMEsimdataFrame['sim relative volume'] -
                             CMEdataFrame['relative volume'])/CMEdataFrame['relative volume']*100.0], axis=1)
print("Deviation analysis...")
print("Average deviation relative volume: ", devanalysisframe[0].mean(
), " %", "  Max devation ", devanalysisframe[0].max(), " %")


# Optimizing fluid characterization for better PVT repretation
# To be done

# Creating property tables
pressures = [150.0, 170.0, 180.0, 200.0, 270.0, 320.0, 400.0]
temperatures = [30.0, 40.0, 50.0, 60.0, 80.0]

numP = len(pressures)
numT = len(temperatures)

gasViscosity = numpy.zeros((numP, numT))
oilViscosity = numpy.zeros((numP, numT))
gasDensity = numpy.zeros((numP, numT))
oilDensity = numpy.zeros((numP, numT))
GORcalc = numpy.zeros((numP, numT))
GORactual = numpy.zeros((numP, numT))
gasViscosity[:] = np.NaN
oilViscosity[:] = np.NaN
gasDensity[:] = np.NaN
oilDensity[:] = np.NaN
GORcalc[:] = np.NaN
GORactual[:] = np.NaN

for i in range(len(temperatures)):
    for j in range(len(pressures)):
        characterizedFluid.setPressure(pressures[j])
        characterizedFluid.setTemperature(temperatures[i]+273.15)
        TPflash(characterizedFluid)
        characterizedFluid.initProperties()
        if (characterizedFluid.hasPhaseType("gas")):
            gasViscosity[j][i] = characterizedFluid.getPhase(
                "gas").getViscosity("cP")
            gasDensity[j][i] = characterizedFluid.getPhase(
                "gas").getDensity("kg/m3")
        if (characterizedFluid.hasPhaseType("oil")):
            oilViscosity[j][i] = characterizedFluid.getPhase(
                "oil").getViscosity("cP")
            oilDensity[j][i] = characterizedFluid.getPhase(
                "oil").getDensity("kg/m3")
        if (characterizedFluid.hasPhaseType("gas") and characterizedFluid.hasPhaseType("oil")):
            GORcalc[j][i] = characterizedFluid.getPhase("gas").getNumberOfMolesInPhase(
            )*8.314*288.15/101325 / (characterizedFluid.getPhase("oil").getVolume("m3"))
            GORactual[j][i] = (characterizedFluid.getPhase("gas").getVolume(
                "m3")) / (characterizedFluid.getPhase("oil").getVolume("m3"))

gasDensityDataFrame = pd.DataFrame(
    gasDensity, index=pressures, columns=temperatures)
oilDensityDataFrame = pd.DataFrame(
    oilDensity, index=pressures, columns=temperatures)
gasviscosityDataFrame = pd.DataFrame(
    gasViscosity, index=pressures, columns=temperatures)
oilviscosityDataFrame = pd.DataFrame(
    oilViscosity, index=pressures, columns=temperatures)
GORcalcFrame = pd.DataFrame(GORcalc, index=pressures, columns=temperatures)
GORactualFrame = pd.DataFrame(GORactual, index=pressures, columns=temperatures)

print("gas density [kg/m3]")
print(gasDensityDataFrame.tail())
print("oil density [kg/m3]")
print(oilDensityDataFrame.head())
print("gas viscosity [(mPa.s)]")
print(gasviscosityDataFrame.tail())
print("oil viscosity [(mPa.s)]")
print(oilviscosityDataFrame.head())
print("GOR actual (Sm3/Sm3)")
print(GORactualFrame.head())
