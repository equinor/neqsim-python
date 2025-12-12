# -*- coding: utf-8 -*-
"""
Beggs and Brill Multiphase Pipeline Simulation Example

This example demonstrates the PipeBeggsAndBrills class in NeqSim,
which uses the Beggs and Brill correlation for multiphase flow
in pipelines. This correlation handles:

- Flow pattern prediction (segregated, intermittent, distributed)
- Liquid holdup calculation
- Pressure drop with elevation effects
- Non-isothermal temperature profiles

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create a multiphase fluid (gas with liquid condensate)
multiphase_fluid = fluid("srk")
multiphase_fluid.addComponent("methane", 75.0)
multiphase_fluid.addComponent("ethane", 8.0)
multiphase_fluid.addComponent("propane", 5.0)
multiphase_fluid.addComponent("n-butane", 3.0)
multiphase_fluid.addComponent("n-pentane", 2.0)
multiphase_fluid.addComponent("n-hexane", 2.0)
multiphase_fluid.addComponent("n-heptane", 3.0)
multiphase_fluid.addComponent("n-octane", 2.0)
multiphase_fluid.setMixingRule("classic")
multiphase_fluid.setMultiPhaseCheck(True)
multiphase_fluid.setTemperature(60.0, "C")
multiphase_fluid.setPressure(80.0, "bara")
multiphase_fluid.setTotalFlowRate(100000.0, "kg/hr")

# Create inlet stream
inlet_stream = jneqsim.process.equipment.stream.Stream("Pipeline Inlet", multiphase_fluid)

# Create Beggs and Brill pipeline
# This pipeline goes uphill with significant elevation change
pipe = jneqsim.process.equipment.pipeline.PipeBeggsAndBrills("Multiphase Pipeline", inlet_stream)

# Set pipeline geometry
pipe.setLength(10000.0)  # 10 km length
pipe.setDiameter(0.3)  # 12 inch (0.3 m) diameter
pipe.setPipeWallRoughness(50.0e-6)  # Surface roughness in meters
pipe.setElevation(200.0)  # 200 m elevation gain (uphill)
pipe.setNumberOfIncrements(20)  # Number of calculation segments

# Set thermal parameters (non-isothermal calculation)
pipe.setRunIsothermal(False)

# Create process and run
process = jneqsim.process.processmodel.ProcessSystem()
process.add(inlet_stream)
process.add(pipe)
process.run()

# Get results
outlet_stream = pipe.getOutletStream()
outlet_pressure = outlet_stream.getPressure("bara")
outlet_temp = outlet_stream.getTemperature("C")
pressure_drop = inlet_stream.getPressure("bara") - outlet_pressure

print("=" * 65)
print("BEGGS AND BRILL MULTIPHASE PIPELINE SIMULATION")
print("=" * 65)

print("\nPipeline Geometry:")
print(f"  Length:          10,000 m (10 km)")
print(f"  Diameter:        0.30 m (12 inch)")
print(f"  Wall roughness:  50 μm")
print(f"  Elevation gain:  200 m (uphill)")

print("\nInlet Conditions:")
print(f"  Pressure:        {inlet_stream.getPressure('bara'):.1f} bara")
print(f"  Temperature:     {inlet_stream.getTemperature('C'):.1f} °C")
print(f"  Mass flow:       {inlet_stream.getFlowRate('kg/hr'):.0f} kg/hr")

print("\nOutlet Conditions:")
print(f"  Pressure:        {outlet_pressure:.2f} bara")
print(f"  Temperature:     {outlet_temp:.1f} °C")

print("\nPipeline Performance:")
print(f"  Pressure drop:   {pressure_drop:.2f} bar")
print(f"  ΔP per km:       {pressure_drop / 10:.2f} bar/km")
print(f"  Temp change:     {outlet_temp - inlet_stream.getTemperature('C'):.1f} °C")

# Get flow information from outlet stream
outlet_fluid = outlet_stream.getFluid()
if outlet_fluid.hasPhaseType("gas") and outlet_fluid.hasPhaseType("oil"):
    gas_fraction = outlet_fluid.getPhase("gas").getBeta()
    liquid_fraction = 1.0 - gas_fraction
    print(f"\nPhase Distribution at Outlet:")
    print(f"  Gas fraction:    {gas_fraction * 100:.1f}%")
    print(f"  Liquid fraction: {liquid_fraction * 100:.1f}%")

print("=" * 65)
