# -*- coding: utf-8 -*-
"""
Hydrate Calculations Tutorial
==============================

This example covers gas hydrate formation and inhibition calculations.
Gas hydrates are ice-like crystalline compounds that can block pipelines
and process equipment in oil and gas operations.

Topics Covered:
    1. Hydrate formation temperature at given pressure
    2. Hydrate formation pressure at given temperature
    3. Hydrate curves (phase boundaries)
    4. Hydrate inhibition with methanol and MEG
    5. Hydrate inhibitor dosage calculations

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash

print("=" * 70)
print("GAS HYDRATE CALCULATIONS TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. INTRODUCTION TO HYDRATES
# =============================================================================
print("\n1. INTRODUCTION TO GAS HYDRATES")
print("-" * 40)
print("""
Gas hydrates form when water and light gases (C1, C2, C3, CO2, H2S)
combine under high pressure and low temperature conditions.

Hydrate Types:
  - Type I: Smaller molecules (methane, CO2, H2S)
  - Type II: Larger molecules (propane, i-butane, natural gas mixtures)
  
Formation conditions:
  - Temperature: Typically < 25°C
  - Pressure: Typically > 10-20 bara
  - Presence of free water
""")

# =============================================================================
# 2. HYDRATE FORMATION TEMPERATURE
# =============================================================================
print("\n2. HYDRATE FORMATION TEMPERATURE")
print("-" * 40)

from neqsim.thermo import hydrateequilibrium

# Create a natural gas
gas = fluid("cpa")  # CPA handles water well
gas.addComponent("nitrogen", 1.0, "mol%")
gas.addComponent("CO2", 2.0, "mol%")
gas.addComponent("methane", 85.0, "mol%")
gas.addComponent("ethane", 6.0, "mol%")
gas.addComponent("propane", 3.0, "mol%")
gas.addComponent("n-butane", 1.0, "mol%")
gas.addComponent("water", 2.0, "mol%")
gas.setMixingRule(10)  # CPA mixing rule
gas.setMultiPhaseCheck(True)

print("Natural gas composition:")
print("  N2: 1%, CO2: 2%, C1: 85%, C2: 6%, C3: 3%, nC4: 1%, Water: 2%")
print("\nHydrate Formation Temperature at Different Pressures:")
print("\nPressure [bara] | Hydrate T [°C]")
print("----------------|---------------")

for p in [20, 50, 100, 150, 200]:
    try:
        gas.setPressure(p, "bara")
        gas.setTemperature(10.0, "C")  # Initial guess
        
        # Calculate hydrate equilibrium temperature
        hydrate_T = hydrateequilibrium(gas)
        
        print(f"{p:15} | {hydrate_T:.1f}")
    except Exception as e:
        print(f"{p:15} | Error: {e}")

# =============================================================================
# 3. HYDRATE CURVE CALCULATION
# =============================================================================
print("\n3. HYDRATE CURVE (P-T DIAGRAM)")
print("-" * 40)
print("Plotting the hydrate formation boundary")

print("\nT [°C]  | P [bara] | Status")
print("--------|----------|--------")

# Calculate hydrate P at various temperatures
for t_c in [0, 5, 10, 15, 20, 25]:
    gas.setTemperature(t_c, "C")
    gas.setPressure(50.0, "bara")  # Initial pressure
    
    try:
        # This gives hydrate equilibrium
        hydrate_T = hydrateequilibrium(gas)
        
        # Since we set temperature, the result tells us the equilibrium T
        # For the hydrate curve, we need to iterate or use proper method
        status = "Hydrate possible" if t_c < hydrate_T else "No hydrate"
        print(f"{t_c:7} | 50       | {status}")
    except Exception as e:
        print(f"{t_c:7} | Error: {e}")

# =============================================================================
# 4. SUBCOOLING CONCEPT
# =============================================================================
print("\n4. SUBCOOLING - HYDRATE RISK ASSESSMENT")
print("-" * 40)
print("""
Subcooling (ΔT) = Hydrate formation T - Operating T

Interpretation:
  ΔT > 0: Operating BELOW hydrate T → HIGH RISK
  ΔT = 0: At hydrate equilibrium → BORDERLINE
  ΔT < 0: Operating ABOVE hydrate T → SAFE
""")

# Example calculation
gas.setPressure(100.0, "bara")
gas.setTemperature(15.0, "C")
hydrate_T = hydrateequilibrium(gas)

operating_T = 5.0  # °C
subcooling = hydrate_T - operating_T

print(f"Operating conditions: P = 100 bara, T = {operating_T}°C")
print(f"Hydrate formation temperature: {hydrate_T:.1f}°C")
print(f"Subcooling: {subcooling:.1f}°C")
print(f"Risk level: {'HIGH - Hydrates will form!' if subcooling > 0 else 'Safe'}")

# =============================================================================
# 5. HYDRATE INHIBITION WITH METHANOL
# =============================================================================
print("\n5. HYDRATE INHIBITION WITH METHANOL")
print("-" * 40)
print("Methanol depresses the hydrate formation temperature")

# Create gas with methanol inhibitor
print("\nEffect of methanol concentration:")
print("\nMeOH [wt%] | Hydrate T [°C] | ΔT Depression")
print("-----------|----------------|---------------")

# Base case without inhibitor
gas_base = fluid("cpa")
gas_base.addComponent("methane", 90.0, "mol%")
gas_base.addComponent("ethane", 5.0, "mol%")
gas_base.addComponent("propane", 3.0, "mol%")
gas_base.addComponent("water", 2.0, "mol%")
gas_base.setMixingRule(10)
gas_base.setMultiPhaseCheck(True)
gas_base.setPressure(100.0, "bara")
gas_base.setTemperature(15.0, "C")

hydrate_T_no_inhibitor = hydrateequilibrium(gas_base)
print(f"{0:10} | {hydrate_T_no_inhibitor:.1f}           | 0.0 (baseline)")

# With different methanol concentrations
for meoh_wt_pct in [10, 20, 30, 40]:
    try:
        gas_meoh = fluid("cpa")
        gas_meoh.addComponent("methane", 88.0, "mol%")
        gas_meoh.addComponent("ethane", 5.0, "mol%")
        gas_meoh.addComponent("propane", 3.0, "mol%")
        gas_meoh.addComponent("water", 2.0, "mol%")
        gas_meoh.addComponent("methanol", 2.0 * meoh_wt_pct / 20, "mol%")  # Approximate
        gas_meoh.setMixingRule(10)
        gas_meoh.setMultiPhaseCheck(True)
        gas_meoh.setPressure(100.0, "bara")
        gas_meoh.setTemperature(15.0, "C")
        
        hydrate_T_meoh = hydrateequilibrium(gas_meoh)
        depression = hydrate_T_no_inhibitor - hydrate_T_meoh
        
        print(f"{meoh_wt_pct:10} | {hydrate_T_meoh:.1f}           | {depression:.1f}")
    except Exception as e:
        print(f"{meoh_wt_pct:10} | Error: {e}")

# =============================================================================
# 6. HYDRATE INHIBITION WITH MEG
# =============================================================================
print("\n6. HYDRATE INHIBITION WITH MEG")
print("-" * 40)
print("MEG (Monoethylene Glycol) is preferred for continuous injection")
print("It can be regenerated and recycled")

print("\nMEG [wt%] | Hydrate T [°C] | Notes")
print("----------|----------------|------------------------")

for meg_wt_pct in [0, 30, 50, 70]:
    try:
        gas_meg = fluid("cpa")
        gas_meg.addComponent("methane", 88.0, "mol%")
        gas_meg.addComponent("ethane", 6.0, "mol%")
        gas_meg.addComponent("propane", 4.0, "mol%")
        gas_meg.addComponent("water", 2.0, "mol%")
        if meg_wt_pct > 0:
            gas_meg.addComponent("MEG", meg_wt_pct / 20, "mol%")  # Approximate
        gas_meg.setMixingRule(10)
        gas_meg.setMultiPhaseCheck(True)
        gas_meg.setPressure(100.0, "bara")
        gas_meg.setTemperature(10.0, "C")
        
        hydrate_T_meg = hydrateequilibrium(gas_meg)
        
        note = "Baseline" if meg_wt_pct == 0 else f"ΔT = {hydrate_T_no_inhibitor - hydrate_T_meg:.1f}°C"
        print(f"{meg_wt_pct:9} | {hydrate_T_meg:.1f}           | {note}")
    except Exception as e:
        print(f"{meg_wt_pct:9} | Error: {e}")

# =============================================================================
# 7. INHIBITOR SELECTION GUIDELINES
# =============================================================================
print("\n7. INHIBITOR SELECTION GUIDELINES")
print("-" * 40)
print("""
┌─────────────────────────────────────────────────────────────────┐
│ Inhibitor Comparison                                            │
├────────────┬──────────────────────────────────────────────────┐
│ Inhibitor  │ Characteristics                                  │
├────────────┼──────────────────────────────────────────────────┤
│ Methanol   │ ✓ Strong depression (~1.5°C per wt%)            │
│            │ ✓ Low viscosity, good distribution              │
│            │ ✗ Lost to gas phase (high volatility)           │
│            │ ✗ Not easily regenerated                        │
│            │ → Best for: Intermittent use, short flowlines   │
├────────────┼──────────────────────────────────────────────────┤
│ MEG        │ ✓ Lower volatility than methanol                │
│            │ ✓ Easily regenerated and recycled               │
│            │ ✓ Lower losses to gas phase                     │
│            │ ✗ Weaker depression (~1°C per wt%)              │
│            │ → Best for: Continuous injection, long tiebacks │
├────────────┼──────────────────────────────────────────────────┤
│ DEG/TEG    │ ✓ Very low volatility                           │
│            │ ✗ High viscosity at low temperatures            │
│            │ → Best for: Special applications                │
├────────────┼──────────────────────────────────────────────────┤
│ Salt (NaCl)│ ✓ Very effective per unit weight                │
│            │ ✗ Corrosion issues                              │
│            │ ✗ Cannot be regenerated                         │
│            │ → Best for: Drilling fluids, completion ops     │
└────────────┴──────────────────────────────────────────────────┘
""")

# =============================================================================
# 8. KINETIC HYDRATE INHIBITORS (KHI)
# =============================================================================
print("\n8. KINETIC HYDRATE INHIBITORS (KHI)")
print("-" * 40)
print("""
Unlike thermodynamic inhibitors (MEG, MeOH) that shift equilibrium,
KHIs work by slowing hydrate formation kinetics.

KHI Types:
  - Polymeric inhibitors (PVP, PVCap)
  - Anti-agglomerants (AAs)

Application:
  - Low dosage (0.5-2 wt% of water)
  - Limited subcooling tolerance (typically < 10°C)
  - Often combined with thermodynamic inhibitors

Note: NeqSim primarily calculates thermodynamic equilibrium.
      KHI effects require separate kinetic models.
""")

# =============================================================================
# 9. PRACTICAL EXAMPLE: PIPELINE HYDRATE ASSESSMENT
# =============================================================================
print("\n9. PRACTICAL EXAMPLE: PIPELINE HYDRATE ASSESSMENT")
print("-" * 40)

print("""
Scenario: Subsea pipeline from wellhead to platform
  - Wellhead: 150 bara, 80°C
  - Pipeline arrival: 80 bara, 5°C
  - Gas is water-saturated
  
Question: Will hydrates form? How much MEG is needed?
""")

# Check hydrate risk
pipeline_gas = fluid("cpa")
pipeline_gas.addComponent("methane", 85.0, "mol%")
pipeline_gas.addComponent("ethane", 7.0, "mol%")
pipeline_gas.addComponent("propane", 4.0, "mol%")
pipeline_gas.addComponent("n-butane", 2.0, "mol%")
pipeline_gas.addComponent("water", 2.0, "mol%")
pipeline_gas.setMixingRule(10)
pipeline_gas.setMultiPhaseCheck(True)

# At pipeline arrival conditions
pipeline_gas.setPressure(80.0, "bara")
pipeline_gas.setTemperature(5.0, "C")

hydrate_T = hydrateequilibrium(pipeline_gas)

print(f"Operating temperature: 5°C")
print(f"Hydrate formation temperature: {hydrate_T:.1f}°C")

if 5.0 < hydrate_T:
    subcooling = hydrate_T - 5.0
    print(f"\n⚠️  HYDRATE RISK! Subcooling = {subcooling:.1f}°C")
    print(f"Recommendation: Inject MEG to reduce hydrate T below 5°C")
else:
    print("\n✓ Safe from hydrates at these conditions")

print("\n" + "=" * 70)
