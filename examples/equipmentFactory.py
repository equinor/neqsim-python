# -*- coding: utf-8 -*-
"""
Equipment Factory Example

This example demonstrates using the EquipmentFactory class in NeqSim
to create process equipment dynamically at runtime.

The factory pattern allows:
- Creating equipment by name string (useful for configuration-driven design)
- Dynamic process construction from JSON/YAML configurations
- Flexible equipment instantiation without knowing exact class names

@author: NeqSim Team
"""

from neqsim import jneqsim
from neqsim.thermo import fluid

# Create a test fluid
test_fluid = fluid("srk")
test_fluid.addComponent("methane", 85.0)
test_fluid.addComponent("ethane", 10.0)
test_fluid.addComponent("propane", 5.0)
test_fluid.setMixingRule("classic")
test_fluid.setTemperature(30.0, "C")
test_fluid.setPressure(50.0, "bara")
test_fluid.setTotalFlowRate(10000.0, "kg/hr")

# Get the EquipmentFactory class
EquipmentFactory = jneqsim.process.equipment.EquipmentFactory

print("=" * 60)
print("EQUIPMENT FACTORY DEMONSTRATION")
print("=" * 60)

# Method 1: Create equipment by type string
print("\n1. Creating equipment by type name strings:")

# Create a valve
valve = EquipmentFactory.createEquipment("valve1", "ThrottlingValve")
print(f"   Created: {valve.getName()} ({type(valve).__name__})")

# Create a separator
separator = EquipmentFactory.createEquipment("sep1", "Separator")
print(f"   Created: {separator.getName()} ({type(separator).__name__})")

# Create a compressor
compressor = EquipmentFactory.createEquipment("comp1", "Compressor")
print(f"   Created: {compressor.getName()} ({type(compressor).__name__})")

# Create a heater
heater = EquipmentFactory.createEquipment("heater1", "Heater")
print(f"   Created: {heater.getName()} ({type(heater).__name__})")

# Create a cooler
cooler = EquipmentFactory.createEquipment("cooler1", "Cooler")
print(f"   Created: {cooler.getName()} ({type(cooler).__name__})")

# Create a mixer
mixer = EquipmentFactory.createEquipment("mixer1", "Mixer")
print(f"   Created: {mixer.getName()} ({type(mixer).__name__})")

# Create a pump
pump = EquipmentFactory.createEquipment("pump1", "Pump")
print(f"   Created: {pump.getName()} ({type(pump).__name__})")

# Method 2: Create equipment using enum
print("\n2. Creating equipment using EquipmentEnum:")
EquipmentEnum = jneqsim.process.equipment.EquipmentEnum

splitter = EquipmentFactory.createEquipment("splitter1", EquipmentEnum.Splitter)
print(f"   Created: {splitter.getName()} (using EquipmentEnum.Splitter)")

# Method 3: Build a dynamic process from a list of equipment specs
print("\n3. Building a complete process dynamically:")

# Define equipment configuration (could come from JSON/YAML)
equipment_config = [
    {"name": "inlet_valve", "type": "ThrottlingValve"},
    {"name": "hp_separator", "type": "Separator"},
    {"name": "gas_compressor", "type": "Compressor"},
    {"name": "gas_cooler", "type": "Cooler"},
]

# Create all equipment from config
created_equipment = {}
for config in equipment_config:
    equip = EquipmentFactory.createEquipment(config["name"], config["type"])
    created_equipment[config["name"]] = equip
    print(f"   Created: {config['name']} ({config['type']})")

# List all available equipment types
print("\n4. Available equipment types (partial list):")
equipment_types = [
    "Stream",
    "Compressor",
    "Pump",
    "Separator",
    "HeatExchanger",
    "ThrottlingValve",
    "Mixer",
    "Splitter",
    "Cooler",
    "Heater",
    "Expander",
    "Pipeline",
]
for eq_type in equipment_types:
    print(f"   - {eq_type}")

print("\n" + "=" * 60)
print("The EquipmentFactory enables configuration-driven process design,")
print("making it easy to build processes from external specifications.")
print("=" * 60)
