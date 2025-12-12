"""
Example: Using ProcessBuilder with JSON/YAML Configuration

This example demonstrates how to build process simulations from 
configuration files, making it easy to separate process topology 
from code and enable configuration-driven design.
"""

from neqsim.thermo import fluid
from neqsim.process import ProcessBuilder

# =============================================================================
# Example 1: Using a Python dictionary configuration
# =============================================================================

# Create the fluid
feed = fluid('srk')
feed.addComponent('methane', 0.9)
feed.addComponent('ethane', 0.1)
feed.setTemperature(30.0, 'C')
feed.setPressure(50.0, 'bara')

# Define process configuration as a dictionary
config = {
    'name': 'Compression Train',
    'equipment': [
        {
            'type': 'stream',
            'name': 'inlet',
            'fluid': 'feed',
            'flow_rate': 10.0,
            'flow_unit': 'MSm3/day'
        },
        {
            'type': 'separator',
            'name': 'inlet_separator',
            'inlet': 'inlet'
        },
        {
            'type': 'compressor',
            'name': 'stage1_compressor',
            'inlet': 'inlet_separator',
            'pressure': 100.0,
            'efficiency': 0.75
        },
        {
            'type': 'cooler',
            'name': 'intercooler',
            'inlet': 'stage1_compressor',
            'temperature': 303.15  # 30°C in Kelvin
        },
        {
            'type': 'compressor',
            'name': 'stage2_compressor',
            'inlet': 'intercooler',
            'pressure': 200.0,
            'efficiency': 0.75
        }
    ]
}

# Build and run the process from config
process = ProcessBuilder.from_dict(config, fluids={'feed': feed}).run()

# Access results
print("=== Compression Train Results ===")
print(f"Stage 1 outlet pressure: {process.get('stage1_compressor').getOutletStream().getPressure():.1f} bara")
print(f"Stage 1 power: {process.get('stage1_compressor').getPower()/1e3:.1f} kW")
print(f"Stage 2 outlet pressure: {process.get('stage2_compressor').getOutletStream().getPressure():.1f} bara")
print(f"Stage 2 power: {process.get('stage2_compressor').getPower()/1e3:.1f} kW")
print(f"Total power: {(process.get('stage1_compressor').getPower() + process.get('stage2_compressor').getPower())/1e3:.1f} kW")


# =============================================================================
# Example 2: Loading from a JSON file
# =============================================================================

import json
import tempfile
import os

# Create a temporary JSON config file
json_config = {
    'name': 'Simple Separator Process',
    'equipment': [
        {'type': 'stream', 'name': 'well_stream', 'fluid': 'reservoir_fluid'},
        {'type': 'heater', 'name': 'heater', 'inlet': 'well_stream', 'temperature': 350.0},
        {'type': 'separator', 'name': 'hp_separator', 'inlet': 'heater', 'three_phase': True},
        {'type': 'valve', 'name': 'lp_valve', 'inlet': 'hp_separator', 'pressure': 10.0}
    ]
}

# Create reservoir fluid
reservoir_fluid = fluid('srk')
reservoir_fluid.addComponent('methane', 0.7)
reservoir_fluid.addComponent('ethane', 0.1)
reservoir_fluid.addComponent('propane', 0.05)
reservoir_fluid.addComponent('n-butane', 0.05)
reservoir_fluid.addComponent('n-pentane', 0.05)
reservoir_fluid.addComponent('n-hexane', 0.05)
reservoir_fluid.setTemperature(80.0, 'C')
reservoir_fluid.setPressure(150.0, 'bara')
reservoir_fluid.setTotalFlowRate(5.0, 'MSm3/day')

# Save config to temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(json_config, f, indent=2)
    json_file = f.name

try:
    # Load and run from JSON file
    process2 = ProcessBuilder.from_json(json_file, fluids={'reservoir_fluid': reservoir_fluid}).run()
    
    print("\n=== Separator Process Results (from JSON) ===")
    print(f"HP Separator gas rate: {process2.get('hp_separator').getGasOutStream().getFlowRate('MSm3/day'):.2f} MSm3/day")
    print(f"LP valve outlet pressure: {process2.get('lp_valve').getOutletStream().getPressure():.1f} bara")
finally:
    os.unlink(json_file)  # Clean up temp file


# =============================================================================
# Example 3: Loading from a YAML file (requires pyyaml)
# =============================================================================

try:
    import yaml
    
    yaml_config = """
name: Gas Cooling Process
equipment:
  - type: stream
    name: hot_gas
    fluid: gas
    flow_rate: 50000
    flow_unit: kg/hr
  - type: cooler
    name: cooler1
    inlet: hot_gas
    temperature: 300.0
  - type: separator
    name: knockout_drum
    inlet: cooler1
  - type: compressor
    name: export_compressor
    inlet: knockout_drum
    pressure: 150.0
"""
    
    # Create gas fluid
    gas = fluid('srk')
    gas.addComponent('methane', 0.85)
    gas.addComponent('ethane', 0.10)
    gas.addComponent('propane', 0.05)
    gas.setTemperature(80.0, 'C')
    gas.setPressure(70.0, 'bara')
    
    # Save to temp YAML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_config)
        yaml_file = f.name
    
    try:
        process3 = ProcessBuilder.from_yaml(yaml_file, fluids={'gas': gas}).run()
        
        print("\n=== Gas Cooling Process Results (from YAML) ===")
        print(f"Cooler outlet temperature: {process3.get('cooler1').getOutletStream().getTemperature() - 273.15:.1f} °C")
        print(f"Export compressor power: {process3.get('export_compressor').getPower()/1e3:.1f} kW")
    finally:
        os.unlink(yaml_file)
        
except ImportError:
    print("\n(Skipping YAML example - install pyyaml: pip install pyyaml)")


# =============================================================================
# Example 4: Dynamic configuration modification
# =============================================================================

print("\n=== Dynamic Configuration Example ===")

# Base configuration that can be modified programmatically
base_config = {
    'name': 'Parameterized Compressor',
    'equipment': [
        {'type': 'stream', 'name': 'inlet', 'fluid': 'gas'},
        {'type': 'compressor', 'name': 'comp', 'inlet': 'inlet', 'pressure': None}
    ]
}

# Create gas
gas = fluid('srk')
gas.addComponent('methane', 1.0)
gas.setTemperature(25.0, 'C')
gas.setPressure(10.0, 'bara')
gas.setTotalFlowRate(1.0, 'MSm3/day')

# Run with different outlet pressures
for outlet_pressure in [30, 50, 70]:
    # Modify config
    config_copy = base_config.copy()
    config_copy['equipment'] = [eq.copy() for eq in base_config['equipment']]
    config_copy['equipment'][1]['pressure'] = float(outlet_pressure)
    
    # Need fresh fluid for each run
    gas_copy = fluid('srk')
    gas_copy.addComponent('methane', 1.0)
    gas_copy.setTemperature(25.0, 'C')
    gas_copy.setPressure(10.0, 'bara')
    gas_copy.setTotalFlowRate(1.0, 'MSm3/day')
    
    result = ProcessBuilder.from_dict(config_copy, fluids={'gas': gas_copy}).run()
    power = result.get('comp').getPower() / 1e3
    print(f"Outlet pressure: {outlet_pressure} bara -> Power: {power:.1f} kW")
