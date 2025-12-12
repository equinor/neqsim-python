# -*- coding: utf-8 -*-
"""
Transient Separator Simulation Example

This example demonstrates transient (dynamic) simulation of a 
separator in NeqSim. Transient simulation tracks how equipment
responds over time to changing conditions.

Features demonstrated:
- Setting up a separator for transient operation
- Running time-stepped simulation
- Tracking pressure and level changes
- Simulating feed rate changes

@author: NeqSim Team
"""

import uuid
from neqsim import jneqsim
from neqsim.thermo import fluid

# Create feed fluid
feed_fluid = fluid("srk")
feed_fluid.addComponent("methane", 70.0)
feed_fluid.addComponent("ethane", 10.0)
feed_fluid.addComponent("propane", 5.0)
feed_fluid.addComponent("n-butane", 3.0)
feed_fluid.addComponent("n-pentane", 2.0)
feed_fluid.addComponent("n-hexane", 5.0)
feed_fluid.addComponent("n-heptane", 5.0)
feed_fluid.setMixingRule("classic")
feed_fluid.setMultiPhaseCheck(True)
feed_fluid.setTemperature(60.0, "C")
feed_fluid.setPressure(40.0, "bara")
feed_fluid.setTotalFlowRate(50000.0, "kg/hr")

# Create feed stream
feed_stream = jneqsim.process.equipment.stream.Stream("Feed Stream", feed_fluid)

# Create separator with internal diameter and length for volume calculation
separator = jneqsim.process.equipment.separator.Separator("HP Separator", feed_stream)
separator.setInternalDiameter(2.5)  # 2.5 m diameter
separator.setSeparatorLength(6.0)  # 6 m length

# Get outlet streams
gas_outlet = jneqsim.process.equipment.stream.Stream(
    "Gas Outlet", separator.getGasOutStream()
)
liquid_outlet = jneqsim.process.equipment.stream.Stream(
    "Liquid Outlet", separator.getLiquidOutStream()
)

# Create process
process = jneqsim.process.processmodel.ProcessSystem()
process.add(feed_stream)
process.add(separator)
process.add(gas_outlet)
process.add(liquid_outlet)

# Run initial steady-state
process.run()

print("=" * 70)
print("TRANSIENT SEPARATOR SIMULATION")
print("=" * 70)

print("\nSeparator Configuration:")
print(f"  Internal diameter: 2.5 m")
print(f"  Length:            6.0 m")

print("\nInitial Steady-State Conditions:")
print(f"  Feed rate:      {feed_stream.getFlowRate('kg/hr'):.0f} kg/hr")
print(f"  Pressure:       {separator.getPressure():.1f} bara")
print(f"  Gas outlet:     {gas_outlet.getFlowRate('kg/hr'):.0f} kg/hr")
print(f"  Liquid outlet:  {liquid_outlet.getFlowRate('kg/hr'):.0f} kg/hr")

# Run transient simulation
print("\n" + "-" * 70)
print("Running transient simulation with feed rate step change...")
print("-" * 70)

time_step = 10.0  # seconds
simulation_time = 120.0  # total seconds

print(f"\nTime (s) | Pressure (bara) | Gas Flow (kg/hr) | Liquid Flow (kg/hr)")
print("-" * 70)

time = 0.0
while time <= simulation_time:
    # At t=30s, increase feed rate by 20%
    if time == 30.0:
        feed_fluid.setTotalFlowRate(60000.0, "kg/hr")  # 20% increase
        feed_stream.setFluid(feed_fluid)
        print(f">>> Feed rate increased to 60,000 kg/hr at t={time:.0f}s <<<")
    
    # At t=90s, decrease feed rate back to original
    if time == 90.0:
        feed_fluid.setTotalFlowRate(50000.0, "kg/hr")  # Back to original
        feed_stream.setFluid(feed_fluid)
        print(f">>> Feed rate decreased to 50,000 kg/hr at t={time:.0f}s <<<")
    
    # Run feed stream
    feed_stream.run()
    
    # Run separator transient step
    run_id = uuid.uuid4()
    separator.runTransient(time_step, jneqsim.util.util.UUIDJVM.randomUUID())
    
    # Run outlet streams
    gas_outlet.run()
    liquid_outlet.run()
    
    # Print results every 10 seconds
    if time % 10.0 == 0:
        print(f"{time:8.0f} | {separator.getPressure():15.2f} | "
              f"{gas_outlet.getFlowRate('kg/hr'):16.0f} | "
              f"{liquid_outlet.getFlowRate('kg/hr'):18.0f}")
    
    time += time_step

print("-" * 70)
print("\nTransient simulation complete!")
print("=" * 70)
