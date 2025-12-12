# -*- coding: utf-8 -*-
"""
Ejector Process Simulation Example

This example demonstrates using an ejector (steam/gas jet) in NeqSim.
Ejectors are used in vacuum systems, refrigeration cycles, and 
for mixing/boosting low-pressure gas with a high-pressure motive stream.

The ejector calculation uses a quasi one-dimensional formulation combining
energy and momentum balances as described in Keenan et al. (1950) and ESDU 86030.

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create the motive (high-pressure driving) fluid
motive_fluid = fluid("srk")
motive_fluid.addComponent("methane", 90.0)
motive_fluid.addComponent("ethane", 7.0)
motive_fluid.addComponent("propane", 3.0)
motive_fluid.setMixingRule("classic")
motive_fluid.setTemperature(40.0, "C")
motive_fluid.setPressure(50.0, "bara")
motive_fluid.setTotalFlowRate(5000.0, "kg/hr")

# Create the suction (low-pressure) fluid
suction_fluid = fluid("srk")
suction_fluid.addComponent("methane", 85.0)
suction_fluid.addComponent("ethane", 10.0)
suction_fluid.addComponent("propane", 5.0)
suction_fluid.setMixingRule("classic")
suction_fluid.setTemperature(25.0, "C")
suction_fluid.setPressure(5.0, "bara")
suction_fluid.setTotalFlowRate(2000.0, "kg/hr")

# Create streams
motive_stream = jneqsim.process.equipment.stream.Stream("Motive Stream", motive_fluid)
suction_stream = jneqsim.process.equipment.stream.Stream("Suction Stream", suction_fluid)

# Create ejector
ejector = jneqsim.process.equipment.ejector.Ejector("Gas Ejector", motive_stream, suction_stream)

# Create process system and run
process = jneqsim.process.processmodel.ProcessSystem()
process.add(motive_stream)
process.add(suction_stream)
process.add(ejector)

process.run()

# Get results
outlet_stream = ejector.getOutletStream()
outlet_pressure = outlet_stream.getPressure("bara")
outlet_temperature = outlet_stream.getTemperature("C")
outlet_flow = outlet_stream.getFlowRate("kg/hr")

print("=" * 60)
print("EJECTOR SIMULATION RESULTS")
print("=" * 60)
print(f"\nMotive Stream:")
print(f"  Pressure:    {motive_stream.getPressure('bara'):.1f} bara")
print(f"  Temperature: {motive_stream.getTemperature('C'):.1f} °C")
print(f"  Flow rate:   {motive_stream.getFlowRate('kg/hr'):.0f} kg/hr")

print(f"\nSuction Stream:")
print(f"  Pressure:    {suction_stream.getPressure('bara'):.1f} bara")
print(f"  Temperature: {suction_stream.getTemperature('C'):.1f} °C")
print(f"  Flow rate:   {suction_stream.getFlowRate('kg/hr'):.0f} kg/hr")

print(f"\nMixed Outlet Stream:")
print(f"  Pressure:    {outlet_pressure:.2f} bara")
print(f"  Temperature: {outlet_temperature:.1f} °C")
print(f"  Flow rate:   {outlet_flow:.0f} kg/hr")

# Get entrainment ratio (mass of suction per mass of motive)
entrainment_ratio = suction_fluid.getFlowRate("kg/hr") / motive_fluid.getFlowRate("kg/hr")
print(f"\nEntrainment Ratio: {entrainment_ratio:.3f}")
print(f"Compression Ratio: {outlet_pressure / suction_stream.getPressure('bara'):.2f}")
print("=" * 60)
