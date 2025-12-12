# -*- coding: utf-8 -*-
"""
Mechanical Design Calculation Example

This example demonstrates the mechanical design calculation features
in NeqSim. Mechanical design includes:

- Pressure vessel sizing based on design codes
- Wall thickness calculation
- Material selection considerations
- Design pressure/temperature margins

These calculations follow industry standards like ASME.

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create a process fluid
process_fluid = fluid("srk")
process_fluid.addComponent("methane", 85.0)
process_fluid.addComponent("ethane", 10.0)
process_fluid.addComponent("propane", 5.0)
process_fluid.setMixingRule("classic")
process_fluid.setTemperature(60.0, "C")
process_fluid.setPressure(50.0, "bara")
process_fluid.setTotalFlowRate(100000.0, "kg/hr")

# Create feed stream
feed_stream = jneqsim.process.equipment.stream.Stream("Feed", process_fluid)

# Create separator
separator = jneqsim.process.equipment.separator.Separator("HP Separator", feed_stream)
separator.setInternalDiameter(2.0)  # 2 m diameter
separator.setSeparatorLength(5.0)  # 5 m length

# Create process and run to establish operating conditions
process = jneqsim.process.processmodel.ProcessSystem()
process.add(feed_stream)
process.add(separator)
process.run()

print("=" * 65)
print("MECHANICAL DESIGN CALCULATIONS")
print("=" * 65)

print("\nOperating Conditions:")
print(f"  Operating pressure:    {separator.getPressure():.1f} bara")
print(f"  Operating temperature: {feed_stream.getTemperature('C'):.1f} °C")

# Initialize and run mechanical design calculations
separator.initMechanicalDesign()
mech_design = separator.getMechanicalDesign()

# Set design conditions (typically with safety margins)
operating_pressure = separator.getPressure()
operating_temp = feed_stream.getTemperature("C")

# Design pressure = operating + 10% or operating + 3.5 bar (whichever is greater)
design_pressure = max(operating_pressure * 1.1, operating_pressure + 3.5)
# Design temperature = operating + 25°C margin
design_temp = operating_temp + 25.0

mech_design.setMaxOperationPressure(operating_pressure)
mech_design.setMaxOperationTemperature(operating_temp + 273.15)  # Convert to Kelvin
mech_design.setMaxDesignPressure(design_pressure)

print("\nDesign Conditions:")
print(f"  Design pressure:       {design_pressure:.1f} bara")
print(f"  Design temperature:    {design_temp:.1f} °C")

# Set design capacity (gas volume flow)
mech_design.setMaxDesignGassVolumeFlow(500.0)  # m3/hr

# Run design calculation
mech_design.calcDesign()

print("\nSeparator Geometry:")
print(f"  Internal diameter:     2.0 m")
print(f"  Tangent length:        5.0 m")

# Display results if available
print("\nMechanical Design Parameters:")
print(f"  Max design gas flow:   500.0 m³/hr")

# Get capacity utilization
gas_stream = separator.getGasOutStream()
actual_gas_flow = gas_stream.getFlowRate("m3/hr")
print(f"  Actual gas flow:       {actual_gas_flow:.1f} m³/hr")

capacity_utilization = (actual_gas_flow / 500.0) * 100.0
print(f"  Capacity utilization:  {capacity_utilization:.1f}%")

if capacity_utilization > 100:
    print(f"  ⚠️  WARNING: Separator is OVER capacity!")
elif capacity_utilization > 80:
    print(f"  ⚠️  Note: Operating above 80% design capacity")
else:
    print(f"  ✓ Operating within design limits")

# Pipeline mechanical design example
print("\n" + "-" * 65)
print("Pipeline Mechanical Design")
print("-" * 65)

# Create pipeline
pipeline = jneqsim.process.equipment.pipeline.Pipeline("Export Pipeline", feed_stream)
pipeline.setLength(50000.0)  # 50 km
pipeline.setDiameter(0.5)  # 20 inch

# Initialize pipeline mechanical design
pipeline.initMechanicalDesign()
pipe_design = pipeline.getMechanicalDesign()

# Set design limits
pipe_design.setMaxOperationPressure(operating_pressure)
pipe_design.setMinOperationPressure(10.0)  # Minimum arrival pressure

print("\nPipeline Parameters:")
print(f"  Length:               50 km")
print(f"  Diameter:             0.5 m (20 inch)")
print(f"  Max operating P:      {operating_pressure:.1f} bara")
print(f"  Min operating P:      10.0 bara")

print("=" * 65)
