# -*- coding: utf-8 -*-
"""
Flare System Simulation Example

This example demonstrates using the Flare unit operation in NeqSim.
A flare is used to safely combust emergency relief gases, typically 
from pressure safety valves (PSV) or blowdown systems.

Features demonstrated:
- Setting up a flare with design parameters
- Calculating heat release and emissions
- CO2 emission tracking
- Thermal radiation calculations

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create relief gas fluid (typical hydrocarbon gas)
relief_gas = fluid("srk")
relief_gas.addComponent("methane", 80.0)
relief_gas.addComponent("ethane", 10.0)
relief_gas.addComponent("propane", 5.0)
relief_gas.addComponent("n-butane", 3.0)
relief_gas.addComponent("CO2", 2.0)
relief_gas.setMixingRule("classic")
relief_gas.setTemperature(50.0, "C")
relief_gas.setPressure(2.0, "bara")  # Low pressure after relief valve
relief_gas.setTotalFlowRate(10000.0, "kg/hr")  # Emergency relief rate

# Create the inlet stream to flare
flare_inlet = jneqsim.process.equipment.stream.Stream("Flare Inlet", relief_gas)

# Create flare unit
flare = jneqsim.process.equipment.flare.Flare("Main Flare", flare_inlet)

# Configure flare parameters
flare.setFlameHeight(60.0)  # Flame height in meters
flare.setRadiantFraction(0.20)  # Fraction of heat radiated (typical 0.15-0.30)
flare.setTipDiameter(0.8)  # Tip diameter in meters

# Set design capacities for utilization checks (optional)
flare.setDesignHeatDutyCapacity(50.0, "MW")
flare.setDesignMassFlowCapacity(20000.0, "kg/hr")

# Create process and run
process = jneqsim.process.processmodel.ProcessSystem()
process.add(flare_inlet)
process.add(flare)
process.run()

# Get results
heat_duty_mw = flare.getHeatDuty("MW")
co2_emission = flare.getCO2Emission("kg/hr")

print("=" * 60)
print("FLARE SYSTEM SIMULATION RESULTS")
print("=" * 60)

print(f"\nFlare Configuration:")
print(f"  Flame height:     {60.0} m")
print(f"  Radiant fraction: {0.20:.0%}")
print(f"  Tip diameter:     {0.8} m")

print(f"\nOperating Conditions:")
print(f"  Inlet pressure:    {flare_inlet.getPressure('bara'):.1f} bara")
print(f"  Inlet temperature: {flare_inlet.getTemperature('C'):.1f} °C")
print(f"  Mass flow rate:    {flare_inlet.getFlowRate('kg/hr'):.0f} kg/hr")

print(f"\nFlare Performance:")
print(f"  Heat duty:         {heat_duty_mw:.2f} MW")
print(f"  CO2 emissions:     {co2_emission:.0f} kg/hr")
print(f"  CO2 emissions:     {co2_emission * 24 / 1000:.1f} tonnes/day")

# Check capacity utilization
capacity_check = flare.checkCapacity()
if capacity_check.isOverloaded():
    print(f"\n⚠️  WARNING: Flare is OVERLOADED!")
    print(f"  Heat utilization: {capacity_check.getHeatUtilization() * 100:.1f}%")
    print(f"  Mass utilization: {capacity_check.getMassUtilization() * 100:.1f}%")
else:
    print(f"\n✓ Flare is within design capacity")
    if not float('nan') == capacity_check.getHeatUtilization():
        print(f"  Heat utilization: {capacity_check.getHeatUtilization() * 100:.1f}%")
    if not float('nan') == capacity_check.getMassUtilization():
        print(f"  Mass utilization: {capacity_check.getMassUtilization() * 100:.1f}%")

print("=" * 60)
