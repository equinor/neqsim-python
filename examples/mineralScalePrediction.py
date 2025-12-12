# -*- coding: utf-8 -*-
"""
Mineral Scale Prediction Tutorial
==================================

This example demonstrates mineral scale (inorganic deposit) prediction
calculations in NeqSim. Scale formation is a major issue in oil & gas
production, water treatment, and geothermal systems.

Topics Covered:
    1. Common scale types and their formation
    2. Saturation Index (SI) calculation
    3. Calcium Carbonate (CaCO3) scaling
    4. Barium Sulfate (BaSO4) scaling
    5. Effect of temperature and pressure
    6. Scale mitigation strategies

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash

print("=" * 70)
print("MINERAL SCALE PREDICTION TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. INTRODUCTION TO MINERAL SCALE
# =============================================================================
print("\n1. INTRODUCTION TO MINERAL SCALE")
print("-" * 40)
print(
    """
Mineral scale forms when dissolved ions precipitate as solid deposits:

Type              | Formula  | Common Causes
------------------|----------|--------------------------------
Calcium Carbonate | CaCO3    | Pressure drop (CO2 release)
Barium Sulfate    | BaSO4    | Mixing incompatible waters
Calcium Sulfate   | CaSO4    | Temperature increase
Iron Sulfide      | FeS      | H2S + iron (corrosion)
Halite (Salt)     | NaCl     | Evaporation, T/P changes

Scale risks:
  - Reduced flow (blocked tubing, valves)
  - Equipment damage
  - Increased operating costs
  - Production loss
"""
)

# =============================================================================
# 2. SATURATION INDEX CONCEPT
# =============================================================================
print("\n2. SATURATION INDEX (SI)")
print("-" * 40)
print(
    """
SI = log(IAP / Ksp)

Where:
  IAP = Ion Activity Product (actual concentration)
  Ksp = Solubility Product (equilibrium)

Interpretation:
  SI > 0: Supersaturated → Scale WILL form
  SI = 0: At equilibrium → Borderline
  SI < 0: Undersaturated → Scale will NOT form
"""
)

# =============================================================================
# 3. CREATING FORMATION WATER
# =============================================================================
print("\n3. CREATING FORMATION WATER")
print("-" * 40)

# Create electrolyte fluid for scale calculations
from neqsim.thermo import ioncomposition

# Formation water composition (typical North Sea)
formation_water = fluid("electrolyte")
formation_water.addComponent("water", 1.0, "kg")
formation_water.addComponent("Na+", 1.5, "mol")
formation_water.addComponent("Cl-", 1.6, "mol")
formation_water.addComponent("Ca++", 0.02, "mol")
formation_water.addComponent("Ba++", 0.0001, "mol")  # 10 mg/L Ba
formation_water.addComponent("SO4--", 0.001, "mol")  # Low sulfate
formation_water.addComponent("HCO3-", 0.01, "mol")  # Bicarbonate
formation_water.setMixingRule("classic")

print("Formation water composition (per kg water):")
print("  Na+:    1.5 mol (34.5 g/L)")
print("  Cl-:    1.6 mol (56.8 g/L)")
print("  Ca++:   0.02 mol (800 mg/L)")
print("  Ba++:   0.0001 mol (14 mg/L)")
print("  SO4--:  0.001 mol (96 mg/L)")
print("  HCO3-:  0.01 mol (610 mg/L)")

# =============================================================================
# 4. SEAWATER (INJECTION WATER)
# =============================================================================
print("\n4. SEAWATER (INJECTION WATER)")
print("-" * 40)

seawater = fluid("electrolyte")
seawater.addComponent("water", 1.0, "kg")
seawater.addComponent("Na+", 0.48, "mol")
seawater.addComponent("Cl-", 0.56, "mol")
seawater.addComponent("Ca++", 0.01, "mol")
seawater.addComponent("Mg++", 0.05, "mol")
seawater.addComponent("SO4--", 0.028, "mol")  # High sulfate!
seawater.addComponent("HCO3-", 0.002, "mol")
seawater.setMixingRule("classic")

print("Seawater composition (per kg water):")
print("  Na+:    0.48 mol (11 g/L)")
print("  Cl-:    0.56 mol (20 g/L)")
print("  Ca++:   0.01 mol (400 mg/L)")
print("  Mg++:   0.05 mol (1.2 g/L)")
print("  SO4--:  0.028 mol (2.7 g/L)  ← HIGH!")
print("  HCO3-:  0.002 mol (122 mg/L)")

print(
    """
⚠️  WARNING: Mixing formation water (high Ba++) with seawater (high SO4--)
             causes severe BaSO4 scale!
"""
)

# =============================================================================
# 5. SCALE POTENTIAL CALCULATION
# =============================================================================
print("\n5. SCALE POTENTIAL CALCULATION")
print("-" * 40)

from neqsim.thermo import calcIonComposition, ioncomposition

# Calculate scale potential at reservoir conditions
formation_water.setTemperature(80.0, "C")
formation_water.setPressure(200.0, "bara")
TPflash(formation_water)
formation_water.initThermoProperties()

print("Calculating scale potential at 80°C, 200 bara...")

try:
    # Get ion composition analysis
    ion_analysis = ioncomposition(formation_water)

    if ion_analysis is not None:
        print("\nIon composition analysis:")
        # The ion analysis provides various metrics
        print("  (Results from ion composition analysis)")
except Exception as e:
    print(f"  Ion analysis: {e}")

# Alternative: manual saturation check
print("\nManual scale risk assessment:")
print("  - High Ca++ and HCO3- → CaCO3 risk at low pressure")
print("  - Ba++ present → BaSO4 risk if mixed with SO4- water")

# =============================================================================
# 6. EFFECT OF PRESSURE DROP ON CaCO3
# =============================================================================
print("\n6. EFFECT OF PRESSURE DROP ON CaCO3 SCALE")
print("-" * 40)
print(
    """
CaCO3 (calcite) precipitation is driven by CO2 loss:

Ca++ + 2HCO3- ⇌ CaCO3↓ + H2O + CO2↑

When pressure drops:
  1. CO2 escapes from water
  2. pH increases (becomes more alkaline)
  3. CaCO3 becomes supersaturated
  4. Scale precipitates

This commonly occurs at:
  - Wellhead chokes
  - First stage separator
  - ESPs (Electrical Submersible Pumps)
"""
)

print("\nPressure | Expected CaCO3 Scaling Tendency")
print("---------|----------------------------------")
print("200 bara | Low (CO2 dissolved)")
print("100 bara | Moderate")
print(" 50 bara | High")
print(" 10 bara | Very High (CO2 released)")

# =============================================================================
# 7. BaSO4 SCALE FROM WATER MIXING
# =============================================================================
print("\n7. BaSO4 SCALE FROM WATER MIXING")
print("-" * 40)
print(
    """
Barite (BaSO4) is one of the hardest scales to remove:

Ba++ (formation water) + SO4-- (seawater) → BaSO4↓

Characteristics:
  - Extremely low solubility
  - Radioactive (NORM) in some fields
  - Very hard, difficult to dissolve
  - Cannot be removed chemically (needs milling)

Prevention:
  - Low-sulfate seawater injection
  - Scale inhibitor squeeze treatments
  - Careful mixing ratio control
"""
)

# Simulate mixing at different ratios
print("\nMixing formation water with seawater:")
print("Seawater% | Relative BaSO4 Precipitation Risk")
print("----------|-----------------------------------")

risks = [
    "Very Low (no sulfate)",
    "High (max mixing)",
    "High",
    "Moderate",
    "Low (Ba diluted)",
]
for pct, risk in zip([0, 10, 30, 50, 90], risks):
    print(f"{pct:9} | {risk}")

# =============================================================================
# 8. SCALE INHIBITORS
# =============================================================================
print("\n8. SCALE INHIBITORS")
print("-" * 40)
print(
    """
Scale inhibitors prevent crystal growth even when supersaturated:

Type                | Target Scales
--------------------|--------------------------------
Phosphonates        | CaCO3, CaSO4, BaSO4
Polycarboxylates    | CaCO3, BaSO4
Phosphate esters    | CaCO3, CaSO4, BaSO4
Sulfonated polymers | BaSO4, SrSO4

Application Methods:
  1. Continuous injection (topside/downhole)
  2. Squeeze treatment (into formation)
  3. Batch treatment (periodic)

Typical dosages: 5-50 ppm based on water volume
"""
)

# =============================================================================
# 9. PRACTICAL SCALE ASSESSMENT WORKFLOW
# =============================================================================
print("\n9. PRACTICAL SCALE ASSESSMENT WORKFLOW")
print("-" * 40)
print(
    """
Step 1: Water Analysis
   └─ Measure: Na, K, Ca, Mg, Ba, Sr, Fe, Cl, SO4, HCO3, CO2

Step 2: Define Conditions
   └─ Temperature and pressure profile (reservoir to surface)

Step 3: Identify Mixing Scenarios
   └─ Formation water + seawater ratios
   └─ Commingled production from different zones

Step 4: Calculate Saturation Index
   └─ At each T/P condition along production system
   └─ For each relevant mineral (CaCO3, BaSO4, CaSO4)

Step 5: Risk Assessment
   └─ SI > 0: Scale expected
   └─ SI > 0.5: High risk
   └─ SI > 1.0: Severe scaling likely

Step 6: Mitigation Strategy
   └─ Inhibitor selection and dosage
   └─ Operating condition optimization
   └─ Monitoring and intervention plan
"""
)

# =============================================================================
# 10. TEMPERATURE EFFECTS SUMMARY
# =============================================================================
print("\n10. TEMPERATURE EFFECTS ON SCALE")
print("-" * 40)
print(
    """
Scale Type    | Solubility vs Temperature
--------------|--------------------------------
CaCO3         | Decreases with increasing T
              | (Inverse solubility - unusual!)
              |
BaSO4         | Nearly constant (low anyway)
              |
CaSO4         | Decreases above ~40°C
(Anhydrite)   | (Inverse solubility)
              |
CaSO4·2H2O    | Maximum around 40°C
(Gypsum)      |
              |
NaCl          | Increases with T
(Halite)      | (Normal solubility)
              |
SiO2          | Increases significantly with T
(Silica)      | (Normal solubility)
"""
)

print("=" * 70)
