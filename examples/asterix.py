from neqsim.process import (
    clearProcess,
    heater,
    mixer,
    runProcess,
    separator3phase,
    splitter,
    stream,
)
from neqsim.thermo.thermoTools import *

model = "cpa-statoil"
mixrule = 10
# user settings
carryunderfrac = 3.0 / 100.0  # 0 mol% carryunder
filename = "asterix_results_2026_carryunder_3molpercent.csv"

# setting up data
components = [
    "nitrogen",
    "CO2",
    "methane",
    "ethane",
    "propane",
    "i-butane",
    "n-butane",
    "22-dim-C3",
    "i-pentane",
    "n-pentane",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11",
    "C12",
    "C13-C14",
    "C15",
    "C16-C17",
    "C18-C19",
    "C20-C23",
    "C24-C65",
    "water",
    "MEG",
]
hypos = [
    ("C6", 84.59999847, 667.9000244 / 1000.0),
    ("C7", 91.19999695, 737.7000122 / 1000.0),
    ("C8", 103.5999985, 769.00 / 1000.0),
    ("C9", 118.6999969, 780.2999878 / 1000.0),
    ("C10", 134.0, 797.9000244 / 1000.0),
    ("C11", 147.0, 802.2999878 / 1000.0),
    ("C12", 161.0, 811.9000244 / 1000.0),
    ("C13-C14", 181.7109985, 824.4000244 / 1000.0),
    ("C15", 206.0, 836.4000244 / 1000.0),
    ("C16-C17", 228.7109985, 846.5 / 1000.0),
    ("C18-C19", 256.368988, 859.0999756 / 1000.0),
    ("C20-C23", 293.506012, 874.5999756 / 1000.0),
    ("C24-C65", 390.9890137, 906.9000244 / 1000.0),
]

cond_comp = [
    0.1425,
    1.8105,
    34.3346,
    3.5247,
    3.8396,
    1.2513,
    2.5218,
    0.0384,
    1.6381,
    1.9624,
    3.7375,
    7.7388,
    8.8023,
    4.5450,
    4.4990,
    3.7517,
    2.9845,
    4.4192,
    1.5605,
    2.3410,
    1.5607,
    1.6908,
    1.3006,
    0.0045,
    0.0,
]  # mol%

gas_comp = [
    1.3855,
    1.5861,
    94.3498,
    1.7573,
    0.5940,
    0.0911,
    0.1225,
    0.0017,
    0.0347,
    0.0322,
    0.0224,
    0.0116,
    0.0054,
    0.0011,
    0.0004,
    0.0002,
    0.0001,
    0.0000,
    0.0000,
    0.0000,
    0.0000,
    0.0000,
    0.0000,
    0.0040,
    0.0,
]  # mol%
cond_rate = 145.0  # Am3/d
MEG_rate = 130.0  # Sm3/d
gas_rate = 10.0  # MSm3/d

# F1  F2  F3  F4  F5
T = [-15.0, 40.0, 40.0, 80.0, 90.0, 35]
P = [71.0135, 7.0, 3.5, 3.0, 0.15]
MEGwaterDensity = 1065.5
condDensity = 729.13

Tsens = [-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
Psens = 71.0135
MEGconcsens = [30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0]


# setting up initial fluids
# '''
cond = fluid(model)
k = 0
for i in range(len(cond_comp)):
    if i not in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
        cond.addComponent(components[i], cond_comp[i] / 100.0)
    else:
        cond.addTBPfraction(
            components[i], cond_comp[i] / 100.0, hypos[k][1] / 1000, hypos[k][2]
        )
        k = k + 1

cond.setTemperature(T[0], "C")
cond.setPressure(P[0], "bara")
print(cond_rate / 24.0 * condDensity)
cond.setTotalFlowRate(cond_rate / 24.0 * condDensity, "kg/hr")
cond.setMixingRule(mixrule)
cond.setMultiPhaseCheck(True)
TPflash(cond)
# printFrame(cond)

gas = fluid(model)
k = 0
for i in range(len(cond_comp)):
    if i not in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
        gas.addComponent(components[i], gas_comp[i] / 100.0)
    else:
        gas.addTBPfraction(
            components[i], gas_comp[i] / 100.0, hypos[k][1] / 1000, hypos[k][2]
        )
        k = k + 1

gas.setTemperature(T[0], "C")
gas.setPressure(P[0], "bara")
gas.setTotalFlowRate(gas_rate, "MSm^3/day")
gas.setMixingRule(mixrule)
gas.setMultiPhaseCheck(True)
TPflash(gas)
# printFrame(gas)

MEG = fluid(model)
MEG.addComponent("MEG", 60.0, "kg/sec")
MEG.addComponent("water", 40.0, "kg/sec")
MEG.setTemperature(T[0], "C")
MEG.setPressure(P[0], "bara")
MEG.setTotalFlowRate(MEG_rate / 24.0 * MEGwaterDensity, "kg/hr")
MEG.setMixingRule(mixrule)
MEG.setMultiPhaseCheck(True)
TPflash(MEG)
# printFrame(MEG)
# '''


clearProcess()

# INLET SEPARATOR (S1)
cond_in = stream(cond)
MEG_in = stream(MEG)
gas_in = stream(gas)
mix1 = mixer()
mix1.addStream(cond_in)
mix1.addStream(MEG_in)
mix1.addStream(gas_in)
TPflash(mix1.getOutStream().getThermoSystem())
S1 = separator3phase(mix1.getOutStream())
S1.setName("S1")

gas1 = S1.getGasOutStream()
MEG1 = S1.getWaterOutStream()
cond1 = S1.getOilOutStream()

# SECOND SEPARATOR (S2)
mix2 = mixer()
mix2.addStream(cond1)
mix2.addStream(MEG1)
heat2 = heater(mix2.getOutStream())
heat2.setOutTemperature(T[1] + 273.15)
heat2.setOutPressure(P[1])
S2 = separator3phase(heat2.getOutStream())
S2.setName("S2")
gas2 = S2.getGasOutStream()
MEG2 = S2.getWaterOutStream()
cond2 = S2.getOilOutStream()


# THIRD SEPARATOR (S3)
# make split
split = splitter(cond2, [carryunderfrac, 1.0 - carryunderfrac])
carryunder = split.getSplitStream(0)


# mix, set new condition, separate
mix3 = mixer()
mix3.addStream(carryunder)
mix3.addStream(MEG2)
MEG2_plus_carryunder = mix3.getOutStream()
heat3 = heater(MEG2_plus_carryunder)
heat3.setOutTemperature(T[2] + 273.15)
heat3.setOutPressure(P[2])
S3 = separator3phase(heat3.getOutStream())
S3.setInletStream(heat3.getOutStream())
S3.setName("S3")
gas3 = S3.getGasOutStream()
MEG3 = S3.getWaterOutStream()
cond3 = S3.getOilOutStream()

runProcess()


# S1.display()
# TPflash(gas3.getThermoSystem())
# gas3.getThermoSystem().init(0)
# gas3.getThermoSystem().setNumberOfPhases(1)
printFrame(gas3.getThermoSystem())
print(gas3.getThermoSystem().getFlowRate("m3/hr"))
