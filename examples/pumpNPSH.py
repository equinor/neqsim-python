# -*- coding: utf-8 -*-
"""
Pump with NPSH (Net Positive Suction Head) Calculation Example

This example demonstrates pump calculations in NeqSim including:
- Pump power and efficiency
- NPSH available calculation
- Cavitation risk assessment
- Pump curves

NPSH is critical for pump design to prevent cavitation.
NPSHa (available) must exceed NPSHr (required) with safety margin.

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create a liquid fluid (hydrocarbon condensate)
liquid_fluid = fluid("srk")
liquid_fluid.addComponent("n-pentane", 20.0)
liquid_fluid.addComponent("n-hexane", 30.0)
liquid_fluid.addComponent("n-heptane", 30.0)
liquid_fluid.addComponent("n-octane", 20.0)
liquid_fluid.setMixingRule("classic")
liquid_fluid.setMultiPhaseCheck(True)
liquid_fluid.setTemperature(40.0, "C")
liquid_fluid.setPressure(3.0, "bara")  # Low suction pressure
liquid_fluid.setTotalFlowRate(200.0, "m3/hr")

# Create inlet stream
inlet_stream = jneqsim.process.equipment.stream.Stream("Pump Inlet", liquid_fluid)

# Create pump
pump = jneqsim.process.equipment.pump.Pump("Condensate Pump", inlet_stream)
pump.setOutletPressure(25.0)  # Discharge pressure in bara

# Enable NPSH checking
pump.setCheckNPSH(True)

# Create process and run
process = jneqsim.process.processmodel.ProcessSystem()
process.add(inlet_stream)
process.add(pump)
process.run()

# Get results
outlet_stream = pump.getOutletStream()
power_kw = pump.getPower() / 1000.0  # Convert W to kW
efficiency = pump.getIsentropicEfficiency() * 100.0

print("=" * 60)
print("PUMP SIMULATION WITH NPSH ANALYSIS")
print("=" * 60)

print("\nPump Specifications:")
print(f"  Suction pressure:   {inlet_stream.getPressure('bara'):.1f} bara")
print(f"  Discharge pressure: {outlet_stream.getPressure('bara'):.1f} bara")
print(
    f"  Differential:       {outlet_stream.getPressure('bara') - inlet_stream.getPressure('bara'):.1f} bar"
)

print("\nFlow Conditions:")
print(f"  Volume flow:        {inlet_stream.getFlowRate('m3/hr'):.0f} m³/hr")
print(f"  Suction temp:       {inlet_stream.getTemperature('C'):.1f} °C")
print(f"  Discharge temp:     {outlet_stream.getTemperature('C'):.1f} °C")

print("\nPump Performance:")
print(f"  Shaft power:        {power_kw:.1f} kW")
print(f"  Efficiency:         {efficiency:.1f}%")

# Calculate head (using typical liquid density)
inlet_fluid = inlet_stream.getFluid()
if inlet_fluid.hasPhaseType("oil"):
    density = inlet_fluid.getPhase("oil").getDensity("kg/m3")
    dp_pa = (outlet_stream.getPressure("bara") - inlet_stream.getPressure("bara")) * 1e5
    head_m = dp_pa / (density * 9.81)
    print(f"  Head:               {head_m:.1f} m")
    print(f"  Liquid density:     {density:.1f} kg/m³")

# NPSH Analysis
print("\nNPSH Analysis:")
npsha = pump.getNPSHAvailable()
if npsha > 0:
    print(f"  NPSHa (available):  {npsha:.2f} m")

    # Check for cavitation
    if pump.isCavitating():
        print(f"  ⚠️  WARNING: CAVITATION RISK!")
        print(f"     Consider increasing suction pressure")
        print(f"     or reducing pump speed/flow")
    else:
        print(f"  ✓ No cavitation risk detected")
else:
    print(f"  NPSHa calculation not available")
    print(f"  Tip: Check fluid has liquid phase at suction")

print("=" * 60)
