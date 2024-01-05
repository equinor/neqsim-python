# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:16:07 2020

@author: esol
"""
import pandas as pd
from neqsim.thermo import TPflash, dewt, fluid_df, phaseenvelope, printFrame

naturalgas = {
    "ComponentName": [
        "nitrogen",
        "CO2",
        "methane",
        "ethane",
        "propane",
        "i-butane",
        "n-butane",
        "i-pentane",
        "n-pentane",
        "2-m-C5",
        "3-m-C5",
        "n-hexane",
        "benzene",
        "c-hexane",
        "n-heptane",
        "toluene",
        "c-C7",
        "n-octane",
        "m-Xylene",
        "c-C8",
        "n-nonane",
        "m-Xylene",
        "nC10",
        "nC11",
        "nC12",
    ],
    "MolarComposition[-]": [
        1.192,
        0.5102,
        95.3303,
        2.1102,
        0.3217,
        0.1278,
        0.0846,
        0.0694,
        0.0340,
        0.0335,
        0.0109,
        0.0181,
        0.0017,
        0.0661,
        0.0207,
        0.0045,
        0.0530,
        0.0061,
        0.0033,
        0.000103,
        0.0032,
        0.00354,
        0.00597,
        0.0000597,
        0.000001,
    ],
}


naturalgasdf = pd.DataFrame(naturalgas)
print("Natural Gas Fluid:\n")
print(naturalgasdf.head(30).to_string())

naturalgasFluid = fluid_df(naturalgasdf).setModel("UMR-PRU-EoS")
naturalgasFluid.autoSelectMixingRule()
TPflash(naturalgasFluid)
printFrame(naturalgasFluid)

gasPhaseEnvelope = phaseenvelope(naturalgasFluid, True)
cricobar = gasPhaseEnvelope.get("cricondenbar")
print("cricoP ", cricobar[1], "  [bara] ", " cricoT ", cricobar[0], " °C")


naturalgasFluid.setTemperature(-10.0, "C")
naturalgasFluid.setPressure(21.0, "bara")
TPflash(naturalgasFluid)
printFrame(naturalgasFluid)


naturalgasFluid.setPressure(21.0, "bara")
dewPointT = dewt(naturalgasFluid) - 273.15
print("dew point T ", dewPointT, " °C")
