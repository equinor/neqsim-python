# -*- coding: utf-8 -*-
"""
Fluid Creation Tutorial
========================

This example provides comprehensive coverage of fluid creation methods
in NeqSim. Creating fluids correctly is the foundation for all
thermodynamic calculations.

Topics Covered:
    1. Creating fluids with different EoS
    2. Adding components by mole fraction, mass, and flow rate
    3. Pseudo-components and petroleum fractions
    4. Plus fractions (C7+, C10+, etc.)
    5. Pre-defined fluid types
    6. Copying and modifying fluids
    7. Multi-fluid mixing

@author: NeqSim Team
"""

from neqsim.thermo import fluid, fluid_df, TPflash

print("=" * 70)
print("FLUID CREATION TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. BASIC FLUID CREATION
# =============================================================================
print("\n1. BASIC FLUID CREATION")
print("-" * 40)

# Create an empty fluid with equation of state
gas = fluid("srk")  # Soave-Redlich-Kwong EoS

# Add components one by one
gas.addComponent("methane", 1.0)     # Default: mole fraction
gas.addComponent("ethane", 0.1)
gas.addComponent("propane", 0.05)
gas.setMixingRule("classic")

print("Created SRK fluid with:")
print("  Methane: 1.0 mol")
print("  Ethane: 0.1 mol")
print("  Propane: 0.05 mol")
print(f"Total moles: {gas.getTotalNumberOfMoles():.2f}")

# =============================================================================
# 2. DIFFERENT UNITS FOR COMPOSITION
# =============================================================================
print("\n2. SPECIFYING COMPOSITION WITH DIFFERENT UNITS")
print("-" * 40)

# Method A: Mole percent
gas_mol_pct = fluid("pr")
gas_mol_pct.addComponent("methane", 90.0, "mol%")
gas_mol_pct.addComponent("ethane", 7.0, "mol%")
gas_mol_pct.addComponent("propane", 3.0, "mol%")
gas_mol_pct.setMixingRule("classic")

print("A) Mole percent:")
print("   methane: 90 mol%, ethane: 7 mol%, propane: 3 mol%")

# Method B: Mass (kg)
gas_mass = fluid("pr")
gas_mass.addComponent("methane", 100.0, "kg")
gas_mass.addComponent("ethane", 20.0, "kg")
gas_mass.addComponent("propane", 10.0, "kg")
gas_mass.setMixingRule("classic")

print("\nB) Mass (kg):")
print("   methane: 100 kg, ethane: 20 kg, propane: 10 kg")

# Method C: Molar flow (mol/sec)
gas_flow = fluid("pr")
gas_flow.addComponent("methane", 1000.0, "mol/sec")
gas_flow.addComponent("ethane", 100.0, "mol/sec")
gas_flow.addComponent("propane", 50.0, "mol/sec")
gas_flow.setMixingRule("classic")

print("\nC) Molar flow:")
print("   methane: 1000 mol/s, ethane: 100 mol/s, propane: 50 mol/s")

# =============================================================================
# 3. CREATING FLUIDS FROM DATAFRAME
# =============================================================================
print("\n3. CREATING FLUIDS FROM DATAFRAME")
print("-" * 40)

import pandas as pd

# Define composition in a DataFrame
composition_data = {
    'ComponentName': ['nitrogen', 'CO2', 'methane', 'ethane', 'propane', 
                      'i-butane', 'n-butane', 'i-pentane', 'n-pentane'],
    'MolarComposition[-]': [0.02, 0.01, 0.85, 0.05, 0.03, 
                            0.01, 0.015, 0.005, 0.01]
}
df = pd.DataFrame(composition_data)

print("DataFrame composition:")
print(df.to_string(index=False))

# Create fluid from DataFrame
gas_df = fluid_df(df, lastIsPlusFraction=False)
gas_df.setMixingRule("classic")
gas_df.setTemperature(25.0, "C")
gas_df.setPressure(50.0, "bara")
TPflash(gas_df)

print(f"\nCreated fluid from DataFrame")
print(f"  Total molar flow: {gas_df.getTotalNumberOfMoles():.4f} mol")

# =============================================================================
# 4. PETROLEUM FRACTIONS AND PSEUDO-COMPONENTS
# =============================================================================
print("\n4. PETROLEUM FRACTIONS (PSEUDO-COMPONENTS)")
print("-" * 40)
print("For undefined components, specify molecular weight and density")

oil = fluid("pr")
oil.addComponent("methane", 30.0, "mol%")
oil.addComponent("n-hexane", 20.0, "mol%")

# Add a C10 pseudo-component with custom properties
oil.addComponent("C10", 25.0, "mol%")

# Add a heavier fraction manually
# Using addPlusFraction for C20+ pseudo-component
# Parameters: name, moles, molarMass (g/mol), density (kg/m³)
oil.addTBPfraction("C20", 25.0, 0.282, 850.0)  # M=282 g/mol, ρ=850 kg/m³

oil.setMixingRule("classic")
oil.setMultiPhaseCheck(True)

print("Created oil with pseudo-components:")
print("  Methane: 30 mol%")
print("  n-Hexane: 20 mol%")
print("  C10: 25 mol% (from database)")
print("  C20: 25 mol% (M=282, ρ=850)")

# =============================================================================
# 5. PLUS FRACTION CHARACTERIZATION
# =============================================================================
print("\n5. PLUS FRACTION CHARACTERIZATION")
print("-" * 40)
print("Heavy fractions (C7+) can be characterized into pseudo-components")

# Create oil with C7+ fraction
oil_plus = fluid("pr")
oil_plus.addComponent("nitrogen", 0.5, "mol%")
oil_plus.addComponent("CO2", 1.5, "mol%")
oil_plus.addComponent("methane", 45.0, "mol%")
oil_plus.addComponent("ethane", 7.0, "mol%")
oil_plus.addComponent("propane", 5.0, "mol%")
oil_plus.addComponent("n-butane", 3.0, "mol%")
oil_plus.addComponent("n-pentane", 3.0, "mol%")
oil_plus.addComponent("n-hexane", 3.0, "mol%")

# Add C7+ as plus fraction (32 mol%, MW=200 g/mol, density=800 kg/m³)
oil_plus.addPlusFraction("C7+", 32.0, 0.200, 800.0)

# Characterize the plus fraction into 6 pseudo-components
oil_plus.getCharacterization().setNumberOfPseudoComponents(6)
oil_plus.getCharacterization().characterisePlusFraction()

oil_plus.setMixingRule("classic")
oil_plus.setMultiPhaseCheck(True)

print("Original: C7+ = 32 mol%, MW=200 g/mol, ρ=800 kg/m³")
print("Characterized into 6 pseudo-components")

# =============================================================================
# 6. PRE-DEFINED FLUID TYPES
# =============================================================================
print("\n6. PRE-DEFINED FLUID TYPES")
print("-" * 40)

# Create predefined fluids using createfluid function
from neqsim.thermo import createfluid

# Dry gas
dry_gas = createfluid("dry gas")
print("Dry gas - typical pipeline quality natural gas")

# Rich gas
rich_gas = createfluid("rich gas")
print("Rich gas - NGL-rich natural gas")

# Black oil
black_oil = createfluid("black oil")
print("Black oil - typical black oil composition")

# Light oil
light_oil = createfluid("light oil")
print("Light oil - condensate-like composition")

print("\nAvailable predefined types: 'dry gas', 'rich gas', 'black oil', 'light oil'")

# =============================================================================
# 7. COPYING FLUIDS
# =============================================================================
print("\n7. COPYING AND CLONING FLUIDS")
print("-" * 40)

original = fluid("srk")
original.addComponent("methane", 90.0, "mol%")
original.addComponent("ethane", 10.0, "mol%")
original.setMixingRule("classic")
original.setTemperature(25.0, "C")
original.setPressure(50.0, "bara")

# Clone the fluid
cloned = original.clone()

# Modify the clone - original is unaffected
cloned.setTemperature(100.0, "C")
cloned.setPressure(100.0, "bara")

print(f"Original fluid: T = {original.getTemperature('C'):.1f}°C, P = {original.getPressure('bara'):.1f} bara")
print(f"Cloned fluid:   T = {cloned.getTemperature('C'):.1f}°C, P = {cloned.getPressure('bara'):.1f} bara")
print("(Changes to clone don't affect original)")

# =============================================================================
# 8. MIXING FLUIDS
# =============================================================================
print("\n8. MIXING FLUIDS")
print("-" * 40)
print("Combine multiple streams into one fluid")

# Stream 1: Lean gas
stream1 = fluid("pr")
stream1.addComponent("methane", 95.0, "mol%")
stream1.addComponent("ethane", 5.0, "mol%")
stream1.setMixingRule("classic")
stream1.setTotalFlowRate(1000.0, "mol/hr")

# Stream 2: Rich gas
stream2 = fluid("pr")
stream2.addComponent("methane", 70.0, "mol%")
stream2.addComponent("ethane", 15.0, "mol%")
stream2.addComponent("propane", 10.0, "mol%")
stream2.addComponent("n-butane", 5.0, "mol%")
stream2.setMixingRule("classic")
stream2.setTotalFlowRate(500.0, "mol/hr")

# Add stream2 to stream1 (mixing)
stream1.addFluid(stream2)

print("Stream 1 (lean gas): 1000 mol/hr (95% C1, 5% C2)")
print("Stream 2 (rich gas): 500 mol/hr (70% C1, 15% C2, 10% C3, 5% nC4)")
print(f"\nMixed stream total flow: {stream1.getTotalNumberOfMoles():.1f} mol")

# =============================================================================
# 9. AVAILABLE COMPONENTS
# =============================================================================
print("\n9. COMMONLY USED COMPONENTS")
print("-" * 40)
print("""
Category           | Component Names
-------------------|------------------------------------------------
Light gases        | nitrogen, oxygen, argon, helium, hydrogen, H2S
Inerts             | CO2, water
Hydrocarbons       | methane, ethane, propane, i-butane, n-butane,
                   | i-pentane, n-pentane, n-hexane, n-heptane,
                   | n-octane, n-nonane, n-decane, n-undecane, n-C12,
                   | benzene, toluene, cyclohexane
Glycols            | MEG, DEG, TEG (for CPA EoS)
Alcohols           | methanol, ethanol (for CPA EoS)
Pseudo-components  | C6, C7, C8, C9, C10, C11-C14, C15-C20 (from DB)

Note: For components not in database, use addTBPfraction() or
      addPlusFraction() with MW and density.
""")

# =============================================================================
# 10. ELECTROLYTE FLUIDS
# =============================================================================
print("\n10. ELECTROLYTE FLUIDS (BRINES)")
print("-" * 40)

brine = fluid("electrolyte")
brine.addComponent("water", 1.0, "kg")
brine.addComponent("Na+", 0.035, "mol")  # Sodium ion
brine.addComponent("Cl-", 0.035, "mol")  # Chloride ion
brine.setMixingRule("classic")

print("Created brine with NaCl:")
print("  Water: 1 kg")
print("  Na+: 0.035 mol")
print("  Cl-: 0.035 mol")
print("\nNote: Use 'electrolyte' EoS for ionic species")

print("\n" + "=" * 70)
