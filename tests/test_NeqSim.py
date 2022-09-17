# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 22:24:08 2019

@author: ESOL
"""
from neqsim.neqsimpython import jNeqSim


def test_Viscosity():
    thermoSystem = jNeqSim.thermo.system.SystemSrkEos(280.0, 10.0)
    thermoSystem.addComponent("methane", 10.0)
    thermoSystem.addComponent("water", 4.0)

    thermoOps = jNeqSim.thermodynamicOperations.ThermodynamicOperations(
        thermoSystem)
    thermoOps.TPflash()

    gasEnthalpy = thermoSystem.getPhase(0).getEnthalpy()
    assert abs(1079.4821290144278 - gasEnthalpy) < 1e-10

    thermoSystem.initPhysicalProperties("Viscosity")
    gasViscosity = thermoSystem.getPhase(0).getViscosity("kg/msec")
    assert abs(1.0760998263783299e-05 - gasViscosity) < 1e-10

def test_fullOffshoreProcess():
    import pandas as pd
    import math

    #well stream composition (mole fractions)
    reservoirFluid = {'ComponentName':  ['nitrogen', 'CO2', 'methane', 'ethane', 'propane', 'i-butane', 'n-butane', 'i-pentane', 'n-pentane', 'n-hexane','n-heptane', 'n-octane', 'n-nonane', 'nC10'], 
            'MolarComposition[-]':  [0.56, 1.02, 80.77, 7.77, 3.91, 0.56, 0.9, 0.25, 0.24, 0.5, 0.3, 0.2, 0.12, 0.91]
    }
    reservoirFluiddf = pd.DataFrame(reservoirFluid) #create a dataframe of the well fluid

    well_head_pressure = 180.0 #bara
    well_head_temperature = 80.0 #degC
    platform_inlet_pressure = 90.0 #bara
    platform_inlet_temperature = 5.0 #C
    platform_outlet_pressure = 200.0 #bara
    platform_outlet_temperature = 15.0 #C
    karsto_inlet_pressure = 110.0 #bara
    karsto_inlet_temperature = 110.0 #bara
    well_flow_rate = 20.0 #GSm3/year
    pipeline_length = 690.0 #km
    sea_water_temperature = 5.0 #C
    rich_gas_water_dew_point = -10.0 #degC
    rich_gas_cricondenbar = 90.0 #bara

    from neqsim.thermo import fluid_df
    from neqsim.process import stream,saturator,clearProcess, runProcess, cooler

    clearProcess() #reset process simulation

    reservoirFluid = fluid_df(reservoirFluiddf, modelName='pr') #create a neqsim fluid from the reservoir fluid dataframe
    reservoirFluid.setMultiPhaseCheck(True) #use multiphase flash in neqsim

    wellStream = stream(reservoirFluid) # create a neqsim stream from the reservoir fluid 
    wellStream.setTemperature(well_head_temperature, 'C')
    wellStream.setPressure(well_head_pressure, 'bara')
    wellStream.setFlowRate(well_flow_rate*1000.0/365.0, 'MSm3/day') #convert flow to MSm3/day

    #saturate the well stream with water
    waterSaturator = saturator(wellStream)

    #Simulating the pipeline using a cooler
    wellFlowLine = cooler(waterSaturator.getOutStream())
    wellFlowLine.setOutTemperature(platform_inlet_temperature, 'C')
    wellFlowLine.setOutPressure(platform_inlet_pressure, 'bara')

    wellStreamEnteringPlatform = wellFlowLine.getOutStream()

    runProcess() #run the process simulation

    inputdata = {
        'firstStagePressure': 78.0, 
        'temperatureOilHeater' : 75.9,
        'secondStagePressure': 8.6,
        'thirdStagePressure': 1.3,
        'firstStageSuctionCoolerTemperature': 25.0, 
        'secondStageSuctionCoolerTemperature': 25.0, 
        'thirdStageSuctionCoolerTemperature':25.0,
        'dewPointScrubberTemperature': 25.0,
        'firstStageExportCoolerTemperature': 25.0, 
        'secondStageExportCoolerTemperature': 25.0
        }
        
    from neqsim.process import (compressor, cooler, separator3phase, 
    getProcess, clearProcess, mixer, heater, stream, pump, separator, 
    runProcess, stream, saturator, valve, filters, heatExchanger, simpleTEGAbsorber,
    distillationColumn, waterStripperColumn, recycle2, setpoint, calculator)

    clearProcess() #reset process simulation

    chokeValve = valve(wellFlowLine.getOutStream())
    chokeValve.setOutletPressure(inputdata['firstStagePressure'], 'bara')

    feedToOffshoreProcess = stream(chokeValve.getOutStream())
    feedToOffshoreProcess.setName("feed to offshore")

    firstStageSeparator = separator3phase(feedToOffshoreProcess)
    firstStageSeparator.setName("1st stage separator")

    oilHeaterFromFirstStage = heater(firstStageSeparator.getOilOutStream())
    oilHeaterFromFirstStage.setName("oil heater second stage")
    oilHeaterFromFirstStage.setOutTemperature(inputdata['temperatureOilHeater'],'C')

    oilThrotValve = valve(oilHeaterFromFirstStage.getOutStream())
    oilThrotValve.setName("valve oil from first stage")
    oilThrotValve.setOutletPressure(inputdata['secondStagePressure'])

    secondStageSeparator = separator3phase(oilThrotValve.getOutStream())
    secondStageSeparator.setName("2nd stage separator")

    oilThrotValve2 = valve(secondStageSeparator.getOilOutStream())
    oilThrotValve2.setName("valve oil from second stage")
    oilThrotValve2.setOutletPressure(inputdata['thirdStagePressure'])

    thirdStageSeparator = separator3phase(oilThrotValve2.getOutStream())
    thirdStageSeparator.setName("3rd stage separator")

    oilThirdStageToSep =  wellStream.clone()
    oilThirdStageToSep.setName("resyc oil")
    thirdStageSeparator.addStream(oilThirdStageToSep)

    stableOil = stream(thirdStageSeparator.getOilOutStream())
    stableOil.setName("stable oil")

    stableOilPump = pump(stableOil,15.0,"stable oil pump")

    firstStageCooler = cooler(thirdStageSeparator.getGasOutStream())
    firstStageCooler.setName("1st stage cooler")
    firstStageCooler.setOutTemperature(inputdata['firstStageSuctionCoolerTemperature'],'C')

    firstStageScrubber = separator(firstStageCooler.getOutStream())
    firstStageScrubber.setName("1st stage scrubber")

    firstStageCompressor = compressor(firstStageScrubber.getGasOutStream())
    firstStageCompressor.setName("1st stage compressor")
    firstStageCompressor.setOutletPressure(inputdata['secondStagePressure'])
    firstStageCompressor.setIsentropicEfficiency(0.75)

    secondStageCooler = cooler(firstStageCompressor.getOutStream())
    secondStageCooler.setName("2nd stage cooler")
    secondStageCooler.setOutTemperature(inputdata['secondStageSuctionCoolerTemperature'],'C')

    secondStageScrubber = separator(secondStageCooler.getOutStream())
    secondStageScrubber.setName("2nd stage scrubber")

    secondStageCompressor = compressor(secondStageScrubber.getGasOutStream())
    secondStageCompressor.setName("2nd stage compressor")
    secondStageCompressor.setOutletPressure(inputdata['firstStagePressure'])
    secondStageCompressor.setIsentropicEfficiency(0.75)

    richGasMixer = mixer("fourth Stage mixer")
    richGasMixer.addStream(secondStageCompressor.getOutStream())
    richGasMixer.addStream(firstStageSeparator.getGasOutStream())

    dewPointControlCooler = cooler(richGasMixer.getOutStream())
    dewPointControlCooler.setName("dew point cooler")
    dewPointControlCooler.setOutTemperature(inputdata['dewPointScrubberTemperature'],'C')

    dewPointScrubber = separator(dewPointControlCooler.getOutStream())
    dewPointScrubber.setName("dew point scrubber")

    lpLiqmixer = mixer("LP liq gas mixer");
    lpLiqmixer.addStream(firstStageScrubber.getLiquidOutStream());
    lpLiqmixer.addStream(secondStageScrubber.getLiquidOutStream());
    lpLiqmixer.addStream(dewPointScrubber.getLiquidOutStream());

    lpResycle = recycle2("LP liq resycle")
    lpResycle.addStream(lpLiqmixer.getOutStream())
    lpResycle.setOutletStream(oilThirdStageToSep)

    exportCompressor1 = compressor(dewPointScrubber.getGasOutStream())
    exportCompressor1.setName("export 1st stage")
    exportCompressor1.setOutletPressure(130.0)
    exportCompressor1.setIsentropicEfficiency(0.75)

    exportInterstageCooler = cooler(exportCompressor1.getOutStream())
    exportInterstageCooler.setName("interstage stage cooler")
    exportInterstageCooler.setOutTemperature(inputdata['firstStageExportCoolerTemperature'],'C')

    exportCompressor2= compressor(exportInterstageCooler.getOutStream())
    exportCompressor2.setName("export 2nd stage")
    exportCompressor2.setOutletPressure(200.0)
    exportCompressor2.setIsentropicEfficiency(0.75)

    exportCooler = cooler(exportCompressor2.getOutStream())
    exportCooler.setName("export cooler")
    exportCooler.setOutTemperature(inputdata['secondStageExportCoolerTemperature'],'C')

    exportGas = stream(exportCooler.getOutStream())
    exportGas.setName("export gas")

    runProcess() #run the process simulation

    #NGL expander code
    from neqsim.process import expander, heater, compsplitter, separator

    pressureNGL = 60.0

    clearProcess()

    inletValve = valve(exportGas)
    inletValve.setPressure(110.0, 'bara')

    splitFactors = [1.0]*exportGas.getFluid().getNumberOfComponents()
    splitFactors[-1]=0.0

    watersplitter = compsplitter(inletValve.getOutStream(), splitFactors)

    coolerInlet = cooler(watersplitter.getSplitStream(0))
    coolerInlet.setOutTemperature(-20.0, 'C')

    expanderKarsto = expander(coolerInlet.getOutStream(), pressureNGL)

    scrubberNGL = separator(expanderKarsto.getOutStream())

    gasHeater = heater(scrubberNGL.getGasOutStream())
    gasHeater.setOutTemperature(20.0)

    exportCompressor = compressor(gasHeater.getOutStream())
    exportCompressor.setOutletPressure(200.0, 'bara')
    exportGas = stream(exportCompressor.getOutStream())
    runProcess()
