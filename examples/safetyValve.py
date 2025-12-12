# -*- coding: utf-8 -*-
"""
Pressure Safety Valve (PSV) Simulation Example

This example demonstrates using a Pressure Safety Valve in NeqSim.
PSVs provide mechanical overpressure protection as a final safety layer.

Features demonstrated:
- Setting PSV parameters (set pressure, full open pressure, blowdown)
- Simulating pressure buildup and PSV response
- Transient PSV behavior
- Integration with flare system

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create feed gas for a high-pressure separator
separator_gas = fluid("srk")
separator_gas.addComponent("methane", 85.0)
separator_gas.addComponent("ethane", 8.0)
separator_gas.addComponent("propane", 4.0)
separator_gas.addComponent("n-butane", 2.0)
separator_gas.addComponent("CO2", 1.0)
separator_gas.setMixingRule("classic")
separator_gas.setTemperature(45.0, "C")
separator_gas.setPressure(50.0, "bara")  # Normal operating pressure
separator_gas.setTotalFlowRate(50000.0, "kg/hr")

# Create streams
feed_stream = jneqsim.process.equipment.stream.Stream("Feed Stream", separator_gas)

# Create a separator
separator = jneqsim.process.equipment.separator.Separator("HP Separator", feed_stream)

# Get gas outlet from separator
gas_outlet = separator.getGasOutStream()

# Create Pressure Safety Valve
# PSV specifications based on typical design:
# - Set pressure: 10% above operating (55 bara)
# - Full open pressure: 10% above set pressure (60.5 bara)
# - Blowdown: 7% (reseats at 93% of set pressure)
psv = jneqsim.process.equipment.valve.SafetyValve("PSV-001", gas_outlet)
psv.setPressureSpec(55.0)  # Set pressure in bara
psv.setFullOpenPressure(60.5)  # Full open pressure in bara
psv.setBlowdown(7.0)  # Blowdown percentage

# Create PSV relief stream
psv_relief = jneqsim.process.equipment.stream.Stream(
    "PSV Relief", psv.getOutletStream()
)

# Create flare header (mixer to collect relief streams)
flare_header = jneqsim.process.equipment.mixer.Mixer("Flare Header")
flare_header.addStream(psv_relief)

# Create flare
flare_outlet = jneqsim.process.equipment.stream.Stream(
    "Flare Header Outlet", flare_header.getOutletStream()
)
flare = jneqsim.process.equipment.flare.Flare("Emergency Flare", flare_outlet)
flare.setFlameHeight(50.0)
flare.setRadiantFraction(0.18)
flare.setTipDiameter(0.6)

# Build process
process = jneqsim.process.processmodel.ProcessSystem()
process.add(feed_stream)
process.add(separator)
process.add(psv)
process.add(psv_relief)
process.add(flare_header)
process.add(flare_outlet)
process.add(flare)

# Run at normal conditions
process.run()

print("=" * 70)
print("PRESSURE SAFETY VALVE SIMULATION")
print("=" * 70)

print("\nPSV Configuration:")
print(f"  Set pressure:       55.0 bara")
print(f"  Full open pressure: 60.5 bara")
print(f"  Blowdown:           7%")
print(f"  Reseat pressure:    {55.0 * 0.93:.1f} bara")

print("\nNormal Operating Conditions (50 bara):")
print(f"  Separator pressure: {separator.getPressure():.1f} bara")
print(
    f"  PSV status:         {'CLOSED' if psv.getPercentValveOpening() < 0.1 else 'OPEN'}"
)
print(f"  PSV opening:        {psv.getPercentValveOpening():.1f}%")

# Simulate overpressure by increasing separator pressure
print("\n" + "-" * 70)
print("Simulating overpressure scenario...")
print("-" * 70)

# Increase inlet pressure to simulate blocked outlet
separator_gas.setPressure(58.0, "bara")  # Above set pressure
feed_stream.setFluid(separator_gas)
process.run()

print(f"\nOverpressure Conditions (58 bara inlet):")
print(f"  PSV status:   {'CLOSED' if psv.getPercentValveOpening() < 0.1 else 'OPEN'}")
print(f"  PSV opening:  {psv.getPercentValveOpening():.1f}%")

if psv.getPercentValveOpening() > 0:
    print(f"\n⚠️  PSV IS RELIEVING!")
    print(f"  Relief rate:  {psv_relief.getFlowRate('kg/hr'):.0f} kg/hr")
    print(f"  Flare duty:   {flare.getHeatDuty('MW'):.2f} MW")
    print(f"  CO2 emission: {flare.getCO2Emission('kg/hr'):.0f} kg/hr")
else:
    print("\n✓ PSV remains closed - pressure below set point")

print("=" * 70)
