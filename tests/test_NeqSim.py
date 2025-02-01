# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 22:24:08 2019

@author: ESOL
"""
import os
from neqsim.neqsimpython import jneqsim
import pandas as pd


import pytest

def test_DsibleFaultHandeler():
    try:
        import faulthandler
        # Enable then disable to relinquish control of error handlers
        faulthandler.enable()
        faulthandler.disable()
    except Exception:
        pass

def test_Viscosity():
    thermoSystem = jneqsim.thermo.system.SystemSrkEos(280.0, 10.0)
    thermoSystem.addComponent("methane", 10.0)
    thermoSystem.addComponent("water", 4.0)

    thermoOps = jneqsim.thermodynamicoperations.ThermodynamicOperations(thermoSystem)
    thermoOps.TPflash()

    gasEnthalpy = thermoSystem.getPhase(0).getEnthalpy()
    assert abs(1079.8561270889081 - gasEnthalpy) < 1e-10

    thermoSystem.initPhysicalProperties("Viscosity")
    gasViscosity = thermoSystem.getPhase(0).getViscosity("kg/msec")
    assert abs(1.0760998263782569e-05 - gasViscosity) < 1e-10


# def test_updateDatabase():
#    jneqsim.util.database.NeqSimDataBase.updateTable("COMP",
#        "classpath:/data/COMP.csv")


def test_hasComponentDatabase():
    assert jneqsim.util.database.NeqSimDataBase.hasComponent("methane") is True


def test_fullOffshoreProcess():
    # well stream composition (mole fractions)
    reservoirFluid = {
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
            "n-heptane",
            "n-octane",
            "n-nonane",
            "nC10",
        ],
        "MolarComposition[-]": [
            0.56,
            1.02,
            80.77,
            7.77,
            3.91,
            0.56,
            0.9,
            0.25,
            0.24,
            0.5,
            0.3,
            0.2,
            0.12,
            0.91,
        ],
    }
    reservoirFluiddf = pd.DataFrame(
        reservoirFluid
    )  # create a dataframe of the well fluid

    well_head_pressure = 180.0  # bara
    well_head_temperature = 80.0  # degC
    platform_inlet_pressure = 90.0  # bara
    platform_inlet_temperature = 5.0  # C
    platform_outlet_pressure = 200.0  # bara
    platform_outlet_temperature = 15.0  # C
    karsto_inlet_pressure = 110.0  # bara
    karsto_inlet_temperature = 110.0  # bara
    well_flow_rate = 20.0  # GSm3/year
    pipeline_length = 690.0  # km
    sea_water_temperature = 5.0  # C
    rich_gas_water_dew_point = -10.0  # degC
    rich_gas_cricondenbar = 90.0  # bara

    from neqsim.thermo import fluid_df
    from neqsim.process import stream, saturator, clearProcess, runProcess, cooler

    clearProcess()  # reset process simulation

    reservoirFluid = fluid_df(
        reservoirFluiddf, modelName="pr"
    )  # create a neqsim fluid from the reservoir fluid dataframe
    reservoirFluid.setMultiPhaseCheck(True)  # use multiphase flash in neqsim

    wellStream = stream(
        "stream 1", reservoirFluid
    )  # create a neqsim stream from the reservoir fluid
    wellStream.setTemperature(well_head_temperature, "C")
    wellStream.setPressure(well_head_pressure, "bara")
    wellStream.setFlowRate(
        well_flow_rate * 1000.0 / 365.0, "MSm3/day"
    )  # convert flow to MSm3/day

    # saturate the well stream with water
    waterSaturator = saturator("saturator 1", wellStream)

    # Simulating the pipeline using a cooler
    wellFlowLine = cooler(" cooler 1", waterSaturator.getOutStream())
    wellFlowLine.setOutTemperature(platform_inlet_temperature, "C")
    wellFlowLine.setOutPressure(platform_inlet_pressure, "bara")

    wellStreamEnteringPlatform = wellFlowLine.getOutStream()

    runProcess()  # run the process simulation

    inputdata = {
        "firstStagePressure": 78.0,
        "temperatureOilHeater": 75.9,
        "secondStagePressure": 8.6,
        "thirdStagePressure": 1.3,
        "firstStageSuctionCoolerTemperature": 25.0,
        "secondStageSuctionCoolerTemperature": 25.0,
        "thirdStageSuctionCoolerTemperature": 25.0,
        "dewPointScrubberTemperature": 25.0,
        "firstStageExportCoolerTemperature": 25.0,
        "secondStageExportCoolerTemperature": 25.0,
    }

    from neqsim.process import (
        compressor,
        cooler,
        separator3phase,
        clearProcess,
        mixer,
        heater,
        stream,
        pump,
        separator,
        runProcess,
        stream,
        saturator,
        valve,
        recycle,
    )

    clearProcess()  # reset process simulation

    chokeValve = valve("valve 1", wellFlowLine.getOutStream())
    chokeValve.setOutletPressure(inputdata["firstStagePressure"], "bara")

    feedToOffshoreProcess = stream("stream 2", chokeValve.getOutStream())
    feedToOffshoreProcess.setName("feed to offshore")

    firstStageSeparator = separator3phase("sep2", feedToOffshoreProcess)
    firstStageSeparator.setName("1st stage separator")

    oilHeaterFromFirstStage = heater("heatr", firstStageSeparator.getOilOutStream())
    oilHeaterFromFirstStage.setName("oil heater second stage")
    oilHeaterFromFirstStage.setOutTemperature(inputdata["temperatureOilHeater"], "C")

    oilThrotValve = valve("valvee", oilHeaterFromFirstStage.getOutStream())
    oilThrotValve.setOutletPressure(inputdata["secondStagePressure"])

    secondStageSeparator = separator3phase("seppp", oilThrotValve.getOutStream())
    secondStageSeparator.setName("2nd stage separator")

    oilThrotValve2 = valve("valve5", secondStageSeparator.getOilOutStream())
    oilThrotValve2.setOutletPressure(inputdata["thirdStagePressure"])

    thirdStageSeparator = separator3phase("sep55", oilThrotValve2.getOutStream())
    thirdStageSeparator.setName("3rd stage separator")

    oilThirdStageToSep = wellStream.clone()
    oilThirdStageToSep.setName("resyc oil")
    thirdStageSeparator.addStream(oilThirdStageToSep)

    stableOil = stream("stable oil", thirdStageSeparator.getOilOutStream())

    stableOilPump = pump("stable oil pump", stableOil, 15.0)

    firstStageCooler = cooler("1st stage cooler", thirdStageSeparator.getGasOutStream())
    firstStageCooler.setOutTemperature(
        inputdata["firstStageSuctionCoolerTemperature"], "C"
    )

    firstStageScrubber = separator(
        "1st stage compressor", firstStageCooler.getOutStream()
    )

    firstStageCompressor = compressor(
        '"1st stage compressor"', firstStageScrubber.getGasOutStream()
    )
    firstStageCompressor.setOutletPressure(inputdata["secondStagePressure"])
    firstStageCompressor.setIsentropicEfficiency(0.75)

    secondStageCooler = cooler("cooler44", firstStageCompressor.getOutStream())
    secondStageCooler.setName("2nd stage cooler")
    secondStageCooler.setOutTemperature(
        inputdata["secondStageSuctionCoolerTemperature"], "C"
    )

    secondStageScrubber = separator(
        '"2nd stage scrubber', secondStageCooler.getOutStream()
    )

    secondStageCompressor = compressor(
        "2nd stage compressor", secondStageScrubber.getGasOutStream()
    )
    secondStageCompressor.setOutletPressure(inputdata["firstStagePressure"])
    secondStageCompressor.setIsentropicEfficiency(0.75)

    richGasMixer = mixer("fourth Stage mixer")
    richGasMixer.addStream(secondStageCompressor.getOutStream())
    richGasMixer.addStream(firstStageSeparator.getGasOutStream())

    dewPointControlCooler = cooler("dew point cooler", richGasMixer.getOutStream())
    dewPointControlCooler.setOutTemperature(
        inputdata["dewPointScrubberTemperature"], "C"
    )

    dewPointScrubber = separator(
        "dew point scrubber", dewPointControlCooler.getOutStream()
    )

    lpLiqmixer = mixer("LP liq gas mixer")
    lpLiqmixer.addStream(firstStageScrubber.getLiquidOutStream())
    lpLiqmixer.addStream(secondStageScrubber.getLiquidOutStream())
    lpLiqmixer.addStream(dewPointScrubber.getLiquidOutStream())

    lpResycle = recycle("LP liq resycle")
    lpResycle.addStream(lpLiqmixer.getOutStream())
    lpResycle.setOutletStream(oilThirdStageToSep)

    exportCompressor1 = compressor(
        "export 1st stage", dewPointScrubber.getGasOutStream()
    )
    exportCompressor1.setOutletPressure(130.0)
    exportCompressor1.setIsentropicEfficiency(0.75)

    exportInterstageCooler = cooler(
        "interstage stage cooler", exportCompressor1.getOutStream()
    )
    exportInterstageCooler.setOutTemperature(
        inputdata["firstStageExportCoolerTemperature"], "C"
    )

    exportCompressor2 = compressor(
        "export 2nd stage", exportInterstageCooler.getOutStream()
    )
    exportCompressor2.setOutletPressure(200.0)
    exportCompressor2.setIsentropicEfficiency(0.75)

    exportCooler = cooler("export cooler", exportCompressor2.getOutStream())
    exportCooler.setOutTemperature(inputdata["secondStageExportCoolerTemperature"], "C")

    exportGas = stream("export str", exportCooler.getOutStream())

    runProcess()  # run the process simulation

    # NGL expander code
    from neqsim.process import expander, heater, compsplitter, separator

    pressureNGL = 60.0

    clearProcess()

    inletValve = valve("valvvv", exportGas)
    inletValve.setPressure(110.0, "bara")

    splitFactors = [1.0] * exportGas.getFluid().getNumberOfComponents()
    splitFactors[-1] = 0.0

    watersplitter = compsplitter("comspl", inletValve.getOutStream(), splitFactors)

    coolerInlet = cooler("ccccool", watersplitter.getSplitStream(0))
    coolerInlet.setOutTemperature(-20.0, "C")

    expanderKarsto = expander("exp", coolerInlet.getOutStream(), pressureNGL)

    scrubberNGL = separator("sep3", expanderKarsto.getOutStream())

    gasHeater = heater("heaterrr", scrubberNGL.getGasOutStream())
    gasHeater.setOutTemperature(20.0)

    exportCompressor = compressor("comppp", gasHeater.getOutStream())
    exportCompressor.setOutletPressure(200.0, "bara")
    exportGas = stream("ssstre", exportCompressor.getOutStream())
    runProcess()


def testwriteandopen(tmp_path):
    import neqsim
    from neqsim.thermo import createfluid

    temp_dir = tmp_path / "test"
    os.mkdir(temp_dir)

    temp_file = temp_dir / "name.xml"

    fluid1 = createfluid("dry gas")
    neqsim.save_xml(fluid1, temp_file)
    fluid2 = neqsim.open_xml(temp_file)

    assert fluid1.getTemperature() == fluid2.getTemperature()
