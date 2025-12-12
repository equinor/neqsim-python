# -*- coding: utf-8 -*-
"""
Oil Viscosity Models and Tuning Tutorial
==========================================

This example demonstrates advanced viscosity modeling for oil systems in NeqSim,
including the LBC (Lohrenz-Bray-Clark) and Friction Theory models, and how to
tune their parameters to match laboratory data.

Topics Covered:
    1. Available viscosity models
    2. LBC model and its parameters
    3. Tuning LBC dense-fluid parameters
    4. Friction Theory model
    5. Tuning Friction Theory with TBP correction factor
    6. Model comparison and selection guidelines

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash
import neqsim.jneqsim as jneqsim

print("=" * 70)
print("OIL VISCOSITY MODELS AND TUNING TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. AVAILABLE VISCOSITY MODELS
# =============================================================================
print("\n1. AVAILABLE VISCOSITY MODELS")
print("-" * 40)
print("""
Model              | Keyword            | Best For
-------------------|--------------------|---------------------------------
LBC                | "LBC"              | General oil, reservoir fluids
Friction Theory    | "friction theory"  | Wide range, EoS-consistent
PFCT               | "PFCT"             | Petroleum fractions
PFCT Heavy Oil     | "PFCT-Heavy-Oil"   | Heavy oils, bitumen

The LBC model is based on corresponding states principle using critical
properties. Friction Theory links viscosity to EoS pressure terms,
providing thermodynamic consistency.
""")

# =============================================================================
# 2. BASIC VISCOSITY CALCULATION
# =============================================================================
print("\n2. BASIC VISCOSITY CALCULATION")
print("-" * 40)

# Create a medium oil
oil = fluid("srk")
oil.addComponent("methane", 10.0, "mol%")
oil.addComponent("n-pentane", 15.0, "mol%")
oil.addComponent("n-heptane", 25.0, "mol%")
oil.addComponent("n-decane", 30.0, "mol%")
oil.addComponent("n-C16", 20.0, "mol%")
oil.setMixingRule("classic")
oil.setMultiPhaseCheck(True)

# Set conditions
oil.setTemperature(50.0, "C")
oil.setPressure(100.0, "bara")
TPflash(oil)

print(f"Oil composition: C1: 10%, C5: 15%, C7: 25%, C10: 30%, C16: 20%")
print(f"Conditions: T = 50°C, P = 100 bara")

# Compare different viscosity models
print("\nViscosity with different models:")
print("\nModel              | Viscosity [cP]")
print("-------------------|----------------")

for model in ["LBC", "friction theory", "PFCT"]:
    try:
        if oil.hasPhaseType("oil"):
            oil.getPhase("oil").getPhysicalProperties().setViscosityModel(model)
            oil.initPhysicalProperties()
            visc = oil.getPhase("oil").getViscosity("cP")
            print(f"{model:18} | {visc:.4f}")
    except Exception as e:
        print(f"{model:18} | Error: {e}")

# =============================================================================
# 3. LBC MODEL EXPLANATION
# =============================================================================
print("\n3. LBC MODEL (LOHRENZ-BRAY-CLARK)")
print("-" * 40)
print("""
The LBC model calculates viscosity as:
    
    η = η* + η_dense / ξ_m
    
Where:
    η*      = Low-pressure gas viscosity contribution
    η_dense = Dense-fluid contribution (function of reduced density)
    ξ_m     = Mixture viscosity parameter

Dense-fluid contribution uses a polynomial:

    (η_dense * ξ_m + 10^-4)^0.25 = a0 + a1*ρr + a2*ρr² + a3*ρr³ + a4*ρr⁴
    
Default LBC parameters (a0 to a4):
    a0 = 0.10230
    a1 = 0.023364
    a2 = 0.058533
    a3 = -0.040758
    a4 = 0.0093324

These parameters can be tuned to match laboratory viscosity data.
""")

# =============================================================================
# 4. TUNING LBC MODEL PARAMETERS
# =============================================================================
print("\n4. TUNING LBC MODEL PARAMETERS")
print("-" * 40)
print("Adjusting dense-fluid polynomial coefficients to match lab data")

# Create oil system
tuning_oil = fluid("srk")
tuning_oil.addComponent("n-heptane", 30.0, "mol%")
tuning_oil.addComponent("n-decane", 40.0, "mol%")
tuning_oil.addTBPfraction("C16", 30.0, 0.22, 830.0)
tuning_oil.setMixingRule("classic")

tuning_oil.setTemperature(50.0, "C")
tuning_oil.setPressure(150.0, "bara")
TPflash(tuning_oil)
tuning_oil.initThermoProperties()

# Set LBC model and get default viscosity
if tuning_oil.hasPhaseType("oil"):
    tuning_oil.getPhase("oil").getPhysicalProperties().setViscosityModel("LBC")
    tuning_oil.initPhysicalProperties()
    default_visc = tuning_oil.getPhase("oil").getViscosity("cP")
    
    print(f"\nDefault LBC viscosity: {default_visc:.4f} cP")
    
    # Suppose lab measurement is 2.5 cP - we need to tune
    lab_viscosity = 2.5
    print(f"Laboratory measurement: {lab_viscosity:.4f} cP")
    
    # Method 1: Set all five parameters at once
    # Increasing coefficients generally increases viscosity
    # Default: [0.10230, 0.023364, 0.058533, -0.040758, 0.0093324]
    tuned_params = [0.15, 0.04, 0.08, -0.03, 0.015]  # Increased values
    
    tuning_oil.getPhase("oil").getPhysicalProperties().setLbcParameters(tuned_params)
    tuning_oil.initPhysicalProperties()
    tuned_visc_1 = tuning_oil.getPhase("oil").getViscosity("cP")
    
    print(f"\nTuned viscosity (all params): {tuned_visc_1:.4f} cP")
    
    # Method 2: Adjust individual parameter
    # Parameter indices: a0=0, a1=1, a2=2, a3=3, a4=4
    # a0 (index 0) has most influence at low density
    # a4 (index 4) has most influence at high density
    
    tuning_oil.getPhase("oil").getPhysicalProperties().setLbcParameter(2, 0.10)
    tuning_oil.initPhysicalProperties()
    tuned_visc_2 = tuning_oil.getPhase("oil").getViscosity("cP")
    
    print(f"Further adjusted (a2=0.10): {tuned_visc_2:.4f} cP")

print("""
LBC Tuning Guidelines:
----------------------
• a0 (index 0): Baseline offset - increase for higher overall viscosity
• a1 (index 1): Linear density term - affects moderate densities
• a2 (index 2): Quadratic term - significant for liquid viscosity
• a3 (index 3): Cubic term - fine-tuning at high density
• a4 (index 4): Quartic term - extreme density behavior
""")

# =============================================================================
# 5. FRICTION THEORY MODEL
# =============================================================================
print("\n5. FRICTION THEORY MODEL")
print("-" * 40)
print("""
Friction Theory (f-theory) links viscosity to EoS pressure terms:

    η = η0 + ηf
    
Where:
    η0 = Dilute gas viscosity (Chung correlation)
    ηf = Friction contribution from EoS

The friction term is proportional to attractive and repulsive pressure
terms from the equation of state, providing thermodynamic consistency.

Advantages:
    ✓ Consistent with phase equilibrium calculations
    ✓ Better extrapolation behavior
    ✓ Works well for wide T/P ranges
""")

# =============================================================================
# 6. TUNING FRICTION THEORY - TBP CORRECTION FACTOR
# =============================================================================
print("\n6. TUNING FRICTION THEORY - TBP CORRECTION FACTOR")
print("-" * 40)
print("For TBP (True Boiling Point) fractions, a correction factor can be applied")

# Create oil with TBP fractions
ft_oil = fluid("srk")
ft_oil.addComponent("methane", 5.0, "mol%")
ft_oil.addComponent("n-heptane", 20.0, "mol%")
ft_oil.addTBPfraction("C12", 25.0, 0.17, 780.0)
ft_oil.addTBPfraction("C18", 30.0, 0.25, 820.0)
ft_oil.addTBPfraction("C25", 20.0, 0.35, 860.0)
ft_oil.setMixingRule("classic")

ft_oil.setTemperature(60.0, "C")
ft_oil.setPressure(100.0, "bara")
TPflash(ft_oil)
ft_oil.initThermoProperties()

if ft_oil.hasPhaseType("oil"):
    # Set friction theory model
    ft_oil.getPhase("oil").getPhysicalProperties().setViscosityModel("friction theory")
    ft_oil.initPhysicalProperties()
    
    # Get default viscosity
    default_ft_visc = ft_oil.getPhase("oil").getViscosity("cP")
    print(f"\nDefault Friction Theory viscosity: {default_ft_visc:.4f} cP")
    
    # Apply TBP viscosity correction factor
    # Factor > 1.0 increases viscosity
    # Factor < 1.0 decreases viscosity
    visc_model = ft_oil.getPhase("oil").getPhysicalProperties().getViscosityModel()
    
    # Access the FrictionTheoryViscosityMethod directly
    print("\nApplying TBP correction factors:")
    print("\nCorrection Factor | Viscosity [cP]")
    print("------------------|----------------")
    
    for correction in [0.8, 1.0, 1.2, 1.5, 2.0]:
        try:
            # Set the TBP correction factor
            visc_model.setTBPviscosityCorrection(correction)
            ft_oil.initPhysicalProperties()
            
            corrected_visc = ft_oil.getPhase("oil").getViscosity("cP")
            print(f"{correction:17.1f} | {corrected_visc:.4f}")
        except Exception as e:
            print(f"{correction:17.1f} | Error: {e}")
    
    # Reset to default
    visc_model.setTBPviscosityCorrection(1.0)

print("""
Friction Theory Tuning Guidelines:
----------------------------------
• TBP Correction Factor:
  - Default = 1.0 (no correction)
  - > 1.0: Increases viscosity for heavy fractions
  - < 1.0: Decreases viscosity
  
• Use when TBP fractions give incorrect viscosity predictions
• Tune to match laboratory viscosity at one T/P condition
• Model will extrapolate to other conditions
""")

# =============================================================================
# 7. ADVANCED: TUNING WITH EXPERIMENTAL DATA
# =============================================================================
print("\n7. ADVANCED: TUNING WITH EXPERIMENTAL DATA")
print("-" * 40)
print("Workflow for matching lab measurements")

# Example experimental data
exp_data = [
    {"T_C": 25, "P_bara": 1, "visc_cP": 3.5},
    {"T_C": 50, "P_bara": 50, "visc_cP": 1.8},
    {"T_C": 80, "P_bara": 100, "visc_cP": 0.9},
]

print("\nExample experimental viscosity data:")
print("T [°C] | P [bara] | Viscosity [cP]")
print("-------|----------|---------------")
for pt in exp_data:
    print(f"{pt['T_C']:6} | {pt['P_bara']:8} | {pt['visc_cP']:.2f}")

print("""
Tuning Workflow:
----------------
1. Create fluid with accurate composition
2. Select viscosity model (LBC or Friction Theory)
3. Calculate viscosity at each experimental condition
4. Compare with experimental data
5. Adjust parameters:
   - LBC: Tune a0-a4 dense-fluid parameters
   - Friction Theory: Tune TBP correction factor
6. Iterate until deviation is acceptable
7. Validate at conditions not used for tuning

For automatic optimization, use NeqSim's parameter fitting capabilities
with the ViscosityFunction class in PVT simulation.
""")

# =============================================================================
# 8. MODEL COMPARISON AT DIFFERENT CONDITIONS
# =============================================================================
print("\n8. MODEL COMPARISON AT DIFFERENT CONDITIONS")
print("-" * 40)

comp_oil = fluid("srk")
comp_oil.addComponent("n-heptane", 30.0, "mol%")
comp_oil.addComponent("n-decane", 40.0, "mol%")
comp_oil.addComponent("n-C16", 30.0, "mol%")
comp_oil.setMixingRule("classic")
comp_oil.setMultiPhaseCheck(True)

print("Viscosity comparison: LBC vs Friction Theory")
print("Oil: C7 30%, C10 40%, C16 30%")
print("\nT [°C] | P [bara] | LBC [cP]  | F-Theory [cP] | Ratio")
print("-------|----------|-----------|---------------|-------")

conditions = [
    (25, 1),
    (50, 50),
    (80, 100),
    (100, 200),
    (120, 300),
]

for t_c, p_bara in conditions:
    comp_oil.setTemperature(t_c, "C")
    comp_oil.setPressure(p_bara, "bara")
    TPflash(comp_oil)
    comp_oil.initThermoProperties()
    
    if comp_oil.hasPhaseType("oil"):
        # LBC
        comp_oil.getPhase("oil").getPhysicalProperties().setViscosityModel("LBC")
        comp_oil.initPhysicalProperties()
        lbc_visc = comp_oil.getPhase("oil").getViscosity("cP")
        
        # Friction Theory
        comp_oil.getPhase("oil").getPhysicalProperties().setViscosityModel("friction theory")
        comp_oil.initPhysicalProperties()
        ft_visc = comp_oil.getPhase("oil").getViscosity("cP")
        
        ratio = lbc_visc / ft_visc if ft_visc > 0 else 0
        print(f"{t_c:6} | {p_bara:8} | {lbc_visc:9.4f} | {ft_visc:13.4f} | {ratio:.3f}")

# =============================================================================
# 9. HEAVY OIL CONSIDERATIONS
# =============================================================================
print("\n9. HEAVY OIL CONSIDERATIONS")
print("-" * 40)
print("""
For heavy oils (API < 20°, viscosity > 100 cP), consider:

1. Use PFCT-Heavy-Oil model:
   oil.getPhase("oil").getPhysicalProperties().setViscosityModel("PFCT-Heavy-Oil")

2. LBC may underpredict - needs significant parameter tuning

3. Friction Theory typically needs TBP correction > 1.0 for heavy ends

4. Temperature sensitivity is critical - ensure accurate measurements

5. Consider using Pedersen corresponding states for very heavy systems
""")

# =============================================================================
# 10. SUMMARY
# =============================================================================
print("\n10. SUMMARY: MODEL SELECTION GUIDELINES")
print("-" * 40)
print("""
┌────────────────────┬──────────────────────────────────────────┐
│ Oil Type           │ Recommended Model & Notes                │
├────────────────────┼──────────────────────────────────────────┤
│ Light oil          │ LBC or Friction Theory                   │
│ (API > 35°)        │ Default parameters often sufficient      │
├────────────────────┼──────────────────────────────────────────┤
│ Medium oil         │ LBC with tuned parameters                │
│ (20° < API < 35°)  │ or Friction Theory with TBP correction   │
├────────────────────┼──────────────────────────────────────────┤
│ Heavy oil          │ PFCT-Heavy-Oil or Friction Theory        │
│ (10° < API < 20°)  │ TBP correction factor 1.5-2.0            │
├────────────────────┼──────────────────────────────────────────┤
│ Extra-heavy        │ Specialized correlations                 │
│ (API < 10°)        │ May require custom viscosity data        │
└────────────────────┴──────────────────────────────────────────┘
""")

print("=" * 70)
