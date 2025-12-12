# -*- coding: utf-8 -*-
"""
Equation of State Comparison Tutorial
======================================

This example compares different equations of state (EoS) available in NeqSim.
The choice of EoS significantly affects calculated properties, especially
near critical conditions or for polar/associating compounds.

Equations of State Covered:
    - SRK: Soave-Redlich-Kwong (general purpose, hydrocarbons)
    - PR: Peng-Robinson (similar to SRK, often better liquid density)
    - CPA: Cubic-Plus-Association (water, alcohols, glycols)
    - GERG-2008: Reference EoS for natural gas (very accurate)
    - PR-Peneloux: Peng-Robinson with volume translation

@author: NeqSim Team
"""

from neqsim.thermo import fluid, TPflash

print("=" * 70)
print("EQUATION OF STATE COMPARISON TUTORIAL")
print("=" * 70)

# =============================================================================
# 1. AVAILABLE EQUATIONS OF STATE
# =============================================================================
print("\n1. AVAILABLE EQUATIONS OF STATE")
print("-" * 40)

eos_list = """
EoS Name        | Description
----------------|--------------------------------------------------
'srk'           | Soave-Redlich-Kwong - general purpose
'pr'            | Peng-Robinson - good for liquid density
'pr-peneloux'   | Peng-Robinson with Peneloux volume correction
'cpa'           | CPA-SRK - polar & associating compounds
'cpa-pr'        | CPA-Peng-Robinson
'gerg-2008'     | GERG-2008 - reference EoS for natural gas
'span-wagner'   | Span-Wagner - reference EoS for CO2
'electrolyte'   | For brine/salt solutions
'nrtl'          | Activity coefficient model
'unifac'        | UNIFAC group contribution model
"""
print(eos_list)

# =============================================================================
# 2. COMPARE EoS FOR NATURAL GAS
# =============================================================================
print("\n2. COMPARING EoS FOR NATURAL GAS")
print("-" * 40)

# Define composition
def create_natural_gas(eos_name):
    """Create a natural gas mixture with specified EoS."""
    gas = fluid(eos_name)
    gas.addComponent("nitrogen", 2.0, "mol%")
    gas.addComponent("CO2", 1.0, "mol%")
    gas.addComponent("methane", 88.0, "mol%")
    gas.addComponent("ethane", 5.0, "mol%")
    gas.addComponent("propane", 2.5, "mol%")
    gas.addComponent("i-butane", 0.5, "mol%")
    gas.addComponent("n-butane", 0.5, "mol%")
    gas.addComponent("n-pentane", 0.5, "mol%")
    gas.setMixingRule("classic")
    return gas

# Conditions
temp_c = 25.0
pressure_bara = 100.0

print(f"Conditions: T = {temp_c}°C, P = {pressure_bara} bara")
print("\nEoS         | Z-factor  | Density   | Cp        | Sound Speed")
print("            |    [-]    | [kg/m³]   | [J/mol·K] | [m/s]")
print("-" * 65)

for eos in ["srk", "pr", "gerg-2008"]:
    try:
        gas = create_natural_gas(eos)
        gas.setTemperature(temp_c, "C")
        gas.setPressure(pressure_bara, "bara")
        TPflash(gas)
        gas.initThermoProperties()
        gas.initPhysicalProperties()
        
        z = gas.getZ()
        rho = gas.getDensity("kg/m3")
        cp = gas.getCp("J/molK")
        
        if gas.hasPhaseType("gas"):
            sos = gas.getPhase("gas").getSoundSpeed()
        else:
            sos = gas.getPhase(0).getSoundSpeed()
        
        print(f"{eos:11} | {z:9.5f} | {rho:9.2f} | {cp:9.2f} | {sos:8.1f}")
    except Exception as e:
        print(f"{eos:11} | Error: {e}")

# =============================================================================
# 3. CPA FOR WATER-CONTAINING SYSTEMS
# =============================================================================
print("\n3. CPA vs SRK FOR WATER-CONTAINING SYSTEMS")
print("-" * 40)
print("CPA handles hydrogen bonding (association) in water and alcohols")

def create_wet_gas(eos_name):
    """Create a wet gas mixture with specified EoS."""
    if eos_name == "cpa":
        gas = fluid("cpa")
        gas.setMixingRule(10)  # CPA mixing rule
    else:
        gas = fluid(eos_name)
        gas.setMixingRule("classic")
    
    gas.addComponent("methane", 90.0, "mol%")
    gas.addComponent("ethane", 5.0, "mol%")
    gas.addComponent("water", 5.0, "mol%")
    gas.setMultiPhaseCheck(True)
    return gas

print(f"\nConditions: T = 25°C, P = 50 bara")
print("Wet natural gas with 5 mol% water")
print("\nEoS    | # Phases | Gas Density | Water in Gas Phase")
print("       |          | [kg/m³]     | [mol fraction]")
print("-" * 55)

for eos in ["srk", "cpa"]:
    try:
        gas = create_wet_gas(eos)
        gas.setTemperature(25.0, "C")
        gas.setPressure(50.0, "bara")
        TPflash(gas)
        gas.initThermoProperties()
        
        n_phases = gas.getNumberOfPhases()
        
        if gas.hasPhaseType("gas"):
            gas_phase = gas.getPhase("gas")
            rho = gas_phase.getDensity("kg/m3")
            # Get water mole fraction in gas phase
            water_idx = gas.getPhase(0).getComponent("water").getComponentNumber()
            water_in_gas = gas_phase.getComponent(water_idx).getx()
        else:
            rho = gas.getPhase(0).getDensity("kg/m3")
            water_in_gas = 0.0
        
        print(f"{eos:6} | {n_phases:8} | {rho:11.2f} | {water_in_gas:.6f}")
    except Exception as e:
        print(f"{eos:6} | Error: {e}")

# =============================================================================
# 4. LIQUID DENSITY COMPARISON
# =============================================================================
print("\n4. LIQUID DENSITY COMPARISON")
print("-" * 40)
print("Comparing SRK vs PR for liquid n-heptane")
print("Experimental density at 25°C, 1 atm: ~684 kg/m³")

for eos in ["srk", "pr"]:
    heptane = fluid(eos)
    heptane.addComponent("n-heptane", 1.0)
    heptane.setMixingRule("classic")
    heptane.setTemperature(25.0, "C")
    heptane.setPressure(1.01325, "bara")
    TPflash(heptane)
    heptane.initThermoProperties()
    
    rho = heptane.getDensity("kg/m3")
    print(f"{eos.upper()}: {rho:.1f} kg/m³")

# =============================================================================
# 5. HIGH-PRESSURE CO2
# =============================================================================
print("\n5. HIGH-PRESSURE CO2")
print("-" * 40)
print("CO2 near critical point (Tc=31°C, Pc=73.8 bar)")
print("Span-Wagner is the reference EoS for CO2")

print(f"\nConditions: T = 35°C, P = 80 bara (supercritical)")
print("\nEoS           | Density [kg/m³] | Z-factor")
print("-" * 45)

for eos in ["srk", "pr", "span-wagner"]:
    try:
        co2 = fluid(eos)
        co2.addComponent("CO2", 1.0)
        if eos not in ["span-wagner"]:
            co2.setMixingRule("classic")
        co2.setTemperature(35.0, "C")
        co2.setPressure(80.0, "bara")
        TPflash(co2)
        co2.initThermoProperties()
        
        rho = co2.getDensity("kg/m3")
        z = co2.getZ()
        print(f"{eos:13} | {rho:15.2f} | {z:.5f}")
    except Exception as e:
        print(f"{eos:13} | Error: {e}")

# =============================================================================
# 6. GUIDELINES FOR EoS SELECTION
# =============================================================================
print("\n6. GUIDELINES FOR EoS SELECTION")
print("-" * 40)
print("""
Application                          | Recommended EoS
-------------------------------------|----------------------
Natural gas properties               | GERG-2008 (most accurate)
                                     | SRK or PR (faster)
                                     |
Oil & gas upstream                   | SRK or PR with kij
                                     |
Glycol dehydration                   | CPA-SRK
Water content in gas                 | CPA-SRK or CPA-PR
                                     |
CO2 capture/storage                  | Span-Wagner (pure CO2)
                                     | SRK/PR with kij (mixtures)
                                     |
Refinery / petrochemical             | SRK or PR with kij
                                     |
Liquefied Natural Gas (LNG)          | GERG-2008 or PR
                                     |
Gas hydrates                         | CPA with hydrate model
                                     |
Electrolyte solutions (brine)        | Electrolyte-CPA
""")
print("=" * 70)
