from neqsim import jNeqSim


def test_dynamic_compressor():
    testSystem2 = jNeqSim.thermo.system.SystemSrkEos((273.15 + 25.0), 10.00)
    testSystem2.addComponent("methane", 1.1)
    testSystem2.addComponent("ethane", 0.1)
    testSystem2.setMixingRule(2)

    stream1 = jNeqSim.processSimulation.processEquipment.stream.Stream(
        "Stream1", testSystem2
    )
    stream1.setFlowRate(5000.0, "kg/hr")
    stream1.setPressure(100.0, "bara")
    stream1.setTemperature(55.0, "C")

    valve1 = jNeqSim.processSimulation.processEquipment.valve.ThrottlingValve(
        "valve_1", stream1
    )
    valve1.setOutletPressure(50.0)
    valve1.setPercentValveOpening(50)
    valve1.setCalculateSteadyState(False)

    separator1 = jNeqSim.processSimulation.processEquipment.separator.Separator(
        "separator_1"
    )
    separator1.addStream(valve1.getOutletStream())
    separator1.setCalculateSteadyState(False)
    separator1.setSeparatorLength(3.0)
    separator1.setInternalDiameter(0.8)
    separator1.setLiquidLevel(0.0)

    compressor1 = jNeqSim.processSimulation.processEquipment.compressor.Compressor(
        "comp1", separator1.getGasOutStream()
    )
    compressor1.setCalculateSteadyState(False)
    compressor1.setOutletPressure(100.0)

    separator2 = jNeqSim.processSimulation.processEquipment.separator.Separator(
        "separator_2"
    )
    separator2.addStream(compressor1.getOutletStream())
    separator2.setCalculateSteadyState(False)
    separator2.setSeparatorLength(3.0)
    separator2.setInternalDiameter(0.8)
    separator2.setLiquidLevel(0.0)

    valve2 = jNeqSim.processSimulation.processEquipment.valve.ThrottlingValve(
        "valve_2", separator2.getGasOutStream()
    )
    valve2.setOutletPressure(50.0)
    valve2.setPercentValveOpening(50)
    valve2.setCalculateSteadyState(False)

    p = jNeqSim.processSimulation.processSystem.ProcessSystem()
    p.add(stream1)
    p.add(valve1)
    p.add(separator1)
    p.add(compressor1)
    p.add(separator2)
    p.add(valve2)

    p.run()
    compchartgenerator = (
        jNeqSim.processSimulation.processEquipment.compressor.CompressorChartGenerator(
            compressor1
        )
    )
    compressor1.setCompressorChart(compchartgenerator.generateCompressorChart("normal"))
    compressor1.getCompressorChart().setUseCompressorChart(True)
    p.run()

    time = []
    pressuresep1 = []
    pressuresep2 = []
    flow = []
    head = []

    p.setTimeStep(1.0)
    for i in range(100):
        time.append(p.getTime())
        pressuresep1.append(separator1.getPressure())
        pressuresep2.append(separator2.getPressure())
        flow.append(compressor1.getInletStream().getFlowRate("m3/hr"))
        head.append(compressor1.getPolytropicFluidHead())
        p.runTransient()

    # increaseing compressor speed
    compressor1.setSpeed(compressor1.getSpeed() + 200)
    for i in range(500):
        time.append(p.getTime())
        pressuresep1.append(separator1.getPressure())
        pressuresep2.append(separator2.getPressure())
        flow.append(compressor1.getInletStream().getFlowRate("m3/hr"))
        head.append(compressor1.getPolytropicFluidHead())
        p.runTransient()
