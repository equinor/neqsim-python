# -*- coding: utf-8 -*-
"""
Process Simulation Approaches in NeqSim Python

This example demonstrates the three ways to build process simulations
in NeqSim Python:

1. Python Wrappers with Global Process - Simple, good for notebooks
2. ProcessContext - Explicit process management with context manager
3. ProcessBuilder - Fluent/chainable API for building processes

Each approach has its advantages depending on your use case.

@author: NeqSim Team
"""

from neqsim.thermo import fluid
from neqsim.process import (
    # Wrapper functions (Approach 1)
    clearProcess,
    runProcess,
    stream,
    separator,
    compressor,
    cooler,
    valve,
    # New classes (Approaches 2 & 3)
    ProcessContext,
    ProcessBuilder,
    newProcess,
)

print("=" * 70)
print("NEQSIM PYTHON: THREE APPROACHES TO PROCESS SIMULATION")
print("=" * 70)


# =============================================================================
# APPROACH 1: Python Wrappers with Global Process
# =============================================================================
# Best for: Quick prototyping, Jupyter notebooks, learning
# Pros: Simple, concise, automatic process management
# Cons: Global state, one process at a time

print("\n" + "-" * 70)
print("APPROACH 1: Python Wrappers (Global Process)")
print("-" * 70)

# Create fluid for the process
feed_fluid = fluid("srk")
feed_fluid.addComponent("nitrogen", 1.0)
feed_fluid.addComponent("methane", 85.0)
feed_fluid.addComponent("ethane", 8.0)
feed_fluid.addComponent("propane", 4.0)
feed_fluid.addComponent("n-butane", 2.0)
feed_fluid.setMixingRule("classic")
feed_fluid.setTemperature(30.0, "C")
feed_fluid.setPressure(30.0, "bara")
feed_fluid.setTotalFlowRate(5.0, "MSm3/day")

# Clear any previous process and build new one
clearProcess()

# Equipment is automatically added to global process
inlet = stream("inlet", feed_fluid)
sep1 = separator("HP separator", inlet)
comp1 = compressor("1st stage", sep1.getGasOutStream(), pres=60.0)
cool1 = cooler("intercooler", comp1.getOutletStream())
cool1.setOutTemperature(303.15)  # 30°C
comp2 = compressor("2nd stage", cool1.getOutletStream(), pres=120.0)

# Run the simulation
runProcess()

print(f"\nResults (Approach 1):")
print(f"  Stage 1 power: {comp1.getPower()/1e6:.3f} MW")
print(f"  Stage 2 power: {comp2.getPower()/1e6:.3f} MW")
print(f"  Total power:   {(comp1.getPower() + comp2.getPower())/1e6:.3f} MW")


# =============================================================================
# APPROACH 2: ProcessContext (Explicit Process Management)
# =============================================================================
# Best for: Production code, multiple processes, clean resource management
# Pros: Explicit control, supports multiple processes, context manager
# Cons: Slightly more verbose

print("\n" + "-" * 70)
print("APPROACH 2: ProcessContext (Explicit Process)")
print("-" * 70)

# Create fresh fluid
feed_fluid2 = fluid("srk")
feed_fluid2.addComponent("nitrogen", 1.0)
feed_fluid2.addComponent("methane", 85.0)
feed_fluid2.addComponent("ethane", 8.0)
feed_fluid2.addComponent("propane", 4.0)
feed_fluid2.addComponent("n-butane", 2.0)
feed_fluid2.setMixingRule("classic")
feed_fluid2.setTemperature(30.0, "C")
feed_fluid2.setPressure(30.0, "bara")
feed_fluid2.setTotalFlowRate(5.0, "MSm3/day")

# Use ProcessContext - each context has its own process
with ProcessContext("Compression Train") as ctx:
    # Methods mirror the wrapper functions
    inlet = ctx.stream("inlet", feed_fluid2)
    sep = ctx.separator("HP separator", inlet)
    comp1 = ctx.compressor("1st stage", sep.getGasOutStream(), pres=60.0)
    cool = ctx.cooler("intercooler", comp1.getOutletStream(), temp=303.15)
    comp2 = ctx.compressor("2nd stage", cool.getOutletStream(), pres=120.0)

    # Run this specific process
    ctx.run()

    # Access equipment by name
    stage1 = ctx.get("1st stage")
    stage2 = ctx.get("2nd stage")

    print(f"\nResults (Approach 2):")
    print(f"  Stage 1 power: {stage1.getPower()/1e6:.3f} MW")
    print(f"  Stage 2 power: {stage2.getPower()/1e6:.3f} MW")
    print(f"  Total power:   {(stage1.getPower() + stage2.getPower())/1e6:.3f} MW")


# =============================================================================
# APPROACH 3: ProcessBuilder (Fluent/Chainable API)
# =============================================================================
# Best for: Configuration-driven design, clean declarative style
# Pros: Chainable, equipment referenced by name, very readable
# Cons: Less direct access during construction

print("\n" + "-" * 70)
print("APPROACH 3: ProcessBuilder (Fluent API)")
print("-" * 70)

# Create fresh fluid
feed_fluid3 = fluid("srk")
feed_fluid3.addComponent("nitrogen", 1.0)
feed_fluid3.addComponent("methane", 85.0)
feed_fluid3.addComponent("ethane", 8.0)
feed_fluid3.addComponent("propane", 4.0)
feed_fluid3.addComponent("n-butane", 2.0)
feed_fluid3.setMixingRule("classic")
feed_fluid3.setTemperature(30.0, "C")
feed_fluid3.setPressure(30.0, "bara")
feed_fluid3.setTotalFlowRate(5.0, "MSm3/day")

# Build process with fluent API - all chained together
process = (
    ProcessBuilder("Compression Train")
    .add_stream("inlet", feed_fluid3)
    .add_separator("HP separator", "inlet")
    .add_compressor("1st stage", "HP separator", pressure=60.0)
    .add_cooler("intercooler", "1st stage", temperature=303.15)
    .add_compressor("2nd stage", "intercooler", pressure=120.0)
    .run()
)

# Access results
comp1 = process.get("1st stage")
comp2 = process.get("2nd stage")

print(f"\nResults (Approach 3):")
print(f"  Stage 1 power: {comp1.getPower()/1e6:.3f} MW")
print(f"  Stage 2 power: {comp2.getPower()/1e6:.3f} MW")
print(f"  Total power:   {(comp1.getPower() + comp2.getPower())/1e6:.3f} MW")


# =============================================================================
# HYBRID APPROACH: Wrappers with Explicit Process
# =============================================================================
# You can also use wrapper functions with an explicit process parameter

print("\n" + "-" * 70)
print("HYBRID: Wrapper Functions with process= Parameter")
print("-" * 70)

# Create fresh fluid
feed_fluid4 = fluid("srk")
feed_fluid4.addComponent("nitrogen", 1.0)
feed_fluid4.addComponent("methane", 85.0)
feed_fluid4.addComponent("ethane", 8.0)
feed_fluid4.addComponent("propane", 4.0)
feed_fluid4.addComponent("n-butane", 2.0)
feed_fluid4.setMixingRule("classic")
feed_fluid4.setTemperature(30.0, "C")
feed_fluid4.setPressure(30.0, "bara")
feed_fluid4.setTotalFlowRate(5.0, "MSm3/day")

# Create explicit process
my_process = newProcess("Compression Train")

# Use wrapper functions but specify process explicitly
inlet = stream("inlet", feed_fluid4, process=my_process)
sep = separator("HP separator", inlet, process=my_process)
comp1 = compressor("1st stage", sep.getGasOutStream(), pres=60.0, process=my_process)
cool = cooler("intercooler", comp1.getOutletStream(), process=my_process)
cool.setOutTemperature(303.15)
comp2 = compressor("2nd stage", cool.getOutletStream(), pres=120.0, process=my_process)

# Run specific process
my_process.run()

print(f"\nResults (Hybrid):")
print(f"  Stage 1 power: {comp1.getPower()/1e6:.3f} MW")
print(f"  Stage 2 power: {comp2.getPower()/1e6:.3f} MW")
print(f"  Total power:   {(comp1.getPower() + comp2.getPower())/1e6:.3f} MW")


# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("CHOOSING AN APPROACH")
print("=" * 70)
print(
    """
| Use Case                        | Recommended Approach          |
|---------------------------------|-------------------------------|
| Learning / tutorials            | Wrappers (global process)     |
| Jupyter notebooks               | Wrappers (global process)     |
| Quick prototyping               | Wrappers (global process)     |
| Production applications         | ProcessContext or ProcessBuilder |
| Multiple parallel processes     | ProcessContext                |
| Configuration-driven design     | ProcessBuilder                |
| Clean declarative style         | ProcessBuilder                |
| Mixing wrapper convenience      | Hybrid (process= parameter)   |
  with explicit control           |                               |
"""
)
