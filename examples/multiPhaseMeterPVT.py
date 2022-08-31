import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from neqsim.thermo.thermoTools import *

names = ['nitrogen', 'CO2', 'methane', 'ethane', 'propane',
         'i-butane', 'n-butane', 'i-pentane', 'n-pentane']
molefractions = [0.972, 0.632, 95.111, 2.553, 0.104, 0.121, 0.021, 0.066, 0.02]
fluidDefinedComponents = createfluid2(names, molefractions, "mol/sec")

charNames = ["C6", "C7", "C8", "C9", "C10"]
charFlowrate = [0.058, 0.107, 0.073, 0.044, 0.118]
molarMass = [86.18/1000.0, 96.0/1000.0,
             107.0/1000.0, 121.0/1000.0, 202.0/1000.0]
density = [664.0e-3, 738.0e-3, 765.0e-3, 781.0e-3, 813.30e-3]
characterizedFluid = addOilFractions(
    fluidDefinedComponents, charNames, charFlowrate, molarMass,  density)
# printFrame(characterizedFluid)
characterizedFluid.setTemperature(273.15+20.6)
characterizedFluid.setPressure(86.8)
TPflash(characterizedFluid)
GORcalc = characterizedFluid.getPhase("gas").getNumberOfMolesInPhase(
)*8.314*288.15/101325 / (characterizedFluid.getPhase("oil").getVolume("m3"))
print("GOR test sep ", GORcalc)

characterizedFluid.setTemperature(273.15+15.0)
characterizedFluid.setPressure(1.01325)
TPflash(characterizedFluid)
GORcalcstd = characterizedFluid.getPhase("gas").getNumberOfMolesInPhase(
)*8.314*288.15/101325 / (characterizedFluid.getPhase("oil").getVolume("m3"))
print("GOR standard ", GORcalcstd)

characterizedFluid.setTemperature(273.15+73.6)
characterizedFluid.setPressure(290.8)
TPflash(characterizedFluid)
printFrame(characterizedFluid)
print('phase envelope for characterized fluid')
phaseenvelope(characterizedFluid, True)


pressure = [555.3, 500.0, 400.0, 350.0, 300.0,
            250.0, 230.0, 190.0, 150.0, 100.0, 50.0, 46.1]
temperature = [273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15 +
               73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0, 273.15+73.0]
satPressure = 0
relative_volume = []
liquidrelativevolume = []
Zgas = []
Yfactor = []
isothermalcompressibility = []

CME(characterizedFluid, pressure, temperature, satPressure, relative_volume,
    liquidrelativevolume, Zgas, Yfactor, isothermalcompressibility)

plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, relative_volume, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('relative volume [-]')
plt.subplot(132)
plt.plot(pressure, Yfactor, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('Yfactor [-]')
plt.subplot(133)
plt.plot(pressure, isothermalcompressibility, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('isothermalcompressibility [1/bar]')
plt.show()

Yfactorarray = np.asarray(
    [relative_volume, Yfactor, Zgas, isothermalcompressibility, liquidrelativevolume])
pressurearray = np.asarray(pressure)
temperaturearray = np.asarray(temperature)
YfactorFrame = pd.DataFrame(Yfactorarray.transpose(), index=pressurearray, columns=[
                            "relative_volume", "Yfactor", "Zgas", "isothermalcompressibility", "liquidrelativevolume"])
print("sat pressure ", satPressure)
print("YfactorFrame")
print(YfactorFrame.head(20).to_string())


pressures = [150.0, 170.0, 180.0, 200.0, 270.0, 320.0, 400.0]
temperatures = [30.0, 40.0, 50.0, 60.0, 80.0]

numP = len(pressures)
numT = len(temperatures)

gasViscosity = np.zeros((numP, numT))
oilViscosity = np.zeros((numP, numT))
gasDensity = np.zeros((numP, numT))
oilDensity = np.zeros((numP, numT))
GORcalc = np.zeros((numP, numT))
GORactual = np.zeros((numP, numT))
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
        if(characterizedFluid.hasPhaseType("gas")):
            gasViscosity[j][i] = characterizedFluid.getPhase(
                "gas").getViscosity("cP")
            gasDensity[j][i] = characterizedFluid.getPhase(
                "gas").getDensity("kg/m3")
        if(characterizedFluid.hasPhaseType("oil")):
            oilViscosity[j][i] = characterizedFluid.getPhase(
                "oil").getViscosity("cP")
            oilDensity[j][i] = characterizedFluid.getPhase(
                "oil").getDensity("kg/m3")
        if(characterizedFluid.hasPhaseType("gas") and characterizedFluid.hasPhaseType("oil")):
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

print("gas density")
print(gasDensityDataFrame.tail())
print("oil density")
print(oilDensityDataFrame.head())
print("gas viscosity")
print(gasviscosityDataFrame.tail())
print("oil viscosity")
print(oilviscosityDataFrame.head())
print("GOR actual")
print(GORactualFrame.head())
