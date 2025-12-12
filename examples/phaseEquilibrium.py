# -*- coding: utf-8 -*-
"""
Phase Equilibrium and Saturation Points Tutorial
=================================================

This example demonstrates phase equilibrium calculations including:
- Bubble point (first gas appears from liquid)
- Dew point (first liquid appears from gas)
- Cricondenbar (maximum pressure on phase envelope)
- Cricondentherm (maximum temperature on phase envelope)
- Critical point estimation

These are fundamental concepts for understanding phase behavior in
oil and gas systems.

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash, phaseenvelope

print("=" * 70)
print("PHASE EQUILIBRIUM AND SATURATION POINTS TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. BUBBLE POINT CALCULATION
# =============================================================================
print("\n1. BUBBLE POINT CALCULATION")
print("-" * 40)
print("Bubble point: pressure/temperature where first gas bubble forms")
print("             (liquid at saturation)")

# Create a light oil
oil = fluid("pr")
oil.addComponent("methane", 20.0, "mol%")
oil.addComponent("ethane", 10.0, "mol%")
oil.addComponent("propane", 15.0, "mol%")
oil.addComponent("n-butane", 10.0, "mol%")
oil.addComponent("n-pentane", 15.0, "mol%")
oil.addComponent("n-hexane", 10.0, "mol%")
oil.addComponent("n-heptane", 10.0, "mol%")
oil.addComponent("n-octane", 10.0, "mol%")
oil.setMixingRule("classic")
oil.setMultiPhaseCheck(True)

# Calculate bubble point at 100°C
from neqsim.thermo import bubblepoint

oil.setTemperature(100.0, "C")
bp = bubblepoint(oil)

print(f"\nLight oil composition:")
print("  Methane: 20%, Ethane: 10%, Propane: 15%, Butane: 10%")
print("  Pentane: 15%, Hexane: 10%, Heptane: 10%, Octane: 10%")
print(f"\nBubble point at 100°C: {bp:.2f} bara")

# =============================================================================
# 2. DEW POINT CALCULATION
# =============================================================================
print("\n2. DEW POINT CALCULATION")
print("-" * 40)
print("Dew point: pressure/temperature where first liquid drop forms")
print("          (gas at saturation)")

# Create a rich natural gas
gas = fluid("pr")
gas.addComponent("methane", 80.0, "mol%")
gas.addComponent("ethane", 8.0, "mol%")
gas.addComponent("propane", 5.0, "mol%")
gas.addComponent("n-butane", 3.0, "mol%")
gas.addComponent("n-pentane", 2.0, "mol%")
gas.addComponent("n-hexane", 1.5, "mol%")
gas.addComponent("n-heptane", 0.5, "mol%")
gas.setMixingRule("classic")
gas.setMultiPhaseCheck(True)

# Calculate dew point at 20°C
from neqsim.thermo import dewpoint

gas.setTemperature(20.0, "C")
dp = dewpoint(gas)

print(f"\nRich gas composition:")
print("  Methane: 80%, Ethane: 8%, Propane: 5%, Butane: 3%")
print("  Pentane: 2%, Hexane: 1.5%, Heptane: 0.5%")
print(f"\nDew point at 20°C: {dp:.2f} bara")

# =============================================================================
# 3. PHASE ENVELOPE CALCULATION
# =============================================================================
print("\n3. PHASE ENVELOPE CALCULATION")
print("-" * 40)

# Use the rich gas for phase envelope
gas.setTemperature(25.0, "C")
gas.setPressure(50.0, "bara")
TPflash(gas)

print("Calculating phase envelope (bubble + dew point curves)...")

# Calculate phase envelope
envelope = phaseenvelope(gas)

# Get critical points
try:
    cricondenbar_T = envelope.get("cricondenbarT")[0] - 273.15  # Convert to °C
    cricondenbar_P = envelope.get("cricondenbarP")[0]
    cricondentherm_T = envelope.get("cricondenthermT")[0] - 273.15
    cricondentherm_P = envelope.get("cricondenthermP")[0]

    print(f"\nPhase Envelope Properties:")
    print(f"  Cricondenbar (max pressure):")
    print(f"    P = {cricondenbar_P:.2f} bara at T = {cricondenbar_T:.1f}°C")
    print(f"\n  Cricondentherm (max temperature):")
    print(f"    T = {cricondentherm_T:.1f}°C at P = {cricondentherm_P:.2f} bara")
except Exception as e:
    print(f"  Could not extract cricondenbar/cricondentherm: {e}")

# Get bubble and dew point curves
try:
    temps = envelope.get("Tsat")
    pressures = envelope.get("Psat")

    if temps and pressures:
        print(f"\n  Phase envelope points calculated: {len(temps)}")
        print("\n  Selected points on the envelope:")
        print("  T [°C]   | P [bara]")
        print("  ---------|----------")

        # Print every 5th point
        step = max(1, len(temps) // 8)
        for i in range(0, len(temps), step):
            t_c = temps[i] - 273.15
            p = pressures[i]
            print(f"  {t_c:8.1f} | {p:8.2f}")
except Exception as e:
    print(f"  Error accessing envelope data: {e}")

# =============================================================================
# 4. RETROGRADE CONDENSATION
# =============================================================================
print("\n4. RETROGRADE CONDENSATION")
print("-" * 40)
print(
    """
Retrograde condensation is a unique phenomenon in gas condensate systems
where REDUCING pressure causes MORE liquid to form (counterintuitive!).

This occurs between the cricondentherm and critical point at pressures
below the cricondenbar. It's important for gas condensate reservoirs.
"""
)

# Demonstrate retrograde behavior
print("Demonstrating retrograde behavior with the rich gas:")
print("Temperature: 20°C (between critical and cricondentherm)")
print("\nPressure [bara] | Liquid Fraction")
print("----------------|----------------")

test_gas = fluid("pr")
test_gas.addComponent("methane", 80.0, "mol%")
test_gas.addComponent("ethane", 8.0, "mol%")
test_gas.addComponent("propane", 5.0, "mol%")
test_gas.addComponent("n-butane", 3.0, "mol%")
test_gas.addComponent("n-pentane", 2.0, "mol%")
test_gas.addComponent("n-hexane", 1.5, "mol%")
test_gas.addComponent("n-heptane", 0.5, "mol%")
test_gas.setMixingRule("classic")
test_gas.setMultiPhaseCheck(True)

for p in [120, 100, 80, 60, 40, 20]:
    test_gas.setTemperature(20.0, "C")
    test_gas.setPressure(p, "bara")
    TPflash(test_gas)

    n_phases = test_gas.getNumberOfPhases()
    if n_phases > 1 and test_gas.hasPhaseType("oil"):
        liq_frac = test_gas.getPhase("oil").getBeta()
        print(f"{p:15} | {liq_frac:.4f}")
    else:
        print(f"{p:15} | 0.0000 (single phase)")

# =============================================================================
# 5. WATER DEW POINT
# =============================================================================
print("\n5. WATER DEW POINT")
print("-" * 40)
print("Water dew point: temperature where water starts to condense from gas")
print("Critical for pipeline operations to prevent corrosion and hydrates")

from neqsim.thermo import waterdewpoint

# Create a wet natural gas
wet_gas = fluid("cpa")
wet_gas.addComponent("methane", 90.0, "mol%")
wet_gas.addComponent("ethane", 5.0, "mol%")
wet_gas.addComponent("propane", 3.0, "mol%")
wet_gas.addComponent("water", 2.0, "mol%")
wet_gas.setMixingRule(10)  # CPA mixing rule
wet_gas.setMultiPhaseCheck(True)

# Calculate water dew point at different pressures
print("\nWet natural gas with 2 mol% water vapor:")
print("\nPressure [bara] | Water Dew Point [°C]")
print("----------------|--------------------")

for p in [50, 75, 100, 150]:
    try:
        wet_gas.setPressure(p, "bara")
        wdp = waterdewpoint(wet_gas)
        print(f"{p:15} | {wdp:.1f}")
    except Exception as e:
        print(f"{p:15} | Error: {e}")

# =============================================================================
# 6. CRICONDENBAR & CRICONDENTHERM SIGNIFICANCE
# =============================================================================
print("\n6. CRICONDENBAR & CRICONDENTHERM SIGNIFICANCE")
print("-" * 40)
print(
    """
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE ENVELOPE                                │
│                                                                  │
│    P │         Cricondenbar (max P)                             │
│      │              ●───────●                                   │
│      │           /           \\                                  │
│      │          /   2-phase   \\   Cricondentherm               │
│      │         /    region     \\  (max T)                      │
│      │        /        ●        ●                               │
│      │       /    Critical      │                               │
│      │      /      point        │                               │
│      │     /                    │                               │
│      │    ●────────────────────●                                │
│      │   Bubble               Dew                               │
│      │   curve               curve                              │
│      └──────────────────────────────────────────────────── T    │
│                                                                  │
│  ● Above cricondenbar: ALWAYS single phase (supercritical)     │
│  ● Above cricondentherm: Heating cannot cause condensation     │
│  ● Critical point: Liquid and gas become indistinguishable     │
└─────────────────────────────────────────────────────────────────┘
"""
)

print("=" * 70)
