# import the package
from neqsim.process.processTools import (
    separator,
    pump,
    heater,
    separator3phase,
    compsplitter,
    waterDewPointAnalyser,
    hydrateEquilibriumTemperatureAnalyser,
    virtualstream,
    clearProcess,
    newProcess,
    runProcess,
    stream,
    runProcessAsThread,
    mixer,
    compressor,
    recycle,
    splitter,
    valve,
)
from neqsim.thermo import TPflash, fluid, printFrame, fluid_df
from pytest import approx
from jpype.types import JDouble
from neqsim import jneqsim
import pandas as pd
import neqsim.standards


def test_compsplitter():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("CO2", 2.3, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream("stream1", fluid1)
    splittcomp = compsplitter("splitter 1", stream1, [1.0, 0.0])
    runProcess()
    TPflash(splittcomp.getSplitStream(0).getFluid())
    printFrame(splittcomp.getSplitStream(0).getFluid())
    assert splittcomp.getSplitStream(0).getFluid().getViscosity("kg/msec") > 1e-19


def test_waterDewPointAnalyser():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("water", 50e-6, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream("stream1", fluid1)
    waterDewPoint = waterDewPointAnalyser("water", stream1)
    runProcess()
    assert waterDewPoint.getMeasuredValue("C") == approx(-11.828217379989212, rel=0.001)


def test_hydrateEquilibriumTemperatureAnalyser():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("methane", 5, "mol/sec")
    fluid1.addComponent("ethane", 1, "mol/sec")
    fluid1.addComponent("propane", 1, "mol/sec")
    fluid1.addComponent("water", 50e-6, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream("stream1", fluid1)
    hydrateDewPoint = hydrateEquilibriumTemperatureAnalyser("analyser1", stream1)
    runProcess()
    assert hydrateDewPoint.getMeasuredValue("C") == approx(-25.204324, rel=0.001)


def test_runProcessAsThread():
    """
    In the test_runProcessAsThread() we set up a process and run it as a thread.
    We will start the thread and check that the calculated value is diferent from the final results.
    Then we set maximum calculation time to 10 sec and finish the calculation and check the results is ok.
    """
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("water", 50e-6, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream("stream1", fluid1)
    waterDewPoint = waterDewPointAnalyser("analy", stream1)
    stream2 = stream("stream2", fluid1)
    waterDewPoint2 = waterDewPointAnalyser("anal1", stream2)
    stream3 = stream("stream3", fluid1)
    waterDewPoint3 = waterDewPointAnalyser("water2", stream3)
    processThread = runProcessAsThread()
    # assert waterDewPoint2.getMeasuredValue('C') != approx(-11.828217379989212, rel= 0.001)
    processThread.join(10000)  # max 10 sec calculation time
    assert waterDewPoint2.getMeasuredValue("C") == approx(
        -11.828217379989212, rel=0.001
    )


def test_newprocess():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("CO2", 2.3, "mol/sec")
    fluid1.setMixingRule(2)
    stream1 = stream("str11", fluid1)
    splittcomp = compsplitter("split1", stream1, [1.0, 0.0])
    runProcess()
    newProcess()
    stream1 = stream("str2", fluid1)
    splittcomp = compsplitter("split2", stream1, [1.0, 0.0])
    runProcess()
    TPflash(splittcomp.getSplitStream(0).getFluid())
    # assert splittcomp.getSplitStream(0).getFluid().getViscosity('kg/msec') > 1e-19


def test_flowSplitter():
    temperature_inlet = 35.0
    pressure_inlet = 55.0
    pressure_outlet = 100.0
    gasFlowRate = 5.0

    fluid1 = fluid("srk")
    fluid1.addComponent("methane", 1.0)

    clearProcess()

    stream1 = stream("str1", fluid1)
    stream1.setPressure(pressure_inlet, "bara")
    stream1.setTemperature(temperature_inlet, "C")
    stream1.setFlowRate(gasFlowRate, "MSm3/day")

    streamresycl = stream("str2", stream1.getFluid().clone())
    streamresycl.setFlowRate(0.1, "MSm3/day")

    mixerStream = mixer("mixer1")
    mixerStream.addStream(stream1)
    mixerStream.addStream(streamresycl)

    compressor_1 = compressor("comp1", mixerStream.getOutletStream(), pressure_outlet)

    stream2 = stream("stre333", compressor_1.getOutStream())

    streamSplit = splitter("split1", stream2)
    streamSplit.setFlowRates(JDouble[:]([5.0, 0.1]), "MSm3/day")

    resycStream1 = streamSplit.getSplitStream(1)

    valve1 = valve("valv1", resycStream1)
    valve1.setOutletPressure(pressure_inlet, "bara")

    resycleOp = recycle("rec1")
    resycleOp.addStream(valve1.getOutletStream())
    resycleOp.setOutletStream(streamresycl)
    resycleOp.setFlowTolerance(1e-4)

    exportStream = stream("stre3", streamSplit.getSplitStream(0))
    runProcess()
    assert exportStream.getFlowRate("MSm3/day") == approx(5.0)
    assert streamresycl.getFlowRate("MSm3/day") == approx(0.1)

    streamSplit.setFlowRates(JDouble[:]([5, 0.5]), "MSm3/day")
    runProcess()
    assert exportStream.getFlowRate("MSm3/day") == approx(5.0)
    assert streamresycl.getFlowRate("MSm3/day") == approx(0.5)

    streamSplit.setFlowRates(JDouble[:]([-1, 2.5]), "MSm3/day")
    runProcess()
    assert exportStream.getFlowRate("MSm3/day") == approx(5.0)
    assert streamresycl.getFlowRate("MSm3/day") == approx(2.5)

    streamSplit.setSplitFactors(JDouble[:]([1.0, 0.0]))
    runProcess()
    assert exportStream.getFlowRate("MSm3/day") == approx(5.0)
    assert streamresycl.getFlowRate("MSm3/day") == approx(0.0)


def test_virtualstream():
    fluid1 = fluid("srk")
    fluid1.addComponent("methane", 1.0)

    clearProcess()
    stream1 = stream("str1", fluid1)
    stream1.setFlowRate(3.1, "MSm3/day")
    vstream = virtualstream("str2", stream1)
    vstream.setFlowRate(1.1, "MSm3/day")
    vstream.setTemperature(25.0, "C")
    vstream.setPressure(25.0, "bara")
    runProcess()
    assert stream1.getFlowRate("MSm3/day") == approx(3.1)
    assert vstream.getOutStream().getFlowRate("MSm3/day") == approx(1.1)


# Example of a method using direct calls to neqsim java
def testNoUseOfThermosOrProcessTools():
    fluid = jneqsim.thermo.system.SystemSrkEos((273.15 + 25.0), 10.00)
    fluid.addComponent("methane", 0.900)
    fluid.addComponent("ethane", 0.100)
    fluid.addComponent("n-heptane", 1.00)
    fluid.setMixingRule(2)

    stream1 = jneqsim.process.equipment.stream.Stream("Stream1", fluid)
    stream1.setPressure(10.0, "bara")
    stream1.setTemperature(25.0, "C")
    stream1.setFlowRate(50.0, "kg/hr")

    valve1 = jneqsim.process.equipment.valve.ThrottlingValve(
        "valve_1", stream1
    )
    valve1.setOutletPressure(5.0, "bara")

    separator1 = jneqsim.process.equipment.separator.Separator("sep 1")
    separator1.addStream(valve1.getOutStream())

    operation = jneqsim.process.processmodel.ProcessSystem()
    operation.add(stream1)
    operation.add(valve1)
    operation.add(separator1)

    operation.run()

    print(
        "temperature ", operation.getUnit("sep 1").getGasOutStream().getTemperature("C")
    )
    assert operation.getUnit("sep 1").getGasOutStream().getFlowRate("kg/hr") == approx(
        7.580303857
    )


def test_gasoilprocess():
    ASGAwell = {
        "ComponentName": [
            "water",
            "nitrogen",
            "CO2",
            "methane",
            "ethane",
            "propane",
            "i-butane",
            "n-butane",
            "iC5",
            "nC5",
            "C6",
            "C7",
            "C8",
            "C9",
            "C10_C12",
            "C13_C14",
            "C15_C16",
            "C17_C19",
            "C20_C22",
            "C23_C25",
            "C26_C30",
            "C31_C38",
            "C39_C80",
        ],
        "MolarComposition[-]": [
            0.034266,
            0.005269,
            0.039189,
            0.700553,
            0.091154,
            0.050908,
            0.007751,
            0.014665,
            0.004249,
            0.004878,
            0.004541,
            0.007189,
            0.006904,
            0.004355,
            0.007658,
            0.003861,
            0.003301,
            0.002624,
            0.001857,
            0.001320,
            0.001426,
            0.001164,
            0.000916,
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
            0.08618,
            0.09096,
            0.10343,
            0.11719,
            0.14581,
            0.18133,
            0.21228,
            0.24814,
            0.28922,
            0.33034,
            0.38470,
            0.47116,
            0.66246,
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
            0.66266,
            0.74084,
            0.76922,
            0.78921,
            0.80411,
            0.82491,
            0.83780,
            0.84946,
            0.86331,
            0.87527,
            0.88783,
            0.90479,
            0.92660,
        ],
    }

    ASGAfluid_df = pd.DataFrame(ASGAwell)
    ASGAFluid = fluid_df(ASGAfluid_df, lastIsPlusFraction=False)
    ASGAFluid.setMixingRule("classic")

    reffluidrate = 604094.0
    feedTemperature = 25.5 + 273.15
    feedPressure = 26.0
    MPpressure = 19.0
    LPpressure = 2.7
    LPMidpressure = 7.3
    P_1st_comp = LPpressure - 0.03

    WellFluid2 = ASGAFluid

    clearProcess()

    # Well stream
    wstream_inlet = stream("str11", WellFluid2)
    wstream_inlet.setTemperature(feedTemperature, "K")
    wstream_inlet.setPressure(feedPressure, "bara")
    wstream_inlet.setFlowRate(reffluidrate, "kg/hr")

    # Separator train
    separator1 = separator3phase("inlet separator", wstream_inlet)
    valve1 = valve("HP oil valve", separator1.getOilOutStream(), MPpressure)
    Oilheater1 = heater("heater 2", valve1.getOutletStream())
    Oilheater1.setOutTemperature(359.15)
    separator2 = separator3phase("MP separator", Oilheater1.getOutStream())
    valve2 = valve("valv1", separator2.getOilOutStream(), LPpressure)
    recirc1stream = stream("str1", valve2.getOutletStream().clone())
    recirc2stream = stream("str2", valve2.getOutletStream().clone())
    recirc3stream = stream("str3", valve2.getOutletStream().clone())
    separator3 = separator3phase("LP separator", valve2.getOutletStream())
    separator3.addStream(recirc1stream)
    separator3.addStream(recirc2stream)
    separator3.addStream(recirc3stream)

    # 1st stg compressor
    pipeloss1st = valve("vlv1", separator3.getGasOutStream(), P_1st_comp)
    coolerLP1 = heater("cooler1", pipeloss1st.getOutletStream())
    coolerLP1.setOutTemperature(298.15)
    scrubberLP1 = separator("sep1", coolerLP1.getOutletStream())
    compressorLP1 = compressor("comp1", scrubberLP1.getGasOutStream())

    # Recycle for liquid from 1st stage scrubber
    pumpLP = pump("pump1", scrubberLP1.getLiquidOutStream())
    pumpLP.setOutletPressure(MPpressure)
    valveR1 = valve("1st scr liq", pumpLP.getOutletStream(), LPpressure)
    recycleLP = recycle("recycleLP")
    recycleLP.addStream(valveR1.getOutletStream())
    recycleLP.setOutletStream(recirc1stream)

    # 2nd stg compressor
    coolerMP1 = heater("ht1", compressorLP1.getOutStream())
    coolerMP1.setOutTemperature(325.15)
    scrubberMP1 = separator("ht11", coolerMP1.getOutStream())
    compressorMP1 = compressor("comp221", scrubberMP1.getGasOutStream())
    compressorMP1.setOutletPressure(MPpressure)
    compressorMP1.setPolytropicEfficiency(0.78)

    # Recycle for liquid from 2nd stage scrubber
    valveR2 = valve("2nd scr liq", scrubberMP1.getLiquidOutStream(), LPpressure)
    recycleMP = recycle("recycleMP")
    recycleMP.addStream(valveR2.getOutletStream())
    recycleMP.setOutletStream(recirc2stream)

    # 3rd stg compressor, compressor model is skipped as the target for reference
    # model is to derive gas composition into 3rd stage and then perform more detailed
    # calculation on 3rd stage compressor
    mixerMP = mixer("mix1")
    mixerMP.addStream(compressorMP1.getOutStream())
    mixerMP.addStream(separator2.getGasOutStream())
    cooler3rd = heater("he1", mixerMP.getOutStream())
    cooler3rd.setOutTemperature(317.15)
    scrubber3rd = separator("ss1", cooler3rd.getOutStream())

    # Recycle for liquid from 2nd stage scrubber
    valveR3 = valve("3re scr liq", scrubber3rd.getLiquidOutStream(), LPpressure)
    recycle3rd = recycle("recycle3rd")
    recycle3rd.addStream(valveR3.getOutStream())
    recycle3rd.setOutletStream(recirc3stream)

    runProcess()

    # assert 3859.9 == approx(recirc1stream.getFlowRate('kg/hr'), abs=1.0)
    # assert 22876.1 ==  approx(pipeloss1st.getOutletStream().getFlowRate("kg/hr"), abs=1.0)
    # assert separator3.getGasOutStream().getFlowRate("kg/hr") == pipeloss1st.getOutletStream().getFlowRate("kg/hr")


def test_AFR():
    fluid = jneqsim.thermo.system.SystemSrkEos((273.15 + 25.0), 10.00)
    fluid.addComponent("nitrogen", 1.0)
    fluid.addComponent("CO2", 1.0)
    fluid.addComponent("methane", 92.0)
    fluid.addComponent("ethane", 5.0)
    fluid.addComponent("propane", 1.0)
    fluid.addComponent("i-butane", 0.5)
    fluid.addComponent("n-butane", 0.5)
    fluid.addComponent("i-pentane", 0.1)
    fluid.addComponent("n-pentane", 0.1)
    fluid.addComponent("n-hexane", 0.01)
    fluid.setMixingRule(2)
    TPflash(fluid)

    elements_h = 0.0
    elements_c = 0.0
    sum_hc = 0.0
    molmass_hc = 0.0
    wtfrac_hc = 0.0

    for i in range(fluid.getNumberOfComponents()):
        if fluid.getComponent(i).isHydrocarbon():
            sum_hc = sum_hc + fluid.getComponent(i).getz()
            molmass_hc = (
                molmass_hc
                + fluid.getComponent(i).getz() * fluid.getComponent(i).getMolarMass()
            )
            elements_c = elements_c + fluid.getComponent(i).getz() * fluid.getComponent(
                i
            ).getElements().getNumberOfElements("C")
            elements_h = elements_h + fluid.getComponent(i).getz() * fluid.getComponent(
                i
            ).getElements().getNumberOfElements("H")

    if sum_hc == 0:
        return 0.0
    else:
        wtfrac_hc = molmass_hc / fluid.getMolarMass()
        molmass_hc /= sum_hc
        elements_c /= sum_hc
        elements_h /= sum_hc

    aconst = elements_c + elements_h / 4
    afr = aconst * (32.0 + 3.76 * 28.0) / 1000.0 / molmass_hc * wtfrac_hc

    assert 16.2312248674 == approx(afr, abs=0.01)
    assert 16.2312248674 == approx(neqsim.standards.air_fuel_ratio(fluid), abs=0.01)
    assert 52691.55 == approx(
        neqsim.standards.ISO6976(fluid, numberunit="mass").getValue(
            "SuperiorCalorificValue"
        ),
        abs=0.01,
    )
