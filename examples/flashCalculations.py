# -*- coding: utf-8 -*-
"""
Thermodynamic Flash Calculations Tutorial
==========================================

This example demonstrates various flash calculation types available in NeqSim.
Flash calculations determine the equilibrium state of a mixture given two
thermodynamic specifications.

Flash Types Covered:
    - TPflash: Temperature-Pressure flash (most common)
    - PHflash: Pressure-Enthalpy flash (adiabatic processes)
    - PSflash: Pressure-Entropy flash (isentropic processes)
    - TVflash: Temperature-Volume flash (constant volume systems)
    - VHflash: Volume-Enthalpy flash (closed adiabatic systems)
    - VUflash: Volume-Internal Energy flash (isolated systems)

@author: NeqSim Team
"""

from neqsim.thermo import (
    fluid,
    TPflash,
    PHflash,
    PSflash,
    TVflash,
    VHflash,
    VUflash,
    printFrame,
)

print("=" * 70)
print("THERMODYNAMIC FLASH CALCULATIONS TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. CREATE A TEST FLUID
# =============================================================================
# Using SRK (Soave-Redlich-Kwong) equation of state
natural_gas = fluid("srk")
natural_gas.addComponent("nitrogen", 2.0, "mol%")
natural_gas.addComponent("CO2", 1.5, "mol%")
natural_gas.addComponent("methane", 85.0, "mol%")
natural_gas.addComponent("ethane", 6.0, "mol%")
natural_gas.addComponent("propane", 3.0, "mol%")
natural_gas.addComponent("i-butane", 1.0, "mol%")
natural_gas.addComponent("n-butane", 1.0, "mol%")
natural_gas.addComponent("n-pentane", 0.5, "mol%")
natural_gas.setMixingRule("classic")  # Use standard binary interaction parameters
natural_gas.setMultiPhaseCheck(True)  # Enable detection of multiple phases

print("\n1. FLUID COMPOSITION")
print("-" * 40)
print("Component fractions specified as mol%")
print("Equation of State: SRK (Soave-Redlich-Kwong)")

# =============================================================================
# 2. TP FLASH (Temperature-Pressure)
# =============================================================================
# Most common flash type - specify T and P, calculate phase equilibrium
print("\n2. TP FLASH (Temperature-Pressure)")
print("-" * 40)
print("Given: T = -20°C, P = 30 bara")
print("Find: Number of phases, phase compositions, densities")

natural_gas.setTemperature(-20.0, "C")
natural_gas.setPressure(30.0, "bara")
TPflash(natural_gas)
natural_gas.initThermoProperties()
natural_gas.initPhysicalProperties()

print(f"\nResults:")
print(f"  Number of phases: {natural_gas.getNumberOfPhases()}")
print(f"  Total density: {natural_gas.getDensity('kg/m3'):.2f} kg/m³")

if natural_gas.hasPhaseType("gas"):
    gas_phase = natural_gas.getPhase("gas")
    print(f"  Gas phase:")
    print(
        f"    - Mole fraction: {natural_gas.getMoleFraction(natural_gas.getPhaseNumberOfPhase('gas')):.4f}"
    )
    print(f"    - Density: {gas_phase.getDensity('kg/m3'):.2f} kg/m³")
    print(f"    - Z-factor: {gas_phase.getZ():.4f}")

if natural_gas.hasPhaseType("oil"):
    oil_phase = natural_gas.getPhase("oil")
    print(f"  Liquid phase:")
    print(
        f"    - Mole fraction: {natural_gas.getMoleFraction(natural_gas.getPhaseNumberOfPhase('oil')):.4f}"
    )
    print(f"    - Density: {oil_phase.getDensity('kg/m3'):.2f} kg/m³")

# =============================================================================
# 3. PH FLASH (Pressure-Enthalpy)
# =============================================================================
# Used for adiabatic processes (no heat transfer)
# Example: Joule-Thomson expansion through a valve
print("\n3. PH FLASH (Pressure-Enthalpy)")
print("-" * 40)
print("Application: Adiabatic throttling (Joule-Thomson expansion)")

# First, establish initial state
natural_gas.setTemperature(30.0, "C")
natural_gas.setPressure(100.0, "bara")
TPflash(natural_gas)
natural_gas.initThermoProperties()

# Get initial enthalpy
initial_enthalpy = natural_gas.getEnthalpy("J")
initial_temp = natural_gas.getTemperature("C")
print(f"\nInitial state: T = {initial_temp:.1f}°C, P = 100 bara")
print(f"Initial enthalpy: {initial_enthalpy/1e6:.2f} MJ")

# Throttle to lower pressure (isenthalpic process)
natural_gas.setPressure(20.0, "bara")
PHflash(natural_gas, initial_enthalpy, "J")
natural_gas.initThermoProperties()

final_temp = natural_gas.getTemperature("C")
print(f"\nAfter throttling to 20 bara:")
print(f"  Final temperature: {final_temp:.1f}°C")
print(f"  Temperature drop (JT effect): {initial_temp - final_temp:.1f}°C")

# =============================================================================
# 4. PS FLASH (Pressure-Entropy)
# =============================================================================
# Used for isentropic processes (reversible adiabatic)
# Example: Ideal compression or expansion
print("\n4. PS FLASH (Pressure-Entropy)")
print("-" * 40)
print("Application: Isentropic compression in a compressor")

# Reset fluid and establish initial state
natural_gas.setTemperature(25.0, "C")
natural_gas.setPressure(10.0, "bara")
TPflash(natural_gas)
natural_gas.initThermoProperties()

initial_entropy = natural_gas.getEntropy("J/K")
initial_temp = natural_gas.getTemperature("C")
print(f"\nSuction conditions: T = {initial_temp:.1f}°C, P = 10 bara")
print(f"Entropy: {initial_entropy:.2f} J/K")

# Compress to higher pressure isentropically
natural_gas.setPressure(50.0, "bara")
PSflash(natural_gas, initial_entropy, "J/K")
natural_gas.initThermoProperties()

discharge_temp = natural_gas.getTemperature("C")
print(f"\nIsentropic discharge at 50 bara:")
print(f"  Discharge temperature: {discharge_temp:.1f}°C")
print(f"  Temperature rise: {discharge_temp - initial_temp:.1f}°C")

# =============================================================================
# 5. TV FLASH (Temperature-Volume)
# =============================================================================
# Used when system volume is fixed
# Example: Closed container at constant temperature
print("\n5. TV FLASH (Temperature-Volume)")
print("-" * 40)
print("Application: Fixed volume container")

natural_gas.setTemperature(25.0, "C")
natural_gas.setPressure(50.0, "bara")
TPflash(natural_gas)
natural_gas.initThermoProperties()

# Get current volume
system_volume = natural_gas.getVolume("m3")
print(f"\nInitial state: T = 25°C, P = 50 bara")
print(f"System volume: {system_volume:.6f} m³")

# Change temperature while keeping volume constant
TVflash(natural_gas, system_volume, "m3")
natural_gas.setTemperature(50.0, "C")
TVflash(natural_gas, system_volume, "m3")
natural_gas.initThermoProperties()

new_pressure = natural_gas.getPressure("bara")
print(f"\nAfter heating to 50°C at constant volume:")
print(f"  New pressure: {new_pressure:.2f} bara")

# =============================================================================
# 6. SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("FLASH CALCULATION SUMMARY")
print("=" * 70)
print(
    """
Flash Type | Given          | Find           | Application
-----------|----------------|----------------|---------------------------
TPflash    | T, P           | Phases, comp.  | General equilibrium
PHflash    | P, H           | T, phases      | Valves, throttling
PSflash    | P, S           | T, phases      | Compressors, turbines
TVflash    | T, V           | P, phases      | Closed vessels
VHflash    | V, H           | T, P, phases   | Adiabatic closed systems
VUflash    | V, U           | T, P, phases   | Isolated systems
"""
)
print("=" * 70)
