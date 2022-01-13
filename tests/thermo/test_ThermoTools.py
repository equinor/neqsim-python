# import the package
from neqsim.thermo import (TPflash, addfluids, fluid, fluidComposition,
                           fluidflashproperties, hydt)
from numpy import isnan


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
    fluidcomposition = [0.01, 0.02, 0.9, 0.1,
                        0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
    fluidComposition(fluid1, fluidcomposition)
    fluid1.setPressure(101.0, "bara")
    fluid1.setTemperature(22.3, "C")
    TPflash(fluid1)
    fluid1.initThermoProperties()
    fluid1.initPhysicalProperties()
    assert abs(fluid1.getViscosity('kg/msec') - 1.574354015664789e-05) < 1e-19


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
    fluidcomposition = [0.01, 0.02, 0.9, 0.1,
                        0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
    fluidComposition(fluid1, fluidcomposition)
    fluid1.setPressure(101.0, "bara")
    fluid1.setTemperature(22.3, "C")
    TPflash(fluid1)
    fluid1.initProperties()
    assert fluid1.getNumberOfPhases() == 2


def test_fluidflashproperties():
    res = fluidflashproperties(
        300, 10, 'TP', None, ['methane', 'ethane'], [0.7, 0.3])

    assert int(res.fluidProperties[0][0]) == 1  # Check number of phases
    assert abs(res.fluidProperties[0][1] -
               float(10*1e5)) < 1e-8  # Correct pressure
    assert res.fluidProperties[0][2] == float(300)  # Correct temperature


def test_fluidflashproperties_online_fraction():
    res = fluidflashproperties(
        300, 10, 'TP', None, ['methane', 'ethane'], [0.7, 0.3])
    res2 = fluidflashproperties(
        300, 10, 'TP', None, ['methane', 'ethane'], [0.6, 0.4])

    res3 = fluidflashproperties([300, 300], [10, 10], 'TP', None, ['methane', 'ethane'], [
        [0.7, 0.6], [0.3, 0.4]])

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
    res_1 = fluidflashproperties(
        10, 300, 1, None, ['methane', 'ethane'], [0.7, 0.3])

    res_1_inverse = fluidflashproperties(
        300, 10, 1, None, ['methane', 'ethane'], [0.7, 0.3])

    assert abs(res_1.fluidProperties[0][1]/1e5 -
               res_1_inverse.fluidProperties[0][2]) < 1e-8
    assert abs(res_1.fluidProperties[0][2] -
               res_1_inverse.fluidProperties[0][1]/1e5) < 1e-8

    res_TP = fluidflashproperties(
        10, 300, 'TP', None, ['methane', 'ethane'], [0.7, 0.3])

    # Pressures are equal
    assert res_1.fluidProperties[0][1] == res_TP.fluidProperties[0][1]
    # Temperatures are equal
    assert res_1.fluidProperties[0][2] == res_TP.fluidProperties[0][2]

    res_PT = fluidflashproperties(
        300, 10, 'PT', None, ['methane', 'ethane'], [0.7, 0.3])

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

    fluid1 = fluid('cpa')
    fluid1.addComponent("nitrogen", nitrogen, 'mol/sec')
    fluid1.addComponent("CO2", CO2, 'mol/sec')
    fluid1.addComponent("methane", methane, 'mol/sec')
    fluid1.addComponent("ethane", ethane, 'mol/sec')
    fluid1.addComponent("propane", propane, 'mol/sec')
    fluid1.addComponent("i-butane", ibutane, 'mol/sec')
    fluid1.addComponent("n-butane", nbutane, 'mol/sec')
    fluid1.addComponent("water", water, 'mol/sec')
    fluid1.setMixingRule(10)
    fluid1.setPressure(pressure, 'bara')

    fluid2 = fluid('cpa')
    fluid2.addComponent("oxygen", nitrogen, 'mol/sec')
    fluid2.setMixingRule(10)

    fluid3 = addfluids(fluid1, fluid2)
    hydt(fluid3)
    print("Hydrate equilibrium temperature ",
          fluid3.getTemperature()-273.15, " C")
