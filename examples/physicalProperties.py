# -*- coding: utf-8 -*-
"""
Physical Properties Calculation Tutorial
==========================================

This example demonstrates how to calculate physical (transport) properties
of fluids using NeqSim. Physical properties are essential for equipment
sizing and flow calculations.

Properties Covered:
    - Density (from EoS and correlations)
    - Viscosity (dynamic and kinematic)
    - Thermal conductivity
    - Surface/interfacial tension
    - Heat capacity (Cp, Cv)
    - Speed of sound
    - Joule-Thomson coefficient

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash, printFrame

print("=" * 70)
print("PHYSICAL PROPERTIES CALCULATION TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. CREATE AND FLASH A MULTIPHASE FLUID
# =============================================================================
print("\n1. CREATING MULTIPHASE FLUID")
print("-" * 40)

# Create a fluid that will have gas, oil, and water phases
multiphase = fluid("cpa")  # CPA equation of state handles water well
multiphase.addComponent("nitrogen", 1.0, "mol%")
multiphase.addComponent("CO2", 3.0, "mol%")
multiphase.addComponent("methane", 70.0, "mol%")
multiphase.addComponent("ethane", 8.0, "mol%")
multiphase.addComponent("propane", 5.0, "mol%")
multiphase.addComponent("n-butane", 3.0, "mol%")
multiphase.addComponent("n-pentane", 2.0, "mol%")
multiphase.addComponent("n-hexane", 3.0, "mol%")
multiphase.addComponent("n-heptane", 3.0, "mol%")
multiphase.addComponent("water", 2.0, "mol%")
multiphase.setMixingRule(10)  # CPA mixing rule
multiphase.setMultiPhaseCheck(True)

# Set conditions and flash
multiphase.setTemperature(60.0, "C")
multiphase.setPressure(20.0, "bara")
TPflash(multiphase)

# IMPORTANT: Initialize physical properties after flash
multiphase.initThermoProperties()
multiphase.initPhysicalProperties()

print(f"Conditions: T = 60°C, P = 20 bara")
print(f"Number of phases: {multiphase.getNumberOfPhases()}")

# =============================================================================
# 2. DENSITY
# =============================================================================
print("\n2. DENSITY")
print("-" * 40)

# Overall mixture density
total_density = multiphase.getDensity("kg/m3")
print(f"Overall mixture density: {total_density:.2f} kg/m³")

# Phase-specific densities
if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    print(f"\nGas phase:")
    print(f"  Density: {gas.getDensity('kg/m3'):.4f} kg/m³")
    print(f"  Molar density: {gas.getDensity('mol/m3'):.2f} mol/m³")
    print(f"  Molar volume: {1.0/gas.getDensity('mol/m3')*1e6:.2f} cm³/mol")
    print(f"  Z-factor: {gas.getZ():.4f}")
    # Molar mass for specific gravity
    print(f"  Molar mass: {gas.getMolarMass()*1000:.2f} g/mol")

if multiphase.hasPhaseType("oil"):
    oil = multiphase.getPhase("oil")
    print(f"\nOil (liquid hydrocarbon) phase:")
    print(f"  Density: {oil.getDensity('kg/m3'):.2f} kg/m³")
    print(f"  Molar density: {oil.getDensity('mol/m3'):.2f} mol/m³")
    # API gravity calculation
    sg = oil.getDensity("kg/m3") / 999.0  # specific gravity
    api = 141.5 / sg - 131.5
    print(f"  Specific gravity: {sg:.4f}")
    print(f"  API gravity: {api:.1f}° API")

if multiphase.hasPhaseType("aqueous"):
    aq = multiphase.getPhase("aqueous")
    print(f"\nAqueous phase:")
    print(f"  Density: {aq.getDensity('kg/m3'):.2f} kg/m³")

# =============================================================================
# 3. VISCOSITY
# =============================================================================
print("\n3. VISCOSITY")
print("-" * 40)

# Overall mixture viscosity (limited meaning for multiphase)
total_visc = multiphase.getViscosity("kg/msec")
print(f"Overall viscosity: {total_visc:.6f} kg/(m·s) = {total_visc*1000:.4f} cP")

# Phase-specific viscosities
if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    gas_visc = gas.getViscosity("kg/msec")
    gas_density = gas.getDensity("kg/m3")
    kinematic_visc = gas_visc / gas_density  # m²/s
    print(f"\nGas phase:")
    print(f"  Dynamic viscosity: {gas_visc:.6f} kg/(m·s)")
    print(f"  Dynamic viscosity: {gas_visc*1000:.4f} cP")
    print(f"  Kinematic viscosity: {kinematic_visc*1e6:.4f} cSt")

if multiphase.hasPhaseType("oil"):
    oil = multiphase.getPhase("oil")
    oil_visc = oil.getViscosity("kg/msec")
    oil_density = oil.getDensity("kg/m3")
    kinematic_visc = oil_visc / oil_density
    print(f"\nOil phase:")
    print(f"  Dynamic viscosity: {oil_visc:.6f} kg/(m·s)")
    print(f"  Dynamic viscosity: {oil_visc*1000:.2f} cP")
    print(f"  Kinematic viscosity: {kinematic_visc*1e6:.2f} cSt")

if multiphase.hasPhaseType("aqueous"):
    aq = multiphase.getPhase("aqueous")
    aq_visc = aq.getViscosity("kg/msec")
    print(f"\nAqueous phase:")
    print(f"  Dynamic viscosity: {aq_visc:.6f} kg/(m·s)")
    print(f"  Dynamic viscosity: {aq_visc*1000:.4f} cP")

# =============================================================================
# 4. THERMAL CONDUCTIVITY
# =============================================================================
print("\n4. THERMAL CONDUCTIVITY")
print("-" * 40)

if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    k_gas = gas.getThermalConductivity()
    print(f"Gas phase: {k_gas:.6f} W/(m·K)")

if multiphase.hasPhaseType("oil"):
    oil = multiphase.getPhase("oil")
    k_oil = oil.getThermalConductivity()
    print(f"Oil phase: {k_oil:.4f} W/(m·K)")

if multiphase.hasPhaseType("aqueous"):
    aq = multiphase.getPhase("aqueous")
    k_aq = aq.getThermalConductivity()
    print(f"Aqueous phase: {k_aq:.4f} W/(m·K)")

# =============================================================================
# 5. HEAT CAPACITY
# =============================================================================
print("\n5. HEAT CAPACITY")
print("-" * 40)

# Overall heat capacities
Cp = multiphase.getCp("J/molK")
Cv = multiphase.getCv("J/molK")
gamma = multiphase.getKappa()  # Cp/Cv ratio

print(f"Overall mixture:")
print(f"  Cp: {Cp:.2f} J/(mol·K)")
print(f"  Cv: {Cv:.2f} J/(mol·K)")
print(f"  γ = Cp/Cv: {gamma:.4f}")

if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    print(f"\nGas phase:")
    print(f"  Cp: {gas.getCp('J/molK'):.2f} J/(mol·K)")
    print(f"  Cp: {gas.getCp('J/kgK'):.2f} J/(kg·K)")
    print(f"  γ = Cp/Cv: {gas.getGamma():.4f}")

# =============================================================================
# 6. SPEED OF SOUND
# =============================================================================
print("\n6. SPEED OF SOUND")
print("-" * 40)

if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    sos = gas.getSoundSpeed()
    print(f"Gas phase: {sos:.1f} m/s")

if multiphase.hasPhaseType("oil"):
    oil = multiphase.getPhase("oil")
    sos = oil.getSoundSpeed()
    print(f"Oil phase: {sos:.1f} m/s")

# =============================================================================
# 7. JOULE-THOMSON COEFFICIENT
# =============================================================================
print("\n7. JOULE-THOMSON COEFFICIENT")
print("-" * 40)
print("μJT = (∂T/∂P)H - Temperature change per unit pressure drop")

if multiphase.hasPhaseType("gas"):
    gas = multiphase.getPhase("gas")
    jt = gas.getJouleThomsonCoefficient()
    # Convert from K/Pa to K/bar
    jt_per_bar = jt * 1e5
    print(f"\nGas phase:")
    print(f"  μJT: {jt_per_bar:.4f} K/bar")
    if jt_per_bar > 0:
        print(f"  → Gas cools when throttled (normal JT effect)")
    else:
        print(f"  → Gas heats when throttled (inverse JT effect)")

# =============================================================================
# 8. SURFACE TENSION
# =============================================================================
print("\n8. INTERFACIAL TENSION")
print("-" * 40)

# Get interfacial tension between phases if both exist
if multiphase.getNumberOfPhases() >= 2:
    try:
        # Surface tension between gas and liquid
        ift = multiphase.getInterphaseProperties().getSurfaceTension(0, 1)
        print(f"Interfacial tension (phase 0/1): {ift*1000:.2f} mN/m")
    except:
        print("Interfacial tension calculation not available for these phases")

# =============================================================================
# 9. PROPERTY VARIATION WITH CONDITIONS
# =============================================================================
print("\n9. PROPERTY VARIATION WITH TEMPERATURE")
print("-" * 40)
print("Showing gas viscosity variation:")

# Create a simple gas
simple_gas = fluid("srk")
simple_gas.addComponent("methane", 90.0, "mol%")
simple_gas.addComponent("ethane", 10.0, "mol%")
simple_gas.setMixingRule("classic")
simple_gas.setPressure(50.0, "bara")

print("\nT (°C) | Density (kg/m³) | Viscosity (cP) | k (W/m·K)")
print("-" * 55)

for temp in [0, 25, 50, 75, 100]:
    simple_gas.setTemperature(float(temp), "C")
    TPflash(simple_gas)
    simple_gas.initThermoProperties()
    simple_gas.initPhysicalProperties()
    
    if simple_gas.hasPhaseType("gas"):
        gas = simple_gas.getPhase("gas")
        rho = gas.getDensity("kg/m3")
        mu = gas.getViscosity("kg/msec") * 1000  # cP
        k = gas.getThermalConductivity()
        print(f"{temp:6} | {rho:15.2f} | {mu:14.4f} | {k:.6f}")

print("=" * 70)
print("\nNOTES:")
print("- Always call initPhysicalProperties() after TPflash()")
print("- Physical properties are calculated using correlations")
print("- EoS provides thermodynamic properties (density, enthalpy, etc.)")
print("- Transport properties use Lohrenz-Bray-Clark (LBC) or other models")
print("=" * 70)
