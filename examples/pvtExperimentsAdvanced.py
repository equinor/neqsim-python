# -*- coding: utf-8 -*-
"""
Improved PVT Experiments Tutorial
==================================

This example provides comprehensive coverage of PVT (Pressure-Volume-Temperature)
experiments commonly used in oil and gas reservoir studies.

PVT Experiments Covered:
    1. Constant Mass Expansion (CME)
    2. Constant Volume Depletion (CVD)
    3. Differential Liberation
    4. Separator Test
    5. Swelling Test
    6. Viscosity Study

These experiments are essential for:
    - Reservoir characterization
    - Production forecasting
    - Facility design
    - EOR (Enhanced Oil Recovery) studies

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash

print("=" * 70)
print("PVT EXPERIMENTS TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. FLUID DEFINITION - Black Oil Sample
# =============================================================================
print("\n1. DEFINING A BLACK OIL SAMPLE")
print("-" * 40)

oil = fluid("pr")
oil.addComponent("nitrogen", 0.5, "mol%")
oil.addComponent("CO2", 1.5, "mol%")
oil.addComponent("methane", 40.0, "mol%")
oil.addComponent("ethane", 8.0, "mol%")
oil.addComponent("propane", 6.0, "mol%")
oil.addComponent("i-butane", 1.5, "mol%")
oil.addComponent("n-butane", 3.0, "mol%")
oil.addComponent("i-pentane", 1.5, "mol%")
oil.addComponent("n-pentane", 2.0, "mol%")
oil.addComponent("n-hexane", 3.0, "mol%")
oil.addComponent("C7", 33.0, "mol%")  # Heptane-plus fraction
oil.setMixingRule("classic")
oil.setMultiPhaseCheck(True)

# Set C7+ properties (typically from lab analysis)
oil.getPhase(0).getComponent("C7").setMolarMass(0.150)  # 150 g/mol
oil.getPhase(0).getComponent("C7").setNormalLiquidDensity(780.0)  # kg/m³

# Reservoir conditions
reservoir_T = 100.0  # °C
reservoir_P = 250.0  # bara

oil.setTemperature(reservoir_T, "C")
oil.setPressure(reservoir_P, "bara")
TPflash(oil)

print("Black oil composition defined:")
print("  Light ends: N2, CO2, C1-C6")
print("  C7+ fraction: 33 mol%")
print(f"\nReservoir conditions: T = {reservoir_T}°C, P = {reservoir_P} bara")

# =============================================================================
# 2. SATURATION PRESSURE (Bubble Point)
# =============================================================================
print("\n2. SATURATION PRESSURE (BUBBLE POINT)")
print("-" * 40)

from neqsim.thermo import bubblepoint

oil.setTemperature(reservoir_T, "C")
psat = bubblepoint(oil)

print(f"Bubble point pressure at {reservoir_T}°C: {psat:.1f} bara")
print("\nInterpretation:")
print("  - Above Psat: Single phase (undersaturated oil)")
print("  - Below Psat: Two phases (oil + liberated gas)")

# =============================================================================
# 3. CONSTANT MASS EXPANSION (CME)
# =============================================================================
print("\n3. CONSTANT MASS EXPANSION (CME)")
print("-" * 40)
print("CME simulates pressure depletion at constant composition and temperature")
print("Key outputs: Relative volume, oil compressibility, density, GOR")

print(f"\nCME at T = {reservoir_T}°C")
print("\nP [bara] | Rel.Vol | Oil ρ    | Gas ρ    | Z-gas")
print("         |   [-]   | [kg/m³]  | [kg/m³]  |  [-]")
print("-" * 55)

# Reference volume at saturation pressure
oil.setTemperature(reservoir_T, "C")
oil.setPressure(psat, "bara")
TPflash(oil)
oil.initThermoProperties()
v_sat = oil.getVolume("m3")

# Pressure steps
pressures = [psat, psat * 0.9, psat * 0.8, psat * 0.7, psat * 0.5, psat * 0.3]

for p in pressures:
    oil.setTemperature(reservoir_T, "C")
    oil.setPressure(p, "bara")
    TPflash(oil)
    oil.initThermoProperties()

    v_total = oil.getVolume("m3")
    rel_vol = v_total / v_sat

    # Get phase properties
    if oil.hasPhaseType("oil"):
        rho_oil = oil.getPhase("oil").getDensity("kg/m3")
    else:
        rho_oil = oil.getDensity("kg/m3")

    if oil.hasPhaseType("gas"):
        rho_gas = oil.getPhase("gas").getDensity("kg/m3")
        z_gas = oil.getPhase("gas").getZ()
        print(
            f"{p:8.1f} | {rel_vol:7.4f} | {rho_oil:8.1f} | {rho_gas:8.2f} | {z_gas:.4f}"
        )
    else:
        print(f"{p:8.1f} | {rel_vol:7.4f} | {rho_oil:8.1f} | (single) | -")

# =============================================================================
# 4. DIFFERENTIAL LIBERATION
# =============================================================================
print("\n4. DIFFERENTIAL LIBERATION")
print("-" * 40)
print("Gas is removed at each pressure step (unlike CME where gas stays)")
print("Simulates how gas separates in the reservoir")

print(f"\nDifferential Liberation at T = {reservoir_T}°C")
print("Starting from saturation pressure")
print("\nP [bara] | Oil Vol  | Gas Vol  | GOR")
print("         | [m³]     | [m³]     | [Sm³/Sm³]")
print("-" * 50)

# Create fresh fluid
diff_oil = fluid("pr")
diff_oil.addComponent("nitrogen", 0.5, "mol%")
diff_oil.addComponent("CO2", 1.5, "mol%")
diff_oil.addComponent("methane", 40.0, "mol%")
diff_oil.addComponent("ethane", 8.0, "mol%")
diff_oil.addComponent("propane", 6.0, "mol%")
diff_oil.addComponent("i-butane", 1.5, "mol%")
diff_oil.addComponent("n-butane", 3.0, "mol%")
diff_oil.addComponent("i-pentane", 1.5, "mol%")
diff_oil.addComponent("n-pentane", 2.0, "mol%")
diff_oil.addComponent("n-hexane", 3.0, "mol%")
diff_oil.addComponent("C7", 33.0, "mol%")
diff_oil.setMixingRule("classic")
diff_oil.setMultiPhaseCheck(True)

# Perform differential liberation
pressures = [psat, psat * 0.8, psat * 0.6, psat * 0.4]

total_gas_produced = 0.0

for i, p in enumerate(pressures):
    diff_oil.setTemperature(reservoir_T, "C")
    diff_oil.setPressure(p, "bara")
    TPflash(diff_oil)
    diff_oil.initThermoProperties()

    if diff_oil.hasPhaseType("gas") and diff_oil.hasPhaseType("oil"):
        v_oil = diff_oil.getPhase("oil").getVolume("m3")
        v_gas = diff_oil.getPhase("gas").getVolume("m3")

        # Simple GOR calculation (approximate)
        n_gas = diff_oil.getPhase("gas").getNumberOfMolesInPhase()
        n_oil = diff_oil.getPhase("oil").getNumberOfMolesInPhase()
        gor = (n_gas / n_oil) * 100 if n_oil > 0 else 0

        print(f"{p:8.1f} | {v_oil:.2e} | {v_gas:.2e} | {gor:.1f}")
    else:
        v_total = diff_oil.getVolume("m3")
        print(f"{p:8.1f} | {v_total:.2e} | (single) | -")

# =============================================================================
# 5. SEPARATOR TEST
# =============================================================================
print("\n5. SEPARATOR TEST")
print("-" * 40)
print("Multi-stage separation to optimize oil recovery and gas quality")

# Create fresh reservoir fluid
sep_oil = fluid("pr")
sep_oil.addComponent("methane", 50.0, "mol%")
sep_oil.addComponent("ethane", 10.0, "mol%")
sep_oil.addComponent("propane", 8.0, "mol%")
sep_oil.addComponent("n-butane", 5.0, "mol%")
sep_oil.addComponent("n-pentane", 7.0, "mol%")
sep_oil.addComponent("n-hexane", 8.0, "mol%")
sep_oil.addComponent("n-heptane", 12.0, "mol%")
sep_oil.setMixingRule("classic")
sep_oil.setMultiPhaseCheck(True)

# Separator conditions
sep_stages = [
    (50.0, 40.0),  # Stage 1: 50 bara, 40°C
    (10.0, 30.0),  # Stage 2: 10 bara, 30°C
    (1.0, 20.0),  # Stock tank: 1 bara, 20°C
]

print("\nStage | P [bara] | T [°C] | Gas Fraction | Oil Density")
print("-" * 55)

for i, (p, t) in enumerate(sep_stages):
    sep_oil.setTemperature(t, "C")
    sep_oil.setPressure(p, "bara")
    TPflash(sep_oil)
    sep_oil.initThermoProperties()

    if sep_oil.hasPhaseType("gas"):
        gas_frac = sep_oil.getPhase("gas").getBeta()
        oil_rho = (
            sep_oil.getPhase("oil").getDensity("kg/m3")
            if sep_oil.hasPhaseType("oil")
            else 0
        )
    else:
        gas_frac = 0
        oil_rho = sep_oil.getDensity("kg/m3")

    stage_name = f"Stage {i+1}" if i < 2 else "Tank"
    print(f"{stage_name:5} | {p:8.1f} | {t:6.1f} | {gas_frac:12.4f} | {oil_rho:.1f}")

# =============================================================================
# 6. SWELLING TEST (CO2 Injection)
# =============================================================================
print("\n6. SWELLING TEST (CO2 INJECTION)")
print("-" * 40)
print("Swelling test evaluates enhanced oil recovery by gas injection")
print("Adding CO2 to oil reduces viscosity and increases volume")

base_oil = fluid("pr")
base_oil.addComponent("methane", 30.0, "mol%")
base_oil.addComponent("propane", 10.0, "mol%")
base_oil.addComponent("n-hexane", 20.0, "mol%")
base_oil.addComponent("n-decane", 40.0, "mol%")
base_oil.setMixingRule("classic")
base_oil.setMultiPhaseCheck(True)

print(f"\nBase oil: C1/C3/C6/C10 at T = 80°C")
print("\nCO2 Added | Swelling | Sat. Pressure")
print("[mol%]    | Factor   | [bara]")
print("-" * 40)

# Get reference volume at saturation
base_oil.setTemperature(80.0, "C")
psat_base = bubblepoint(base_oil)
base_oil.setPressure(psat_base, "bara")
TPflash(base_oil)
base_oil.initThermoProperties()
v_ref = base_oil.getVolume("m3")

for co2_pct in [0, 10, 20, 30]:
    swell_oil = fluid("pr")
    # Scale original composition
    scale = (100 - co2_pct) / 100
    swell_oil.addComponent("CO2", co2_pct, "mol%")
    swell_oil.addComponent("methane", 30.0 * scale, "mol%")
    swell_oil.addComponent("propane", 10.0 * scale, "mol%")
    swell_oil.addComponent("n-hexane", 20.0 * scale, "mol%")
    swell_oil.addComponent("n-decane", 40.0 * scale, "mol%")
    swell_oil.setMixingRule("classic")
    swell_oil.setMultiPhaseCheck(True)

    swell_oil.setTemperature(80.0, "C")
    psat_swell = bubblepoint(swell_oil)
    swell_oil.setPressure(psat_swell, "bara")
    TPflash(swell_oil)
    swell_oil.initThermoProperties()
    v_swell = swell_oil.getVolume("m3")

    swelling_factor = v_swell / v_ref
    print(f"{co2_pct:9} | {swelling_factor:8.4f} | {psat_swell:8.1f}")

# =============================================================================
# 7. VISCOSITY STUDY
# =============================================================================
print("\n7. VISCOSITY STUDY")
print("-" * 40)
print("Viscosity variation with pressure and temperature")

visc_oil = fluid("pr")
visc_oil.addComponent("methane", 30.0, "mol%")
visc_oil.addComponent("n-pentane", 20.0, "mol%")
visc_oil.addComponent("n-decane", 50.0, "mol%")
visc_oil.setMixingRule("classic")

print("\nOil viscosity at different conditions:")
print("\nT [°C] | P [bara] | Viscosity [cP]")
print("-" * 35)

for t, p in [(25, 50), (50, 50), (100, 50), (100, 100), (100, 200)]:
    visc_oil.setTemperature(t, "C")
    visc_oil.setPressure(p, "bara")
    TPflash(visc_oil)
    visc_oil.initThermoProperties()
    visc_oil.initPhysicalProperties("viscosity")

    mu = visc_oil.getViscosity("cP")
    print(f"{t:6} | {p:8} | {mu:.4f}")

# =============================================================================
# 8. SUMMARY
# =============================================================================
print("\n8. PVT EXPERIMENTS SUMMARY")
print("-" * 40)
print(
    """
Experiment          | Purpose
--------------------|----------------------------------------------
CME                 | Oil compressibility, relative volume, GOR
Differential        | Gas liberation, reservoir depletion behavior
Liberation          |
Separator Test      | Optimize surface separation, stock tank oil
Swelling Test       | EOR potential with gas injection (CO2, HC gas)
Viscosity Study     | Flow assurance, production optimization
"""
)

print("=" * 70)
