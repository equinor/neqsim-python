# import the package
import pandas as pd
from pytest import approx
from neqsim.thermo import (
    TPflash,
    addfluids,
    fluid,
    fluid_df,
    fluidComposition,
    fluidflashproperties,
    hydt,
)
from numpy import isnan


def test_fluid_df_emptycomp():
    gascondensate = {
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
            "n-hexane",
            "C7",
            "C8",
            "C9",
            "C10",
            "C11",
            "C12",
            "C13",
            "C14",
            "C15",
            "C16",
            "C17",
            "C18",
            "C19",
            "C20",
        ],
        "MolarComposition[-]": [
            0.0,
            3.3,
            72.98,
            7.68,
            4.1,
            0.7,
            1.42,
            0.54,
            0.67,
            0.85,
            1.33,
            1.33,
            0.78,
            0.61,
            0.42,
            0.33,
            0.42,
            0.24,
            0.3,
            0.17,
            0.21,
            0.0,
            0.0,
            0.0,
        ],
        "MolarMass[kg/mol]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.0913,
            0.1041,
            0.1188,
            0.136,
            0.150,
            0.164,
            0.179,
            0.188,
            0.204,
            0.216,
            0.236,
            0.253,
            0.27,
            0.391,
        ],
        "RelativeDensity[-]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.746,
            0.768,
            0.79,
            0.787,
            0.793,
            0.804,
            0.817,
            0.83,
            0.835,
            0.843,
            0.837,
            0.84,
            0.85,
            0.877,
        ],
    }

    gascondensatedf = pd.DataFrame(gascondensate)
    naturalgasFluid = fluid_df(gascondensatedf)
    naturalgasFluid2 = fluid_df(gascondensatedf, add_all_components=False)
    assert naturalgasFluid.getNumberOfComponents() == 24
    assert naturalgasFluid2.getNumberOfComponents() == 20


def test_fluid_df_emptycomp3():
    gascondensate = {
        "ComponentName": ["nitrogen", "n-hexane", "C7"],
        "MolarComposition[-]": [1.0, 0.0, 72.98],
        "MolarMass[kg/mol]": [None, None, 0.0913],
        "RelativeDensity[-]": [None, None, 0.746],
    }

    gascondensatedf = pd.DataFrame(gascondensate)
    naturalgasFluid = fluid_df(gascondensatedf)
    naturalgasFluid2 = fluid_df(gascondensatedf, add_all_components=False)
    assert naturalgasFluid.getNumberOfComponents() == 3
    assert naturalgasFluid2.getNumberOfComponents() == 2


def test_fluid_df_emptycomp2():
    gascondensate = {
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
            "n-hexane",
            "C7",
            "C8",
            "C9",
            "C10",
            "C11",
            "C12",
            "C13",
            "C14",
            "C15",
            "C16",
            "C17",
            "C18",
            "C19",
            "C20",
        ],
        "MolarComposition[-]": [
            0.0,
            3.3,
            72.98,
            7.68,
            4.1,
            0.7,
            1.42,
            0.54,
            0.67,
            0.85,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        "MolarMass[kg/mol]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.0913,
            0.1041,
            0.1188,
            0.136,
            0.150,
            0.164,
            0.179,
            0.188,
            0.204,
            0.216,
            0.236,
            0.253,
            0.27,
            0.391,
        ],
        "RelativeDensity[-]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.746,
            0.768,
            0.79,
            0.787,
            0.793,
            0.804,
            0.817,
            0.83,
            0.835,
            0.843,
            0.837,
            0.84,
            0.85,
            0.877,
        ],
    }

    gascondensatedf = pd.DataFrame(gascondensate)
    naturalgasFluid = fluid_df(gascondensatedf)
    naturalgasFluid2 = fluid_df(gascondensatedf, add_all_components=False)
    assert naturalgasFluid.getNumberOfComponents() == 24
    assert naturalgasFluid2.getNumberOfComponents() == 9


def test_fluid_df():
    components = [
        "nitrogen",
        "CO2",
        "methane",
        "ethane",
        "propane",
        "i-butane",
        "n-butane",
        "i-pentane",
        "n-pentane",
        "n-hexane",
    ]
    composition = [
        0.633,
        1.371,
        85.697,
        6.914,
        3.086,
        0.475,
        0.886,
        0.242,
        0.254,
        0.016,
    ]
    naturalgas = {"ComponentName": components, "MolarComposition[-]": composition}
    naturalgasFluid = fluid_df(pd.DataFrame(naturalgas))


def test_TPflash1():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("CO2", 2.3, "mol/sec")
    fluid1.addComponent("methane", 80.0, "mol/sec")
    fluid1.addComponent("ethane", 6.0, "mol/sec")
    fluid1.addComponent("propane", 3.0, "mol/sec")
    fluid1.addComponent("i-butane", 1.0, "mol/sec")
    fluid1.addComponent("n-butane", 1.0, "mol/sec")
    fluid1.addComponent("i-pentane", 0.4, "mol/sec")
    fluid1.addComponent("n-pentane", 0.2, "mol/sec")
    fluid1.addComponent("n-hexane", 0.1, "mol/sec")
    fluid1.setMixingRule("classic")  # classic will use binary kij
    # True if more than two phases could be present
    fluid1.setMultiPhaseCheck(True)
    fluidcomposition = [0.01, 0.02, 0.9, 0.1, 0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
    fluidComposition(fluid1, fluidcomposition)
    fluid1.setPressure(101.0, "bara")
    fluid1.setTemperature(22.3, "C")
    TPflash(fluid1)
    fluid1.initThermoProperties()
    fluid1.initPhysicalProperties()
    assert abs(fluid1.getViscosity("kg/msec") - 1.574354015664789e-05) < 1e-19


def test_TPflash2():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("CO2", 2.3, "mol/sec")
    fluid1.addComponent("methane", 80.0, "mol/sec")
    fluid1.addComponent("ethane", 6.0, "mol/sec")
    fluid1.addComponent("propane", 3.0, "mol/sec")
    fluid1.addComponent("i-butane", 1.0, "mol/sec")
    fluid1.addComponent("n-butane", 1.0, "mol/sec")
    fluid1.addComponent("i-pentane", 0.4, "mol/sec")
    fluid1.addComponent("n-pentane", 0.2, "mol/sec")
    fluid1.addComponent("n-heptane", 10.1, "mol/sec")
    fluid1.setMixingRule("classic")  # classic will use binary kij
    # True if more than two phases could be present
    fluid1.setMultiPhaseCheck(True)
    fluidcomposition = [0.01, 0.02, 0.9, 0.1, 0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
    fluidComposition(fluid1, fluidcomposition)
    fluid1.setPressure(101.0, "bara")
    fluid1.setTemperature(22.3, "C")
    TPflash(fluid1)
    fluid1.initProperties()
    assert fluid1.getNumberOfPhases() == 2


def test_fluidflashproperties():
    res = fluidflashproperties(300, 10, "TP", None, ["methane", "ethane"], [0.7, 0.3])

    assert int(res.fluidProperties[0][0]) == 1  # Check number of phases
    assert abs(res.fluidProperties[0][1] - float(10 * 1e5)) < 1e-8  # Correct pressure
    assert res.fluidProperties[0][2] == float(300)  # Correct temperature


def test_fluidflashproperties_online_fraction():
    res = fluidflashproperties(300, 10, "TP", None, ["methane", "ethane"], [0.7, 0.3])
    res2 = fluidflashproperties(300, 10, "TP", None, ["methane", "ethane"], [0.6, 0.4])

    res3 = fluidflashproperties(
        [300, 300],
        [10, 10],
        "TP",
        None,
        ["methane", "ethane"],
        [[0.7, 0.6], [0.3, 0.4]],
    )

    for k in range(0, len(res3.fluidProperties[0])):
        if isnan(res.fluidProperties[0][k]):
            assert isnan(res3.fluidProperties[0][k])
        else:
            assert res3.fluidProperties[0][k] == res.fluidProperties[0][k]

        if isnan(res2.fluidProperties[0][k]):
            assert isnan(res3.fluidProperties[1][k])
        else:
            assert res3.fluidProperties[1][k] == res2.fluidProperties[0][k]


def test_fluidflashproperties_TP_PT():
    res_1 = fluidflashproperties(10, 300, 1, None, ["methane", "ethane"], [0.7, 0.3])

    res_1_inverse = fluidflashproperties(
        300, 10, 1, None, ["methane", "ethane"], [0.7, 0.3]
    )

    assert (
        abs(res_1.fluidProperties[0][1] / 1e5 - res_1_inverse.fluidProperties[0][2])
        < 1e-8
    )
    assert (
        abs(res_1.fluidProperties[0][2] - res_1_inverse.fluidProperties[0][1] / 1e5)
        < 1e-8
    )

    res_TP = fluidflashproperties(
        10, 300, "TP", None, ["methane", "ethane"], [0.7, 0.3]
    )

    # Pressures are equal
    assert res_1.fluidProperties[0][1] == res_TP.fluidProperties[0][1]
    # Temperatures are equal
    assert res_1.fluidProperties[0][2] == res_TP.fluidProperties[0][2]

    res_PT = fluidflashproperties(
        300, 10, "PT", None, ["methane", "ethane"], [0.7, 0.3]
    )

    # Pressures are equal
    assert res_1.fluidProperties[0][1] == res_PT.fluidProperties[0][1]
    # Temperatures are equal
    assert res_1.fluidProperties[0][2] == res_TP.fluidProperties[0][2]


def test_addfluid():
    pressure = 150.0

    nitrogen = 1.5
    CO2 = 2.5
    methane = 95.0
    ethane = 5.0
    propane = 2.5
    ibutane = 1.25
    nbutane = 1.25
    water = 10.25

    fluid1 = fluid("cpa")
    fluid1.addComponent("nitrogen", nitrogen, "mol/sec")
    fluid1.addComponent("CO2", CO2, "mol/sec")
    fluid1.addComponent("methane", methane, "mol/sec")
    fluid1.addComponent("ethane", ethane, "mol/sec")
    fluid1.addComponent("propane", propane, "mol/sec")
    fluid1.addComponent("i-butane", ibutane, "mol/sec")
    fluid1.addComponent("n-butane", nbutane, "mol/sec")
    fluid1.addComponent("water", water, "mol/sec")
    fluid1.setMixingRule(10)
    fluid1.setPressure(pressure, "bara")

    fluid2 = fluid("cpa")
    fluid2.addComponent("oxygen", nitrogen, "mol/sec")
    fluid2.setMixingRule(10)

    fluid3 = addfluids(fluid1, fluid2)
    hydt(fluid3)
    print("Hydrate equilibrium temperature ", fluid3.getTemperature() - 273.15, " C")


def test_fluidChar():
    import neqsim
    from neqsim.thermo import (
        fluid,
        fluid_df,
        addOilFractions,
        printFrame,
        dataFrame,
        fluidcreator,
        createfluid,
        createfluid2,
        TPflash,
        phaseenvelope,
    )
    import pandas as pd

    gascondensate = {
        "ComponentName": [
            "water",
            "H2S",
            "CO2",
            "nitrogen",
            "methane",
            "ethane",
            "propane",
            "i-butane",
            "n-butane",
            "i-pentane",
            "n-pentane",
            "n-hexane",
            "C7",
        ],
        "MolarComposition[-]": [
            10.1,
            0.001,
            0.53,
            3.3,
            72.98,
            7.68,
            4.1,
            0.7,
            1.42,
            0.54,
            0.67,
            0.85,
            10.33,
        ],
        "MolarMass[kg/mol]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.391,
        ],
        "RelativeDensity[-]": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.746,
        ],
    }

    gascondensatedf = pd.DataFrame(gascondensate)
    gascondensateFluid = fluid_df(
        gascondensatedf,
        lastIsPlusFraction=True,
        lumpComponents=False,
        numberOfLumpedComponents=12,
    )  # need to add number of pseudo components to 80 and distribution to gamma
    gascondensateFluid.setMultiPhaseCheck(True)
    TPflash(gascondensateFluid)
    assert gascondensateFluid.getNumberOfComponents() == 85

    compositon = gascondensateFluid.getMolarComposition()

    # Add mud contamination
    compositon[30] += compositon[30] + 0.01

    gascondensateFluid.setMolarComposition(compositon)
    gascondensateFluid.setTemperature(25.0, "C")
    gascondensateFluid.setPressure(5.0, "bara")
    TPflash(gascondensateFluid)


def test_TPflash():
    fluid1 = fluid("cpa")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("water", 1.0, "mol/sec")
    fluid1.setMixingRule(10)
    fluid1.setTemperature(293.15)
    fluid1.setPressure(125.0)
    TPflash(fluid1)
    assert fluid1.getPhase("gas").getZ() == approx(1.0262852545644505, rel=1e-6)
    TPflash(fluid1, temperature=20.0, tUnit="C", pressure=125.0, pUnit="bara")
    assert fluid1.getPhase("gas").getZ() == approx(1.0262852545644505, rel=1e-6)
    TPflash(fluid1, temperature=293.15, pressure=125.0)
    assert fluid1.getPhase("gas").getZ() == approx(1.0262852545644505, rel=1e-6)
