"""Process simulation tools for NeqSim.

This module provides Python wrapper functions for creating and running
process simulations using the NeqSim Java library. It includes equipment
like compressors, pumps, heat exchangers, separators, and more.

Four Approaches for Process Simulation
======================================

NeqSim Python offers four ways to build process simulations:

1. **Python Wrappers with Global Process** (Recommended for beginners)
   Simple functions that auto-add equipment to a global process.

2. **ProcessContext** (Recommended for production)
   Context manager with its own process - supports multiple processes.

3. **ProcessBuilder** (Fluent API)
   Chainable builder pattern - great for configuration-driven design.

4. **Direct Java Access** (Full control)
   Direct jneqsim access for advanced features.

Approach 1: Python Wrappers (Global Process)
--------------------------------------------
Simple functions that automatically add equipment to a global process.
Use clearProcess() to reset, runProcess() to execute.

    >>> from neqsim.thermo import fluid
    >>> from neqsim.process import stream, compressor, runProcess, clearProcess
    >>>
    >>> clearProcess()
    >>> my_fluid = fluid('srk')
    >>> my_fluid.addComponent('methane', 1.0)
    >>> my_fluid.setTemperature(30.0, 'C')
    >>> my_fluid.setPressure(10.0, 'bara')
    >>>
    >>> inlet = stream('inlet', my_fluid)
    >>> comp = compressor('compressor1', inlet, pres=50.0)
    >>> runProcess()
    >>> print(f"Power: {comp.getPower()/1e6:.2f} MW")

Pros: Concise, readable, great for learning and prototyping
Cons: Global state limits to one process at a time

Approach 2: ProcessContext (Explicit Process Management)
---------------------------------------------------------
Context manager that creates its own ProcessSystem. Supports multiple
independent processes running simultaneously.

    >>> from neqsim.thermo import fluid
    >>> from neqsim.process import ProcessContext
    >>>
    >>> with ProcessContext("Compression") as ctx:
    ...     my_fluid = fluid('srk')
    ...     my_fluid.addComponent('methane', 1.0)
    ...     my_fluid.setPressure(10.0, 'bara')
    ...
    ...     inlet = ctx.stream('inlet', my_fluid)
    ...     comp = ctx.compressor('comp1', inlet, pres=50.0)
    ...     ctx.run()
    ...     print(f"Power: {comp.getPower()/1e6:.2f} MW")

Pros: Multiple processes, explicit control, clean resource management
Cons: Slightly more verbose than global wrappers

Approach 3: ProcessBuilder (Fluent/Chainable API)
--------------------------------------------------
Builder pattern with method chaining. Equipment referenced by name.
Ideal for configuration-driven process construction.

    >>> from neqsim.thermo import fluid
    >>> from neqsim.process import ProcessBuilder
    >>>
    >>> my_fluid = fluid('srk')
    >>> my_fluid.addComponent('methane', 1.0)
    >>> my_fluid.setPressure(10.0, 'bara')
    >>>
    >>> process = (ProcessBuilder("Compression")
    ...     .add_stream('inlet', my_fluid)
    ...     .add_compressor('comp1', 'inlet', pressure=50.0)
    ...     .run())
    >>>
    >>> print(f"Power: {process.get('comp1').getPower()/1e6:.2f} MW")

Pros: Very readable, chainable, equipment by name, declarative style
Cons: Less direct access during construction

Approach 4: Direct Java Access
-------------------------------
Create and manage ProcessSystem objects explicitly using jneqsim.

    >>> from neqsim import jneqsim
    >>> from neqsim.thermo import fluid
    >>>
    >>> my_fluid = fluid('srk')
    >>> my_fluid.addComponent('methane', 1.0)
    >>> my_fluid.setPressure(10.0, 'bara')
    >>>
    >>> inlet = jneqsim.process.equipment.stream.Stream('inlet', my_fluid)
    >>> comp = jneqsim.process.equipment.compressor.Compressor('comp1', inlet)
    >>> comp.setOutletPressure(50.0)
    >>>
    >>> process = jneqsim.process.processmodel.ProcessSystem()
    >>> process.add(inlet)
    >>> process.add(comp)
    >>> process.run()

Pros: Full access to all Java features, maximum flexibility
Cons: Verbose, requires Java knowledge

Hybrid Approach: Wrappers with process= Parameter
--------------------------------------------------
Wrapper functions accept an optional process= parameter for explicit
process control while keeping concise syntax:

    >>> from neqsim.process import stream, compressor, newProcess
    >>>
    >>> my_process = newProcess('MyProcess')
    >>> inlet = stream('inlet', my_fluid, process=my_process)
    >>> comp = compressor('comp1', inlet, pres=50.0, process=my_process)
    >>> my_process.run()

Choosing an Approach
--------------------
+----------------------------------+--------------------------------+
| Use Case                         | Recommended Approach           |
+==================================+================================+
| Learning / tutorials             | Wrappers (global process)      |
| Jupyter notebooks                | Wrappers (global process)      |
| Quick prototyping                | Wrappers (global process)      |
| Production applications          | ProcessContext                 |
| Multiple parallel processes      | ProcessContext                 |
| Configuration-driven design      | ProcessBuilder                 |
| Full Java API access             | Direct jneqsim                 |
+----------------------------------+--------------------------------+

Available Equipment
-------------------
Streams: stream, virtualstream, neqstream, energystream
Separation: separator, separator3phase, gasscrubber, filters
Compression: compressor, pump, expander
Heat Transfer: heater, cooler, heatExchanger
Valves: valve, safety_valve
Mixing/Splitting: mixer, phasemixer, splitter, compsplitter, staticmixer
Pipelines: pipe, pipeline, beggs_brill_pipe, wellflow
Columns: distillationColumn, simpleTEGAbsorber, waterStripperColumn
Control: calculator, setpoint, adjuster, flowrateadjuster, setter, flowsetter
Special: ejector, flare, flarestack, recycle, saturator, GORfitter
Storage: tank, simplereservoir, manifold
Measurement: waterDewPointAnalyser, hydrateEquilibriumTemperatureAnalyser
Power: windturbine, solarpanel, batterystorage, fuelcell, electrolyzer, co2electrolyzer

Classes: ProcessContext, ProcessBuilder
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional, List, Dict, Union

import pandas as pd
from jpype.types import *

from neqsim import jneqsim

processoperations = jneqsim.process.processmodel.ProcessSystem()
_loop_mode: bool = False


_YAML_SUFFIXES = {".yaml", ".yml"}


def _as_float_list(values) -> list[float]:
    if values is None:
        return []
    if hasattr(values, "tolist"):
        values = values.tolist()
    return [float(v) for v in list(values)]


def _as_float_matrix(values) -> list[list[float]]:
    if values is None:
        return []
    if hasattr(values, "tolist"):
        values = values.tolist()
    return [[float(v) for v in row] for row in list(values)]


def _resolve_path_in_cwd(
    user_path: str,
    *,
    allowed_suffixes: Optional[set[str]] = None,
    must_exist: bool = False,
) -> Path:
    """
    Resolve a user-supplied path safely inside the current working directory.

    This is used for convenience helpers that read/write local config/result files.
    To avoid path traversal / arbitrary file read/write, absolute paths and paths that
    escape the current working directory are rejected.
    """
    if not isinstance(user_path, str):
        raise TypeError("path must be a string")

    if "\x00" in user_path:
        raise ValueError("Path contains NUL byte.")

    base_dir = os.path.abspath(os.getcwd())
    resolved_str = os.path.abspath(os.path.join(base_dir, user_path))

    # Ensure the normalized path is still within the base directory.
    # Using `startswith` on normalized paths is recognized by CodeQL as a safe-access check.
    base_prefix = base_dir + os.sep
    if resolved_str.startswith(base_prefix):
        pass
    else:
        raise ValueError(
            "Path traversal outside the current working directory is not allowed."
        )

    resolved = Path(resolved_str)

    if allowed_suffixes is not None:
        suffix = resolved.suffix.lower()
        if suffix not in allowed_suffixes:
            allowed = ", ".join(sorted(allowed_suffixes))
            raise ValueError(f"Invalid file extension '{suffix}'. Allowed: {allowed}.")

    if must_exist and not resolved.is_file():
        raise FileNotFoundError(f"File not found: {resolved}")

    return resolved


class ProcessContext:
    """
    Context manager for explicit process simulation management.

    ProcessContext provides a clean way to create and manage process
    simulations without relying on global state. Each context has its
    own ProcessSystem, allowing multiple independent processes.

    Args:
        name: Name of the process (optional).

    Attributes:
        process: The underlying ProcessSystem object.
        equipment: Dictionary of equipment by name.

    Example:
        >>> from neqsim.thermo import fluid
        >>> from neqsim.process import ProcessContext
        >>>
        >>> with ProcessContext("Compression") as ctx:
        ...     feed = fluid('srk')
        ...     feed.addComponent('methane', 1.0)
        ...     feed.setPressure(10.0, 'bara')
        ...
        ...     inlet = ctx.stream('inlet', feed)
        ...     comp = ctx.compressor('comp1', inlet, pres=50.0)
        ...     ctx.run()
        ...     print(f"Power: {comp.getPower()/1e6:.2f} MW")

    Example without context manager:
        >>> ctx = ProcessContext("MyProcess")
        >>> inlet = ctx.stream('inlet', my_fluid)
        >>> comp = ctx.compressor('comp1', inlet, pres=50.0)
        >>> ctx.run()
    """

    def __init__(self, name: str = ""):
        """Create a new ProcessContext with its own ProcessSystem."""
        self.process = jneqsim.process.processmodel.ProcessSystem(name)
        self.equipment: Dict[str, Any] = {}
        self._name = name

    def __enter__(self) -> "ProcessContext":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit the context manager."""
        return False

    def add(self, equipment: Any) -> Any:
        """
        Add equipment to the process.

        Args:
            equipment: Equipment object to add.

        Returns:
            The equipment object (for chaining).
        """
        self.process.add(equipment)
        if hasattr(equipment, "getName"):
            self.equipment[equipment.getName()] = equipment
        return equipment

    def run(self) -> "ProcessContext":
        """
        Run the process simulation.

        Returns:
            Self for method chaining.
        """
        self.process.run()
        return self

    def run_transient(self, dt: float, time: float) -> "ProcessContext":
        """
        Run transient simulation.

        Args:
            dt: Time step in seconds.
            time: Total simulation time in seconds.

        Returns:
            Self for method chaining.
        """
        self.process.setTimeStep(dt)
        self.process.runTransient(time)
        return self

    def get(self, name: str) -> Any:
        """
        Get equipment by name.

        Args:
            name: Name of the equipment.

        Returns:
            The equipment object.
        """
        return self.equipment.get(name)

    def stream(self, name: str, thermo_system: Any, t: float = 0, p: float = 0) -> Any:
        """Create a stream and add to this process."""
        if t != 0:
            thermo_system.setTemperature(t)
        if p != 0:
            thermo_system.setPressure(p)
        s = jneqsim.process.equipment.stream.Stream(name, thermo_system)
        return self.add(s)

    def separator(self, name: str, inlet_stream: Any) -> Any:
        """Create a separator and add to this process."""
        sep = jneqsim.process.equipment.separator.Separator(name, inlet_stream)
        return self.add(sep)

    def separator3phase(self, name: str, inlet_stream: Any) -> Any:
        """Create a 3-phase separator and add to this process."""
        sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(
            name, inlet_stream
        )
        return self.add(sep)

    def compressor(
        self, name: str, inlet_stream: Any, pres: float = 0, efficiency: float = 0.75
    ) -> Any:
        """Create a compressor and add to this process."""
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        if pres > 0:
            comp.setOutletPressure(pres)
        comp.setIsentropicEfficiency(efficiency)
        return self.add(comp)

    def pump(
        self, name: str, inlet_stream: Any, pres: float = 0, efficiency: float = 0.75
    ) -> Any:
        """Create a pump and add to this process."""
        p = jneqsim.process.equipment.pump.Pump(name, inlet_stream)
        if pres > 0:
            p.setOutletPressure(pres)
        p.setIsentropicEfficiency(efficiency)
        return self.add(p)

    def expander(self, name: str, inlet_stream: Any, pres: float = 0) -> Any:
        """Create an expander and add to this process."""
        exp = jneqsim.process.equipment.expander.Expander(name, inlet_stream)
        if pres > 0:
            exp.setOutletPressure(pres)
        return self.add(exp)

    def valve(self, name: str, inlet_stream: Any, pres: float = 0) -> Any:
        """Create a valve and add to this process."""
        v = jneqsim.process.equipment.valve.ThrottlingValve(name, inlet_stream)
        if pres > 0:
            v.setOutletPressure(pres)
        return self.add(v)

    def heater(self, name: str, inlet_stream: Any, temp: float = 0) -> Any:
        """Create a heater and add to this process."""
        h = jneqsim.process.equipment.heatexchanger.Heater(name, inlet_stream)
        if temp > 0:
            h.setOutTemperature(temp)
        return self.add(h)

    def cooler(self, name: str, inlet_stream: Any, temp: float = 0) -> Any:
        """Create a cooler and add to this process."""
        c = jneqsim.process.equipment.heatexchanger.Cooler(name, inlet_stream)
        if temp > 0:
            c.setOutTemperature(temp)
        return self.add(c)

    def mixer(self, name: str) -> Any:
        """Create a mixer and add to this process."""
        m = jneqsim.process.equipment.mixer.Mixer(name)
        return self.add(m)

    def splitter(
        self, name: str, inlet_stream: Any, split_factors: List[float] = None
    ) -> Any:
        """Create a splitter and add to this process."""
        s = jneqsim.process.equipment.splitter.Splitter(name, inlet_stream)
        if split_factors:
            s.setSplitFactors(split_factors)
        return self.add(s)

    def heat_exchanger(
        self, name: str, hot_stream: Any, cold_stream: Any, approach_temp: float = 10.0
    ) -> Any:
        """Create a heat exchanger and add to this process."""
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(
            name, hot_stream, cold_stream
        )
        hx.setApproachTemperature(approach_temp)
        return self.add(hx)

    def pipe(
        self, name: str, inlet_stream: Any, length: float = 100.0, diameter: float = 0.1
    ) -> Any:
        """Create a pipe and add to this process."""
        p = jneqsim.process.equipment.pipeline.AdiabaticPipe(name, inlet_stream)
        p.setLength(length)
        p.setDiameter(diameter)
        return self.add(p)

    def recycle(self, name: str, inlet_stream: Any = None) -> Any:
        """Create a recycle and add to this process."""
        r = jneqsim.process.equipment.util.Recycle(name)
        if inlet_stream is not None:
            r.addStream(inlet_stream)
        return self.add(r)

    def gas_scrubber(self, name: str, inlet_stream: Any) -> Any:
        """Create a gas scrubber and add to this process."""
        scrubber = jneqsim.process.equipment.separator.GasScrubber(name, inlet_stream)
        return self.add(scrubber)

    def distillation_column(
        self, name: str, trays: int = 5, reboiler: bool = True, condenser: bool = True
    ) -> Any:
        """Create a distillation column and add to this process."""
        column = jneqsim.process.equipment.distillation.DistillationColumn(
            trays, reboiler, condenser
        )
        column.setName(name)
        return self.add(column)

    def teg_absorber(self, name: str) -> Any:
        """Create a simple TEG absorber and add to this process."""
        absorber = jneqsim.process.equipment.absorber.SimpleTEGAbsorber(name)
        return self.add(absorber)

    def water_stripper_column(self, name: str) -> Any:
        """Create a water stripper column and add to this process."""
        column = jneqsim.process.equipment.absorber.WaterStripperColumn(name)
        return self.add(column)

    def component_splitter(
        self, name: str, inlet_stream: Any, split_factors: List[float] = None
    ) -> Any:
        """Create a component splitter and add to this process."""
        splitter = jneqsim.process.equipment.splitter.ComponentSplitter(
            name, inlet_stream
        )
        if split_factors:
            splitter.setSplitFactors(split_factors)
        return self.add(splitter)

    def saturator(self, name: str, inlet_stream: Any) -> Any:
        """Create a stream saturator and add to this process."""
        sat = jneqsim.process.equipment.util.StreamSaturatorUtil(name, inlet_stream)
        return self.add(sat)

    def filters(self, name: str, inlet_stream: Any) -> Any:
        """Create a filter and add to this process."""
        f = jneqsim.process.equipment.filter.Filter(name, inlet_stream)
        return self.add(f)

    def calculator(self, name: str) -> Any:
        """Create a calculator and add to this process."""
        calc = jneqsim.process.equipment.util.Calculator(name)
        return self.add(calc)

    def setpoint(
        self,
        name: str,
        target_equipment: Any,
        target_variable: str,
        source_equipment: Any,
    ) -> Any:
        """Create a setpoint controller and add to this process."""
        sp = jneqsim.process.equipment.util.SetPoint(
            name, target_equipment, target_variable, source_equipment
        )
        return self.add(sp)

    def adjuster(
        self,
        name: str,
        target_equipment: Any = None,
        target_variable: str = None,
        target_value: float = None,
    ) -> Any:
        """Create an adjuster and add to this process."""
        adj = jneqsim.process.equipment.util.Adjuster(name)
        if target_equipment is not None and target_variable is not None:
            adj.setAdjustedVariable(target_equipment, target_variable)
        if target_value is not None:
            adj.setTargetValue(target_value)
        return self.add(adj)

    def ejector(self, name: str, motive_stream: Any, suction_stream: Any) -> Any:
        """Create an ejector and add to this process."""
        ej = jneqsim.process.equipment.ejector.Ejector(
            name, motive_stream, suction_stream
        )
        return self.add(ej)

    def flare(self, name: str, inlet_stream: Any = None) -> Any:
        """Create a flare and add to this process."""
        f = jneqsim.process.equipment.flare.Flare(name)
        if inlet_stream is not None:
            f.addStream(inlet_stream)
        return self.add(f)

    def tank(self, name: str, inlet_stream: Any = None) -> Any:
        """Create a tank and add to this process."""
        t = jneqsim.process.equipment.tank.Tank(name)
        if inlet_stream is not None:
            t.addStream(inlet_stream)
        return self.add(t)


class ProcessBuilder:
    """
    Fluent builder for constructing process simulations.

    ProcessBuilder provides a chainable API for building processes
    step by step. Equipment is referenced by name, making it easy
    to construct processes from configuration data.

    QUICK START
    ===========

    Basic usage follows a simple pattern:
    1. Create a fluid (thermodynamic system)
    2. Create a ProcessBuilder
    3. Chain equipment additions using the fluent API
    4. Call .run() to execute the simulation
    5. Access results via .get() or .results()

    Example::

        from neqsim.thermo import fluid
        from neqsim.process import ProcessBuilder

        # Create feed fluid
        feed = fluid('srk')
        feed.addComponent('methane', 0.9)
        feed.addComponent('ethane', 0.1)
        feed.setMolarFlowRate(100.0, 'mol/sec')
        feed.setTemperature(25.0, 'C')
        feed.setPressure(10.0, 'bara')

        # Build and run process
        process = (
            ProcessBuilder("My Process")
            .add_stream('feed', feed)
            .add_compressor('comp', 'feed', outlet_pressure=50.0)
            .add_cooler('cooler', 'comp', outlet_temperature=30.0)
            .add_separator('sep', 'cooler')
            .run()
        )

        # Access results
        print(f"Compressor power: {process.get('comp').getPower()/1e3:.1f} kW")
        print(f"Gas out temp: {process.get('sep').getGasOutStream().getTemperature('C'):.1f} C")

    FLUENT API PATTERN
    ==================

    All add_* methods return ``self``, enabling method chaining::

        builder = (
            ProcessBuilder()
            .add_stream(...)
            .add_compressor(...)
            .add_cooler(...)
            .run()
        )

    EQUIPMENT CONNECTIONS
    =====================

    Equipment is connected by referencing upstream equipment by name.
    The builder automatically gets the appropriate outlet stream.

    **Basic connection** - just use the equipment name::

        .add_compressor('comp', inlet='feed')    # Gets feed's outlet
        .add_cooler('cooler', inlet='comp')       # Gets comp's outlet

    **Separator outlets** - use dot notation for specific outlets::

        .add_separator('sep', inlet='cooler')
        .add_compressor('gas_comp', inlet='sep.gas')      # Gas outlet
        .add_pump('oil_pump', inlet='sep.oil')            # Oil outlet
        .add_pump('water_pump', inlet='sep.water')        # Water outlet (3-phase)

    **Available outlet types**:
        - ``.gas`` or ``.vapor`` - gas/vapor phase outlet
        - ``.liquid`` - liquid outlet (2-phase separator)
        - ``.oil`` - oil outlet (3-phase separator)
        - ``.water`` or ``.aqueous`` - water outlet (3-phase separator)
        - ``.out`` - generic outlet (VirtualStream, etc.)

    EQUIPMENT CATEGORIES
    ====================

    **Streams**::

        .add_stream(name, fluid, temperature=None, pressure=None,
                    flow_rate=None, flow_unit='kg/sec')
        .add_virtual_stream(name, source=None, flow_rate=None, ...)
        .add_neq_stream(name, fluid)              # Non-equilibrium stream
        .add_energy_stream(name)                  # Energy/duty stream
        .add_well_stream(name, fluid)             # Well stream

    **Separation**::

        .add_separator(name, inlet)               # 2-phase separator
        .add_three_phase_separator(name, inlet)   # 3-phase separator
        .add_separator_with_dimensions(name, inlet, inner_diameter, length)
        .add_gas_scrubber(name, inlet)
        .add_gas_scrubber_with_options(name, inlet, ...)

    **Compression**::

        .add_compressor(name, inlet, outlet_pressure=None, isentropic_efficiency=None)
        .add_compressor_with_chart(name, inlet)   # With performance curves
        .add_polytopic_compressor(name, inlet, outlet_pressure, efficiency)

    **Pumping**::

        .add_pump(name, inlet, outlet_pressure=None, efficiency=None)

    **Heat Transfer**::

        .add_heater(name, inlet, outlet_temperature=None)
        .add_cooler(name, inlet, outlet_temperature=None)
        .add_heat_exchanger(name, hot_inlet=None, cold_inlet=None)

    **Pressure Control**::

        .add_valve(name, inlet, outlet_pressure=None)
        .add_valve_with_options(name, inlet, outlet_pressure, cv=None, ...)

    **Mixing/Splitting**::

        .add_mixer(name, inlets=None)             # List of inlet names
        .add_static_mixer(name, inlets=None)
        .add_splitter(name, inlet, split_fractions=None)
        .add_splitter_with_flowrates(name, inlet, flowrates, flow_unit)

    **Pipelines**::

        .add_pipe(name, inlet, length=None, diameter=None)
        .add_beggs_brill_pipe(name, inlet, length, elevation, diameter, ...)
        .add_two_phase_pipe(name, inlet, length, elevation, diameter, ...)

    **Distillation/Absorption**::

        .add_distillation_column(name, trays=5, reboiler=True, condenser=True)
        .add_teg_absorber(name)
        .add_simple_absorber(name, inlet_gas=None, inlet_liquid=None)
        .add_water_stripper(name)

    **Process Control**::

        .add_setpoint(name, source_equipment, source_variable, target_equipment,
                      target_variable, target_value)
        .add_adjuster(name, target_equipment, target_variable, target_value,
                      adjust_equipment, adjust_variable)
        .add_calculator(name)
        .add_pid_controller(name, transmitter=None, valve=None, setpoint=None, ...)

    **Measurement**::

        .add_pressure_transmitter(name, equipment, measurement_point='outlet')
        .add_temperature_transmitter(name, equipment, measurement_point='outlet')
        .add_flow_transmitter(name, equipment, measurement_point='outlet')
        .add_level_transmitter(name, separator)

    **Other Equipment**::

        .add_ejector(name, motive_inlet=None, suction_inlet=None)
        .add_flare(name, inlet=None)
        .add_tank(name, inlet=None)
        .add_saturator(name, inlet=None)
        .add_filter(name, inlet=None)
        .add_reactor(name, inlet)                 # Gibbs reactor
        .add_component_splitter(name, inlet, split_factors=None)

    RECYCLE LOOPS
    =============

    Recycles handle "streams that go back" - a common challenge because you
    need to reference equipment that doesn't exist yet.

    **The Pattern**: Create a virtual stream (initial guess) FIRST, build
    forward through the process, then connect the actual output back.

    Example - Anti-surge recycle::

        process = (
            ProcessBuilder()
            .add_stream('feed', fluid, flow_rate=100, flow_unit='kg/hr')

            # Step 1: Create virtual stream as initial guess
            .add_virtual_stream('recycle_guess', source='feed',
                                flow_rate=5.0, flow_unit='kg/hr')

            # Step 2: Build forward using the guess
            .add_mixer('mixer', inlets=['feed', 'recycle_guess.out'])
            .add_compressor('compressor', inlet='mixer', outlet_pressure=50)
            .add_cooler('cooler', inlet='compressor', outlet_temperature=30)
            .add_separator('separator', inlet='cooler')

            # Step 3: Connect actual output back to virtual stream
            .add_recycle('antisurge',
                         inlet='separator.liquid',    # actual stream
                         outlet='recycle_guess.out',  # virtual stream
                         tolerance=1e-6)
            .run()
        )

    **Alternative helper methods**::

        # Using setup/close pattern
        .setup_recycle_loop('my_recycle', 'recycle_guess', 'feed',
                            initial_flow=5.0, initial_flow_unit='kg/hr')
        # ... build process ...
        .close_recycle_loop('my_recycle', 'separator.liquid')

    CONFIGURATION & ACCESS
    ======================

    **Configure equipment after creation**::

        .configure('equipment_name', lambda eq: eq.setSomeProperty(value))

    **Access equipment**::

        process.get('compressor')           # Get Java equipment object
        process.get('separator').run()      # Run single equipment
        process['compressor']               # Dict-style access

    **Get results**::

        process.results()                   # Returns underlying ProcessSystem
        process.run()                       # Run simulation, returns self

    BUILDING FROM CONFIG
    ====================

    For dynamic process construction, use ``add()`` or ``add_from_config()``::

        # Single equipment with type string
        builder.add('compressor', 'comp1', inlet='feed', outlet_pressure=50)

        # From configuration list
        config = [
            {'type': 'stream', 'name': 'feed', 'fluid': my_fluid},
            {'type': 'compressor', 'name': 'comp', 'inlet': 'feed',
             'outlet_pressure': 50},
            {'type': 'cooler', 'name': 'cooler', 'inlet': 'comp',
             'outlet_temperature': 30},
        ]
        builder.add_from_config(config, fluids={'feed_fluid': my_fluid})

    COMPLETE EXAMPLES
    =================

    **Gas Compression Train**::

        feed = fluid('srk')
        feed.addComponent('methane', 0.85)
        feed.addComponent('ethane', 0.10)
        feed.addComponent('propane', 0.05)
        feed.setMolarFlowRate(1000, 'mol/sec')
        feed.setTemperature(25, 'C')
        feed.setPressure(5, 'bara')

        process = (
            ProcessBuilder("Compression Train")
            .add_stream('inlet', feed)
            .add_gas_scrubber('scrubber', 'inlet')
            .add_compressor('stage1', 'scrubber.gas', outlet_pressure=15)
            .add_cooler('ic1', 'stage1', outlet_temperature=35)
            .add_gas_scrubber('kd1', 'ic1')
            .add_compressor('stage2', 'kd1.gas', outlet_pressure=45)
            .add_cooler('ic2', 'stage2', outlet_temperature=35)
            .add_gas_scrubber('kd2', 'ic2')
            .add_compressor('stage3', 'kd2.gas', outlet_pressure=120)
            .add_cooler('aftercooler', 'stage3', outlet_temperature=40)
            .run()
        )

        total_power = sum(
            process.get(f'stage{i}').getPower() for i in [1, 2, 3]
        ) / 1e6
        print(f"Total compression power: {total_power:.2f} MW")

    **Oil/Gas Separation**::

        wellstream = fluid('srk')
        # ... configure wellstream ...

        process = (
            ProcessBuilder("Separation")
            .add_stream('well', wellstream)
            .add_heater('heater', 'well', outlet_temperature=80)
            .add_three_phase_separator('hp_sep', 'heater')
            .add_valve('gas_valve', 'hp_sep.gas', outlet_pressure=20)
            .add_valve('oil_valve', 'hp_sep.oil', outlet_pressure=5)
            .add_three_phase_separator('lp_sep', 'oil_valve')
            .add_pump('export_pump', 'lp_sep.oil', outlet_pressure=30)
            .run()
        )

    **With Recycle (TEG Dehydration)**::

        process = (
            ProcessBuilder("TEG Dehydration")
            .add_stream('wet_gas', wet_gas_fluid)
            .add_virtual_stream('lean_teg_recycle', source='teg_stream',
                                flow_rate=1000, flow_unit='kg/hr')
            .add_teg_absorber('absorber')
            .configure('absorber', lambda a: (
                a.addGasInStream(process.get('wet_gas').getOutletStream()),
                a.addSolventInStream(process.get('lean_teg_recycle').getOutStream())
            ))
            # ... regeneration equipment ...
            .add_recycle('teg_recycle',
                         inlet='teg_cooler',
                         outlet='lean_teg_recycle.out',
                         tolerance=1e-4)
            .run()
        )

    See Also
    --------
    neqsim.thermo.fluid : Create thermodynamic systems
    neqsim.process.newProcess : Alternative process creation function
    """

    def __init__(self, name: str = ""):
        """Create a new ProcessBuilder."""
        self.process = jneqsim.process.processmodel.ProcessSystem(name)
        self.equipment: Dict[str, Any] = {}
        self._name = name

    def _get_outlet(self, ref: Union[str, Any]) -> Any:
        """
        Get outlet stream from equipment reference (name or object).

        Supports dot notation for selecting specific outlets:

        Separators:
        - 'separator.gas' or 'separator.vapor' - gas/vapor outlet
        - 'separator.liquid' - liquid outlet (2-phase separator)
        - 'separator.oil' - oil outlet (3-phase separator)
        - 'separator.water' or 'separator.aqueous' - water outlet

        Splitters and Manifolds:
        - 'splitter.split_0', 'splitter.split_1', etc. - numbered outlets
        - 'manifold.split_0', 'manifold.split_1', etc. - numbered outlets
        - 'manifold.mixed' - mixed stream (before splitting)

        Other:
        - 'virtual_stream.out' - output from VirtualStream/Recycle

        Examples:
            >>> builder.add_compressor('comp', 'sep.gas', pressure=100)
            >>> builder.add_pump('pump', 'sep.oil', pressure=50)
            >>> builder.add_mixer('mixer', inlets=['feed', 'recycle_guess.out'])
            >>> builder.add_valve('valve1', 'splitter.split_0', pressure=10)
            >>> builder.add_compressor('comp1', 'manifold.split_0', pressure=100)
        """
        if isinstance(ref, str):
            # Check for dot notation (e.g., 'separator.gas')
            if "." in ref:
                parts = ref.split(".", 1)
                equip_name = parts[0]
                outlet_type = parts[1].lower()

                equip = self.equipment.get(equip_name)
                if equip is None:
                    raise ValueError(f"Equipment '{equip_name}' not found")

                # Handle VirtualStream .out notation
                if outlet_type == "out":
                    if hasattr(equip, "getOutStream"):
                        return equip.getOutStream()
                    elif hasattr(equip, "getOutletStream"):
                        return equip.getOutletStream()
                    raise ValueError(
                        f"Equipment '{equip_name}' does not have an output stream method"
                    )

                # Handle manifold mixed stream outlet (.mixed)
                if outlet_type == "mixed":
                    if hasattr(equip, "getMixedStream"):
                        return equip.getMixedStream()
                    raise ValueError(
                        f"Equipment '{equip_name}' does not have a mixed stream outlet"
                    )

                # Handle splitter/manifold outlets (.split_0, .split_1, etc.)
                if outlet_type.startswith("split_"):
                    if hasattr(equip, "getSplitStream"):
                        try:
                            index = int(outlet_type.replace("split_", ""))
                            split_stream = equip.getSplitStream(index)
                            if split_stream is not None:
                                return split_stream
                            raise ValueError(
                                f"Equipment '{equip_name}' does not have outlet at index {index}"
                            )
                        except ValueError as e:
                            if "does not have outlet" in str(e):
                                raise
                            raise ValueError(
                                f"Invalid splitter outlet format: '{outlet_type}'. Use 'split_0', 'split_1', etc."
                            )
                    raise ValueError(
                        f"Equipment '{equip_name}' is not a splitter or manifold"
                    )

                # Map outlet type to method
                outlet_methods = {
                    "gas": ["getGasOutStream", "getOutletStream"],
                    "vapor": ["getGasOutStream", "getOutletStream"],
                    "liquid": ["getLiquidOutStream", "getOilOutStream"],
                    "oil": ["getOilOutStream", "getLiquidOutStream"],
                    "water": ["getWaterOutStream", "getAqueousOutStream"],
                    "aqueous": ["getWaterOutStream", "getAqueousOutStream"],
                }

                if outlet_type not in outlet_methods:
                    raise ValueError(
                        f"Unknown outlet type '{outlet_type}'. "
                        f"Valid types: {list(outlet_methods.keys()) + ['out', 'mixed', 'split_N']}"
                    )

                for method_name in outlet_methods[outlet_type]:
                    if hasattr(equip, method_name):
                        return getattr(equip, method_name)()

                raise ValueError(
                    f"Equipment '{equip_name}' does not have a '{outlet_type}' outlet"
                )

            # Standard lookup without dot notation
            equip = self.equipment.get(ref)
            if equip is None:
                raise ValueError(f"Equipment '{ref}' not found")
            if hasattr(equip, "getOutletStream"):
                return equip.getOutletStream()
            elif hasattr(equip, "getOutStream"):
                return equip.getOutStream()
            elif hasattr(equip, "getGasOutStream"):
                return equip.getGasOutStream()
            return equip
        return ref

    def add_stream(
        self,
        name: str,
        thermo_system: Any,
        temperature: float = None,
        pressure: float = None,
        flow_rate: float = None,
        flow_unit: str = "kg/sec",
    ) -> "ProcessBuilder":
        """
        Add a stream to the process.

        Args:
            name: Name of the stream.
            thermo_system: Fluid/thermodynamic system.
            temperature: Optional temperature in Kelvin.
            pressure: Optional pressure in bara.
            flow_rate: Optional flow rate. If not specified, uses the flow rate
                already set on the fluid.
            flow_unit: Unit for flow rate (default 'kg/sec'). Common units include
                'kg/sec', 'kg/hr', 'MSm3/day', 'Sm3/day', 'mole/sec'.

        Returns:
            Self for method chaining.

        Example:
            >>> process = (ProcessBuilder("Test")
            ...     .add_stream('inlet', feed, flow_rate=10.0, flow_unit='MSm3/day')
            ...     .run())
        """
        if temperature is not None:
            thermo_system.setTemperature(temperature)
        if pressure is not None:
            thermo_system.setPressure(pressure)
        if flow_rate is not None:
            thermo_system.setTotalFlowRate(flow_rate, flow_unit)
        s = jneqsim.process.equipment.stream.Stream(name, thermo_system)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_separator(
        self, name: str, inlet: str, three_phase: bool = False
    ) -> "ProcessBuilder":
        """Add a separator to the process."""
        inlet_stream = self._get_outlet(inlet)
        if three_phase:
            sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(
                name, inlet_stream
            )
        else:
            sep = jneqsim.process.equipment.separator.Separator(name, inlet_stream)
        self.equipment[name] = sep
        self.process.add(sep)
        return self

    def add_compressor(
        self, name: str, inlet: str, pressure: float = None, efficiency: float = 0.75
    ) -> "ProcessBuilder":
        """Add a compressor to the process."""
        inlet_stream = self._get_outlet(inlet)
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        if pressure is not None:
            comp.setOutletPressure(pressure)
        comp.setIsentropicEfficiency(efficiency)
        self.equipment[name] = comp
        self.process.add(comp)
        return self

    def add_pump(
        self, name: str, inlet: str, pressure: float = None, efficiency: float = 0.75
    ) -> "ProcessBuilder":
        """Add a pump to the process."""
        inlet_stream = self._get_outlet(inlet)
        p = jneqsim.process.equipment.pump.Pump(name, inlet_stream)
        if pressure is not None:
            p.setOutletPressure(pressure)
        p.setIsentropicEfficiency(efficiency)
        self.equipment[name] = p
        self.process.add(p)
        return self

    def add_expander(
        self, name: str, inlet: str, pressure: float = None
    ) -> "ProcessBuilder":
        """Add an expander to the process."""
        inlet_stream = self._get_outlet(inlet)
        exp = jneqsim.process.equipment.expander.Expander(name, inlet_stream)
        if pressure is not None:
            exp.setOutletPressure(pressure)
        self.equipment[name] = exp
        self.process.add(exp)
        return self

    def add_valve(
        self, name: str, inlet: str, pressure: float = None
    ) -> "ProcessBuilder":
        """Add a valve to the process."""
        inlet_stream = self._get_outlet(inlet)
        v = jneqsim.process.equipment.valve.ThrottlingValve(name, inlet_stream)
        if pressure is not None:
            v.setOutletPressure(pressure)
        self.equipment[name] = v
        self.process.add(v)
        return self

    def add_heater(
        self, name: str, inlet: str, temperature: float = None, duty: float = None
    ) -> "ProcessBuilder":
        """Add a heater to the process."""
        inlet_stream = self._get_outlet(inlet)
        h = jneqsim.process.equipment.heatexchanger.Heater(name, inlet_stream)
        if temperature is not None:
            h.setOutTemperature(temperature)
        if duty is not None:
            h.setDuty(duty)
        self.equipment[name] = h
        self.process.add(h)
        return self

    def add_cooler(
        self, name: str, inlet: str, temperature: float = None, duty: float = None
    ) -> "ProcessBuilder":
        """Add a cooler to the process."""
        inlet_stream = self._get_outlet(inlet)
        c = jneqsim.process.equipment.heatexchanger.Cooler(name, inlet_stream)
        if temperature is not None:
            c.setOutTemperature(temperature)
        if duty is not None:
            c.setDuty(duty)
        self.equipment[name] = c
        self.process.add(c)
        return self

    def add_mixer(self, name: str, inlets: List[str]) -> "ProcessBuilder":
        """
        Add a mixer to the process.

        Args:
            name: Name of the mixer.
            inlets: List of inlet stream/equipment names. Supports dot notation:
                - 'equipment_name' - default outlet
                - 'separator.gas', 'separator.liquid' - separator outlets
                - 'splitter.split_0', 'splitter.split_1' - splitter outlets
                - 'virtual_stream.out' - virtual stream outlet

        Returns:
            Self for method chaining.

        Examples:
            >>> builder.add_mixer('mixer', inlets=['stream1', 'stream2'])
            >>> builder.add_mixer('mix', inlets=['splitter.split_0', 'splitter.split_1'])
            >>> builder.add_mixer('recycle_mix', inlets=['feed', 'recycle_guess.out'])
        """
        m = jneqsim.process.equipment.mixer.Mixer(name)
        for inlet in inlets:
            inlet_stream = self._get_outlet(inlet)
            m.addStream(inlet_stream)
        self.equipment[name] = m
        self.process.add(m)
        return self

    def add_splitter(
        self,
        name: str,
        inlet: str,
        split_factors: List[float] = None,
        flow_rates: List[float] = None,
        flow_unit: str = "MSm3/day",
    ) -> "ProcessBuilder":
        """
        Add a splitter to the process.

        Args:
            name: Name of the splitter.
            inlet: Name of inlet stream/equipment.
            split_factors: List of split fractions (should sum to 1.0).
                Length determines number of outlets. Use this OR flow_rates.
            flow_rates: List of absolute flow rates for each outlet.
                Use -1 for one outlet to auto-calculate remainder.
            flow_unit: Unit for flow_rates (default 'MSm3/day').
                Options: 'MSm3/day', 'Sm3/day', 'kg/hr', 'kg/sec', 'mole/sec'

        Returns:
            Self for method chaining.

        Notes:
            Access splitter outlets using dot notation:
            - 'splitter.split_0' for first outlet
            - 'splitter.split_1' for second outlet
            - etc.

        Examples:
            # Using split factors (fractions)
            >>> builder.add_splitter('split', 'feed', split_factors=[0.5, 0.5])

            # Using absolute flow rates
            >>> builder.add_splitter('split', 'feed',
            ...     flow_rates=[5.0, 2.0], flow_unit='MSm3/day')

            # Auto-calculate one outlet (use -1)
            >>> builder.add_splitter('split', 'feed',
            ...     flow_rates=[-1, 1.0], flow_unit='MSm3/day')  # First gets remainder
        """
        inlet_stream = self._get_outlet(inlet)
        s = jneqsim.process.equipment.splitter.Splitter(name, inlet_stream)
        if flow_rates is not None:
            s.setFlowRates(flow_rates, flow_unit)
        elif split_factors is not None:
            s.setSplitFactors(split_factors)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_heat_exchanger(
        self, name: str, hot_inlet: str, cold_inlet: str, approach_temp: float = 10.0
    ) -> "ProcessBuilder":
        """Add a heat exchanger to the process."""
        hot_stream = self._get_outlet(hot_inlet)
        cold_stream = self._get_outlet(cold_inlet)
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(
            name, hot_stream, cold_stream
        )
        hx.setApproachTemperature(approach_temp)
        self.equipment[name] = hx
        self.process.add(hx)
        return self

    def add_pipe(
        self,
        name: str,
        inlet: str,
        length: float = 100.0,
        diameter: float = 0.1,
        elevation: float = 0.0,
    ) -> "ProcessBuilder":
        """Add a pipe to the process."""
        inlet_stream = self._get_outlet(inlet)
        p = jneqsim.process.equipment.pipeline.AdiabaticPipe(name, inlet_stream)
        p.setLength(length)
        p.setDiameter(diameter)
        if elevation != 0:
            p.setElevation(elevation)
        self.equipment[name] = p
        self.process.add(p)
        return self

    def add_gas_scrubber(self, name: str, inlet: str) -> "ProcessBuilder":
        """
        Add a gas scrubber to the process.

        Args:
            name: Name of the gas scrubber.
            inlet: Name of inlet equipment or stream.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        scrubber = jneqsim.process.equipment.separator.GasScrubber(name, inlet_stream)
        self.equipment[name] = scrubber
        self.process.add(scrubber)
        return self

    def add_recycle(
        self,
        name: str,
        inlet: str = None,
        outlet: str = None,
        tolerance: float = 1e-4,
        priority: int = None,
        max_iterations: int = None,
        downstream_property: str = None,
    ) -> "ProcessBuilder":
        """
        Add a recycle stream to the process.

        RECYCLE PATTERN EXPLANATION:
        ============================
        Recycles handle "streams that go back" in a process. The pattern is:

        1. Create a virtual stream FIRST as an initial guess for the recycle
        2. Build forward through the process (using virtual stream as input)
        3. Add the recycle to connect actual output back to virtual stream

        Example - Anti-surge recycle loop:
        ----------------------------------
        ```python
        builder = (
            ProcessBuilder()
            .add_stream("feed", fluid, flow_rate=100, flow_unit="kg/hr")
            # Step 1: Create virtual stream as initial guess for recycle
            .add_virtual_stream("recycle_guess", source="feed")
            # Configure it with estimated recycle flow
            .configure("recycle_guess", lambda vs: vs.setFlowRate(10.0, "kg/hr"))
            # Step 2: Mix feed with recycle guess
            .add_mixer("suction_mixer", inlets=["feed", "recycle_guess.out"])
            # Continue forward through process
            .add_compressor("compressor", inlet="suction_mixer", outlet_pressure=50.0)
            .add_cooler("aftercooler", inlet="compressor", outlet_temperature=30.0)
            .add_separator("separator", inlet="aftercooler")
            # Step 3: Add recycle connecting separator liquid back to virtual stream
            .add_recycle("antisurge_recycle",
                         inlet="separator.liquid",
                         outlet="recycle_guess.out",
                         tolerance=1e-6)
            .run()
        )
        ```

        Args:
            name: Name of the recycle.
            inlet: Name of inlet equipment (the actual stream to recycle).
            outlet: Name of outlet stream (typically a virtual stream's output).
            tolerance: Convergence tolerance for recycle iteration (default 1e-4).
            priority: Recycle priority (higher = later in solve order).
            max_iterations: Maximum iterations for this recycle.
            downstream_property: Property to pass downstream (e.g., "flow rate").

        Returns:
            Self for method chaining.
        """
        r = jneqsim.process.equipment.util.Recycle(name)
        if inlet is not None:
            inlet_stream = self._get_outlet(inlet)
            r.addStream(inlet_stream)
        if outlet is not None:
            outlet_stream = self._get_outlet(outlet)
            r.setOutletStream(outlet_stream)
        r.setTolerance(tolerance)
        if priority is not None:
            r.setPriority(priority)
        if max_iterations is not None:
            r.setMaximumIterations(max_iterations)
        if downstream_property is not None:
            r.setDownstreamProperty(downstream_property)
        self.equipment[name] = r
        self.process.add(r)
        return self

    def setup_recycle_loop(
        self,
        recycle_name: str,
        virtual_stream_name: str,
        source_stream: str,
        initial_flow: float = None,
        initial_flow_unit: str = "kg/hr",
    ) -> "ProcessBuilder":
        """
        Set up a recycle loop by creating a virtual stream for the initial guess.

        This is a convenience method that creates a virtual stream to be used
        as the recycle guess. You then build your process forward using this
        virtual stream, and finally connect the actual recycle back to it.

        Example workflow:
        -----------------
        ```python
        builder = (
            ProcessBuilder()
            .add_stream("feed", fluid, flow_rate=100, flow_unit="kg/hr")
            # Set up the recycle initial guess
            .setup_recycle_loop("my_recycle", "recycle_guess", "feed",
                                initial_flow=10.0, initial_flow_unit="kg/hr")
            # Mix feed with recycle
            .add_mixer("mixer", inlets=["feed", "recycle_guess.out"])
            # Process forward...
            .add_separator("sep", inlet="mixer")
            # Close the loop
            .close_recycle_loop("my_recycle", "sep.liquid", "recycle_guess.out")
            .run()
        )
        ```

        Args:
            recycle_name: Name for the recycle (used later in close_recycle_loop).
            virtual_stream_name: Name for the virtual stream.
            source_stream: Stream to use as template for composition.
            initial_flow: Initial guess for recycle flow rate.
            initial_flow_unit: Unit for the flow rate.

        Returns:
            Self for method chaining.
        """
        # Create the virtual stream
        source = self._get_outlet(source_stream)
        vs = jneqsim.process.equipment.stream.VirtualStream(virtual_stream_name, source)
        if initial_flow is not None:
            vs.setFlowRate(initial_flow, initial_flow_unit)
        self.equipment[virtual_stream_name] = vs
        self.process.add(vs)
        # Store recycle info for later
        if not hasattr(self, "_pending_recycles"):
            self._pending_recycles = {}
        self._pending_recycles[recycle_name] = virtual_stream_name
        return self

    def close_recycle_loop(
        self,
        recycle_name: str,
        inlet: str,
        outlet: str = None,
        tolerance: float = 1e-4,
        priority: int = None,
    ) -> "ProcessBuilder":
        """
        Close a recycle loop that was set up with setup_recycle_loop.

        This creates the actual Recycle object that connects the process
        output back to the virtual stream.

        Args:
            recycle_name: Name for the recycle (should match setup_recycle_loop).
            inlet: The actual stream to recycle (e.g., "separator.liquid").
            outlet: The virtual stream output (if None, uses the one from setup).
            tolerance: Convergence tolerance.
            priority: Recycle priority.

        Returns:
            Self for method chaining.
        """
        # Get the virtual stream from setup if outlet not specified
        if outlet is None:
            if (
                hasattr(self, "_pending_recycles")
                and recycle_name in self._pending_recycles
            ):
                vs_name = self._pending_recycles[recycle_name]
                outlet = f"{vs_name}.out"
            else:
                raise ValueError(
                    f"No outlet specified and no setup_recycle_loop found for '{recycle_name}'"
                )
        return self.add_recycle(
            recycle_name,
            inlet=inlet,
            outlet=outlet,
            tolerance=tolerance,
            priority=priority,
        )

    def add_distillation_column(
        self,
        name: str,
        trays: int = 5,
        reboiler: bool = True,
        condenser: bool = True,
    ) -> "ProcessBuilder":
        """
        Add a distillation column to the process.

        Args:
            name: Name of the column.
            trays: Number of theoretical trays.
            reboiler: Whether to include a reboiler.
            condenser: Whether to include a condenser.

        Returns:
            Self for method chaining.

        Note:
            Use get() to access the column and add feed streams, set temperatures, etc.
        """
        column = jneqsim.process.equipment.distillation.DistillationColumn(
            trays, reboiler, condenser
        )
        column.setName(name)
        self.equipment[name] = column
        self.process.add(column)
        return self

    def add_teg_absorber(self, name: str) -> "ProcessBuilder":
        """
        Add a simple TEG absorber to the process.

        Args:
            name: Name of the absorber.

        Returns:
            Self for method chaining.

        Note:
            Use get() to access the absorber and configure it (add streams, set parameters).
        """
        absorber = jneqsim.process.equipment.absorber.SimpleTEGAbsorber(name)
        self.equipment[name] = absorber
        self.process.add(absorber)
        return self

    def add_water_stripper(self, name: str) -> "ProcessBuilder":
        """
        Add a water stripper column to the process.

        Args:
            name: Name of the stripper.

        Returns:
            Self for method chaining.
        """
        column = jneqsim.process.equipment.absorber.WaterStripperColumn(name)
        self.equipment[name] = column
        self.process.add(column)
        return self

    def add_component_splitter(
        self, name: str, inlet: str, split_factors: List[float] = None
    ) -> "ProcessBuilder":
        """
        Add a component splitter to the process.

        A component splitter separates a stream by component, useful for
        creating pseudo-streams for specific components.

        Args:
            name: Name of the splitter.
            inlet: Name of inlet equipment.
            split_factors: List of split factors for each component (0 to 1).

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        splitter = jneqsim.process.equipment.splitter.ComponentSplitter(
            name, inlet_stream
        )
        if split_factors:
            splitter.setSplitFactors(split_factors)
        self.equipment[name] = splitter
        self.process.add(splitter)
        return self

    def add_saturator(self, name: str, inlet: str) -> "ProcessBuilder":
        """
        Add a stream saturator to the process.

        A saturator ensures the stream is at its saturation point.

        Args:
            name: Name of the saturator.
            inlet: Name of inlet equipment.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        sat = jneqsim.process.equipment.util.StreamSaturatorUtil(name, inlet_stream)
        self.equipment[name] = sat
        self.process.add(sat)
        return self

    def add_filter(self, name: str, inlet: str) -> "ProcessBuilder":
        """
        Add a filter to the process.

        Args:
            name: Name of the filter.
            inlet: Name of inlet equipment.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        f = jneqsim.process.equipment.filter.Filter(name, inlet_stream)
        self.equipment[name] = f
        self.process.add(f)
        return self

    def add_calculator(self, name: str) -> "ProcessBuilder":
        """
        Add a calculator to the process.

        Calculators allow custom calculations based on process variables.

        Args:
            name: Name of the calculator.

        Returns:
            Self for method chaining.

        Note:
            Use get() to access the calculator and configure it.
        """
        calc = jneqsim.process.equipment.util.Calculator(name)
        self.equipment[name] = calc
        self.process.add(calc)
        return self

    def add_setpoint(
        self,
        name: str,
        target: str,
        target_variable: str,
        source: str,
    ) -> "ProcessBuilder":
        """
        Add a setpoint controller to the process.

        A setpoint sets a variable in one unit based on another unit's property.

        Args:
            name: Name of the setpoint.
            target: Name of target equipment to control.
            target_variable: Variable name to control (e.g., 'pressure', 'temperature').
            source: Name of source equipment to read from.

        Returns:
            Self for method chaining.
        """
        target_eq = self.equipment.get(target)
        source_eq = self.equipment.get(source)
        if target_eq is None:
            raise ValueError(f"Target equipment '{target}' not found")
        if source_eq is None:
            raise ValueError(f"Source equipment '{source}' not found")
        sp = jneqsim.process.equipment.util.SetPoint(
            name, target_eq, target_variable, source_eq
        )
        self.equipment[name] = sp
        self.process.add(sp)
        return self

    def add_adjuster(
        self,
        name: str,
        adjust_equipment: str = None,
        adjust_variable: str = None,
        target_equipment: str = None,
        target_variable: str = None,
        target_value: float = None,
    ) -> "ProcessBuilder":
        """
        Add an adjuster to the process.

        An adjuster iteratively adjusts a variable to achieve a target value.

        Args:
            name: Name of the adjuster.
            adjust_equipment: Name of equipment with variable to adjust.
            adjust_variable: Variable name to adjust.
            target_equipment: Name of equipment with target variable.
            target_variable: Target variable name.
            target_value: Target value to achieve.

        Returns:
            Self for method chaining.
        """
        adj = jneqsim.process.equipment.util.Adjuster(name)
        if adjust_equipment is not None and adjust_variable is not None:
            adj_eq = self.equipment.get(adjust_equipment)
            if adj_eq is None:
                raise ValueError(f"Adjust equipment '{adjust_equipment}' not found")
            adj.setAdjustedVariable(adj_eq, adjust_variable)
        if target_equipment is not None and target_variable is not None:
            tgt_eq = self.equipment.get(target_equipment)
            if tgt_eq is None:
                raise ValueError(f"Target equipment '{target_equipment}' not found")
            adj.setTargetVariable(tgt_eq, target_variable)
        if target_value is not None:
            adj.setTargetValue(target_value)
        self.equipment[name] = adj
        self.process.add(adj)
        return self

    def add_ejector(
        self, name: str, motive_inlet: str, suction_inlet: str
    ) -> "ProcessBuilder":
        """
        Add an ejector to the process.

        Args:
            name: Name of the ejector.
            motive_inlet: Name of motive (high-pressure) stream equipment.
            suction_inlet: Name of suction (low-pressure) stream equipment.

        Returns:
            Self for method chaining.
        """
        motive_stream = self._get_outlet(motive_inlet)
        suction_stream = self._get_outlet(suction_inlet)
        ej = jneqsim.process.equipment.ejector.Ejector(
            name, motive_stream, suction_stream
        )
        self.equipment[name] = ej
        self.process.add(ej)
        return self

    def add_flare(self, name: str, inlet: str = None) -> "ProcessBuilder":
        """
        Add a flare to the process.

        Args:
            name: Name of the flare.
            inlet: Optional name of inlet equipment.

        Returns:
            Self for method chaining.
        """
        f = jneqsim.process.equipment.flare.Flare(name)
        if inlet is not None:
            inlet_stream = self._get_outlet(inlet)
            f.addStream(inlet_stream)
        self.equipment[name] = f
        self.process.add(f)
        return self

    def add_tank(self, name: str, inlet: str = None) -> "ProcessBuilder":
        """
        Add a tank to the process.

        Args:
            name: Name of the tank.
            inlet: Optional name of inlet equipment.

        Returns:
            Self for method chaining.
        """
        t = jneqsim.process.equipment.tank.Tank(name)
        if inlet is not None:
            inlet_stream = self._get_outlet(inlet)
            t.addStream(inlet_stream)
        self.equipment[name] = t
        self.process.add(t)
        return self

    def add_virtual_stream(
        self,
        name: str,
        source: str = None,
        flow_rate: float = None,
        flow_unit: str = "kg/hr",
        temperature: float = None,
        temperature_unit: str = "C",
        pressure: float = None,
        pressure_unit: str = "bara",
    ) -> "ProcessBuilder":
        """
        Add a virtual stream to the process.

        Virtual streams are used with recycling to create initial guesses
        for recycle convergence. They copy composition from a source stream
        but can have independent flow/T/P settings.

        USAGE WITH RECYCLES:
        ====================
        Virtual streams are essential for recycle loops. The pattern is:

        1. Create virtual stream as initial guess (copies composition from source)
        2. Use virtual_stream.out as input to equipment in the loop
        3. Create a Recycle that connects actual output back to virtual_stream.out

        Example:
        --------
        ```python
        builder = (
            ProcessBuilder()
            .add_stream("feed", fluid, flow_rate=100, flow_unit="kg/hr")
            # Virtual stream as recycle guess (small flow to start)
            .add_virtual_stream("recycle_guess", source="feed",
                                flow_rate=5.0, flow_unit="kg/hr")
            # Mix feed with recycle
            .add_mixer("mixer", inlets=["feed", "recycle_guess.out"])
            .add_separator("sep", inlet="mixer")
            # Connect separator liquid back to virtual stream
            .add_recycle("recycle", inlet="sep.liquid", outlet="recycle_guess.out")
            .run()
        )
        ```

        Args:
            name: Name of the virtual stream.
            source: Name of source stream to copy composition from.
            flow_rate: Initial flow rate guess.
            flow_unit: Unit for flow rate (default "kg/hr").
            temperature: Temperature (if different from source).
            temperature_unit: Unit for temperature (default "C").
            pressure: Pressure (if different from source).
            pressure_unit: Unit for pressure (default "bara").

        Returns:
            Self for method chaining.

        Note:
            Access the virtual stream's output with '.out' suffix in inlet parameters,
            e.g., 'virtual_stream_name.out' or just 'virtual_stream_name' (auto-detected).
        """
        if source is not None:
            source_stream = self._get_outlet(source)
            vs = jneqsim.process.equipment.stream.VirtualStream(name, source_stream)
        else:
            vs = jneqsim.process.equipment.stream.VirtualStream(name)
        if flow_rate is not None:
            vs.setFlowRate(flow_rate, flow_unit)
        if temperature is not None:
            vs.setTemperature(temperature, temperature_unit)
        if pressure is not None:
            vs.setPressure(pressure, pressure_unit)
        self.equipment[name] = vs
        self.process.add(vs)
        return self

    def add_water_stream(
        self,
        name: str,
        temperature: float = None,
        temperature_unit: str = "C",
        pressure: float = None,
        pressure_unit: str = "bara",
        flow_rate: float = None,
        flow_unit: str = "kg/hr",
    ) -> "ProcessBuilder":
        """
        Add a water stream to the process.

        Creates a stream containing pure water at specified conditions.

        Args:
            name: Name of the stream.
            temperature: Temperature value.
            temperature_unit: Unit for temperature (default 'C').
            pressure: Pressure value.
            pressure_unit: Unit for pressure (default 'bara').
            flow_rate: Flow rate value.
            flow_unit: Unit for flow rate (default 'kg/hr').

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_water_stream('water_feed', temperature=80.0, pressure=10.0, flow_rate=1000.0)
        """
        water_fluid = jneqsim.thermo.system.SystemSrkEos(273.15 + 25.0, 1.0)
        water_fluid.addComponent("water", 1.0)
        water_fluid.setMixingRule(2)
        water_fluid.init(0)

        s = jneqsim.process.equipment.stream.Stream(name, water_fluid)
        if temperature is not None:
            s.setTemperature(temperature, temperature_unit)
        if pressure is not None:
            s.setPressure(pressure, pressure_unit)
        if flow_rate is not None:
            s.setFlowRate(flow_rate, flow_unit)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_three_phase_separator(
        self,
        name: str,
        inlet: str = None,
        inlets: List[str] = None,
        entrainment: Dict[str, Any] = None,
        internal_diameter: float = None,
    ) -> "ProcessBuilder":
        """
        Add a three-phase separator to the process.

        Three-phase separators separate gas, oil, and water phases.

        Args:
            name: Name of the separator.
            inlet: Name of primary inlet equipment (for single inlet).
            inlets: List of inlet equipment names (for multiple inlets).
            entrainment: Optional entrainment settings dict with keys:
                - 'value': entrainment fraction
                - 'from_phase': source phase ('feed')
                - 'unit': unit type ('volume')
                - 'from': phase to entrain from ('aqueous', 'oil', 'gas')
                - 'to': phase to entrain to ('oil', 'gas', 'aqueous')
            internal_diameter: Optional internal diameter in meters.

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_three_phase_separator(
            ...     '1st_stage_sep',
            ...     inlet='feed_heater',
            ...     entrainment={'value': 0.001, 'from_phase': 'feed', 'unit': 'volume',
            ...                  'from': 'aqueous', 'to': 'oil'}
            ... )
        """
        if inlet is not None:
            inlet_stream = self._get_outlet(inlet)
            sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(
                name, inlet_stream
            )
        else:
            sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(name)

        # Add additional inlet streams
        if inlets is not None:
            for inlet_name in inlets:
                inlet_stream = self._get_outlet(inlet_name)
                sep.addStream(inlet_stream)

        if entrainment is not None:
            sep.setEntrainment(
                entrainment.get("value", 0.0),
                entrainment.get("from_phase", "feed"),
                entrainment.get("unit", "volume"),
                entrainment.get("from", "aqueous"),
                entrainment.get("to", "oil"),
            )

        if internal_diameter is not None:
            sep.setInternalDiameter(internal_diameter)

        self.equipment[name] = sep
        self.process.add(sep)
        return self

    def add_manifold(
        self,
        name: str,
        inlets: List[str] = None,
        split_factors: List[float] = None,
        flow_rates: List[float] = None,
        flow_unit: str = "MSm3/day",
    ) -> "ProcessBuilder":
        """
        Add a manifold to the process.

        A manifold combines multiple inlet streams (like a mixer) and then
        distributes to multiple outlets (like a splitter).

        Args:
            name: Name of the manifold.
            inlets: List of inlet equipment/stream names. Supports dot notation.
            split_factors: List of split fractions for each outlet (should sum to 1).
                Use this OR flow_rates.
            flow_rates: List of absolute flow rates for each outlet.
                Use -1 for one outlet to auto-calculate remainder.
            flow_unit: Unit for flow_rates (default 'MSm3/day').
                Options: 'MSm3/day', 'Sm3/day', 'kg/hr', 'kg/sec', 'mole/sec'

        Returns:
            Self for method chaining.

        Notes:
            Access manifold outlets using dot notation:
            - 'manifold.split_0' for first outlet
            - 'manifold.split_1' for second outlet
            - 'manifold.mixed' for the mixed stream (before splitting)

        Examples:
            # Using split factors
            >>> builder.add_manifold('prod_manifold',
            ...     inlets=['well1', 'well2', 'well3'],
            ...     split_factors=[0.5, 0.3, 0.2])

            # Using absolute flow rates
            >>> builder.add_manifold('prod_manifold',
            ...     inlets=['well1', 'well2'],
            ...     flow_rates=[10.0, 5.0], flow_unit='MSm3/day')

        Note:
            For manifolds, flow_rates are set on the internal splitter after
            the streams are mixed. Use -1 for one outlet to auto-calculate.
        """
        m = jneqsim.process.equipment.manifold.Manifold(name)
        if inlets is not None:
            for inlet in inlets:
                inlet_stream = self._get_outlet(inlet)
                m.addStream(inlet_stream)
        if flow_rates is not None:
            # Manifold uses internal splitter - access via localsplitter field
            # First set split factors to initialize the right number of outlets
            m.setSplitFactors([1.0 / len(flow_rates)] * len(flow_rates))
            # Then set flow rates on internal splitter
            if hasattr(m, "localsplitter"):
                m.localsplitter.setFlowRates(flow_rates, flow_unit)
        elif split_factors is not None:
            m.setSplitFactors(split_factors)
        self.equipment[name] = m
        self.process.add(m)
        return self

    def add_compressor_with_chart(
        self,
        name: str,
        inlet: str,
        outlet_pressure: float = None,
        pressure_unit: str = "bara",
        polytopic_efficiency: float = 0.75,
        use_polytropic: bool = True,
        speed: float = None,
        chart_conditions: Any = None,
        chart_speeds: List[float] = None,
        chart_flow: List[List[float]] = None,
        chart_head: List[List[float]] = None,
        chart_eff_flow: List[List[float]] = None,
        chart_efficiency: List[List[float]] = None,
        surge_flow: List[float] = None,
        surge_head: List[float] = None,
        use_chart: bool = False,
        use_energy_efficiency_chart: bool = True,
    ) -> "ProcessBuilder":
        """
        Add a compressor with performance charts to the process.

        This method provides full control over compressor performance curves
        including surge curves.

        Args:
            name: Name of the compressor.
            inlet: Name of inlet equipment.
            outlet_pressure: Outlet pressure.
            pressure_unit: Unit for pressure (default 'bara').
            polytopic_efficiency: Polytropic efficiency (0-1).
            use_polytropic: Use polytropic calculation (default True).
            speed: Rotational speed in RPM.
            chart_conditions: Reference conditions for chart.
            chart_speeds: List of speeds for chart curves.
            chart_flow: Nested list of flow values for each speed.
            chart_head: Nested list of head values for each speed.
            chart_eff_flow: Nested list of flow values for efficiency.
            chart_efficiency: Nested list of efficiency values.
            surge_flow: Flow values for surge curve.
            surge_head: Head values for surge curve.
            use_chart: Whether to use compressor chart (default False).
            use_energy_efficiency_chart: Use energy efficiency chart (default True).

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        comp.setCompressorChartType("interpolate and extrapolate")

        if use_polytropic:
            comp.setUsePolytropicCalc(True)
            comp.setPolytropicEfficiency(polytopic_efficiency)
        else:
            comp.setIsentropicEfficiency(polytopic_efficiency)

        if outlet_pressure is not None:
            comp.setOutletPressure(outlet_pressure, pressure_unit)

        if speed is not None:
            comp.setSpeed(speed)

        # Set performance chart if provided
        if chart_conditions is not None and chart_speeds is not None:
            comp.getCompressorChart().setCurves(
                chart_conditions,
                chart_speeds,
                chart_flow,
                chart_head,
                chart_eff_flow,
                chart_efficiency,
            )

        comp.getCompressorChart().setUseCompressorChart(use_chart)
        comp.setUseEnergyEfficiencyChart(use_energy_efficiency_chart)

        # Set surge curve if provided
        if (
            surge_flow is not None
            and surge_head is not None
            and chart_conditions is not None
        ):
            comp.getCompressorChart().getSurgeCurve().setCurve(
                chart_conditions, surge_flow, surge_head
            )

        self.equipment[name] = comp
        self.process.add(comp)
        return self

    def add_valve_with_options(
        self,
        name: str,
        inlet: str,
        outlet_pressure: float = None,
        delta_pressure: float = None,
        pressure_unit: str = "bara",
        percent_opening: float = None,
        tag_name: str = None,
    ) -> "ProcessBuilder":
        """
        Add a throttling valve with extended options.

        Args:
            name: Name of the valve.
            inlet: Name of inlet equipment.
            outlet_pressure: Outlet pressure value.
            delta_pressure: Pressure drop across valve (alternative to outlet_pressure).
            pressure_unit: Unit for pressure (default 'bara').
            percent_opening: Valve opening percentage (0-100).
            tag_name: Equipment tag for identification.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        v = jneqsim.process.equipment.valve.ThrottlingValve(name, inlet_stream)

        if outlet_pressure is not None:
            v.setOutletPressure(outlet_pressure, pressure_unit)
        elif delta_pressure is not None:
            v.setDeltaPressure(delta_pressure, pressure_unit)

        if percent_opening is not None:
            v.setPercentValveOpening(percent_opening)

        if tag_name is not None:
            v.setTagName(tag_name)

        self.equipment[name] = v
        self.process.add(v)
        return self

    def add_splitter_with_flowrates(
        self,
        name: str,
        inlet: str,
        flow_rates: List[float] = None,
        flow_unit: str = "kg/hr",
        split_factors: List[float] = None,
    ) -> "ProcessBuilder":
        """
        Add a splitter with flow rate specifications.

        Use -1 in flow_rates to indicate "remainder" (balance stream).

        Args:
            name: Name of the splitter.
            inlet: Name of inlet equipment.
            flow_rates: List of flow rates for each split (-1 for remainder).
            flow_unit: Unit for flow rates (default 'kg/hr').
            split_factors: Alternative: split by fractions (0 to 1 each).

        Returns:
            Self for method chaining.

        Example:
            >>> # Split with specific flow rate and remainder
            >>> builder.add_splitter_with_flowrates('splitter', 'stream',
            ...                                     flow_rates=[-1, 100.0])
        """
        inlet_stream = self._get_outlet(inlet)
        spl = jneqsim.process.equipment.splitter.Splitter(name, inlet_stream)

        if flow_rates is not None:
            spl.setFlowRates(flow_rates, flow_unit)
        elif split_factors is not None:
            spl.setSplitFactors(split_factors)

        self.equipment[name] = spl
        self.process.add(spl)
        return self

    def add_gas_scrubber_with_options(
        self,
        name: str,
        inlet: str,
        internal_diameter: float = None,
        orientation: str = None,
    ) -> "ProcessBuilder":
        """
        Add a gas scrubber with configuration options.

        Args:
            name: Name of the scrubber.
            inlet: Name of inlet equipment.
            internal_diameter: Internal diameter in meters.
            orientation: 'vertical' or 'horizontal'.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        scrubber = jneqsim.process.equipment.separator.GasScrubber(name, inlet_stream)

        if internal_diameter is not None:
            scrubber.setInternalDiameter(internal_diameter)

        if orientation is not None:
            scrubber.setOrientation(orientation)

        self.equipment[name] = scrubber
        self.process.add(scrubber)
        return self

    def add_stream_from_outlet(
        self,
        name: str,
        source: str,
    ) -> "ProcessBuilder":
        """
        Add a named stream from another equipment's outlet.

        Useful for creating named reference streams from separator outlets
        or other equipment.

        Args:
            name: Name of the new stream.
            source: Source equipment with optional outlet spec (e.g., 'sep.water').

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_stream_from_outlet('water_product', 'separator.water')
        """
        source_stream = self._get_outlet(source)
        s = jneqsim.process.equipment.stream.Stream(name, source_stream)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_process(
        self,
        sub_process: "ProcessBuilder",
        prefix: str = "",
    ) -> "ProcessBuilder":
        """
        Add all equipment from another ProcessBuilder as a sub-process.

        This allows building modular process sections that can be combined.

        Args:
            sub_process: Another ProcessBuilder instance to incorporate.
            prefix: Optional prefix to add to all equipment names.

        Returns:
            Self for method chaining.

        Example:
            >>> compression_train = (ProcessBuilder("Compression")
            ...     .add_compressor('comp1', 'inlet', pressure=50)
            ...     .add_cooler('cooler1', 'comp1', temperature=303))
            >>> main_process = (ProcessBuilder("Main")
            ...     .add_stream('feed', fluid)
            ...     .add_process(compression_train, prefix='train1_'))
        """
        for eq_name, eq in sub_process.equipment.items():
            new_name = f"{prefix}{eq_name}" if prefix else eq_name
            self.equipment[new_name] = eq
            self.process.add(eq)
        return self

    def configure(self, equipment_name: str, **kwargs) -> "ProcessBuilder":
        """
        Configure an existing equipment item with additional settings.

        This method allows setting arbitrary properties on equipment
        after it has been added to the process.

        Args:
            equipment_name: Name of the equipment to configure.
            **kwargs: Property-value pairs to set. Property names should
                match Java setter methods (without 'set' prefix).

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_stream('feed', fluid)
            >>> builder.configure('feed', Temperature=(80, 'C'), Pressure=(10, 'bara'))
        """
        eq = self.equipment.get(equipment_name)
        if eq is None:
            raise ValueError(f"Equipment '{equipment_name}' not found")

        for prop, value in kwargs.items():
            setter_name = f"set{prop}"
            if hasattr(eq, setter_name):
                setter = getattr(eq, setter_name)
                if isinstance(value, (tuple, list)):
                    setter(*value)
                else:
                    setter(value)
            else:
                raise ValueError(
                    f"Equipment '{equipment_name}' has no setter '{setter_name}'"
                )

        return self

    # ============ PIPELINE EQUIPMENT ============

    def add_beggs_brill_pipe(
        self,
        name: str,
        inlet: str,
        length: float = 100.0,
        diameter: float = 0.1,
        elevation: float = 0.0,
        wall_roughness: float = 1e-5,
        increments: int = 10,
    ) -> "ProcessBuilder":
        """
        Add a Beggs and Brill pipeline to the process.

        Beggs-Brill is a multiphase flow correlation commonly used for
        oil and gas pipelines.

        Args:
            name: Name of the pipe.
            inlet: Name of inlet equipment.
            length: Pipe length in meters (default 100.0).
            diameter: Pipe internal diameter in meters (default 0.1).
            elevation: Elevation change in meters (default 0.0).
            wall_roughness: Pipe wall roughness in meters (default 1e-5).
            increments: Number of calculation increments (default 10).

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        p = jneqsim.process.equipment.pipeline.PipeBeggsAndBrills(name, inlet_stream)
        p.setLength(length)
        p.setDiameter(diameter)
        p.setElevation(elevation)
        p.setPipeWallRoughness(wall_roughness)
        p.setNumberOfIncrements(increments)
        self.equipment[name] = p
        self.process.add(p)
        return self

    def add_two_phase_pipe(
        self,
        name: str,
        inlet: str,
        length: float = 100.0,
        diameter: float = 0.1,
        elevation: float = 0.0,
    ) -> "ProcessBuilder":
        """
        Add a two-phase pipeline to the process.

        Args:
            name: Name of the pipe.
            inlet: Name of inlet equipment.
            length: Pipe length in meters (default 100.0).
            diameter: Pipe internal diameter in meters (default 0.1).
            elevation: Elevation change in meters (default 0.0).

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        p = jneqsim.process.equipment.pipeline.TwoPhasePipeLine(name, inlet_stream)
        p.setLength(length)
        p.setDiameter(diameter)
        if elevation != 0:
            p.setElevation(elevation)
        self.equipment[name] = p
        self.process.add(p)
        return self

    # ============ MEASUREMENT DEVICES ============

    def add_pressure_transmitter(
        self,
        name: str,
        inlet: str,
        unit: str = "bara",
        min_value: float = 0.0,
        max_value: float = 100.0,
    ) -> "ProcessBuilder":
        """
        Add a pressure transmitter to the process.

        Args:
            name: Name of the transmitter.
            inlet: Name of stream to measure.
            unit: Pressure unit (default 'bara').
            min_value: Minimum value for scaling.
            max_value: Maximum value for scaling.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        pt = jneqsim.process.measurementdevice.PressureTransmitter(inlet_stream)
        pt.setName(name)
        pt.setUnit(unit)
        pt.setMinimumValue(min_value)
        pt.setMaximumValue(max_value)
        self.equipment[name] = pt
        self.process.add(pt)
        return self

    def add_level_transmitter(
        self,
        name: str,
        separator: str,
        min_value: float = 0.0,
        max_value: float = 1.0,
    ) -> "ProcessBuilder":
        """
        Add a level transmitter to the process.

        Args:
            name: Name of the transmitter.
            separator: Name of separator to measure level.
            min_value: Minimum value for scaling (default 0.0).
            max_value: Maximum value for scaling (default 1.0).

        Returns:
            Self for method chaining.
        """
        sep = self.equipment.get(separator)
        if sep is None:
            raise ValueError(f"Separator '{separator}' not found")
        lt = jneqsim.process.measurementdevice.LevelTransmitter(sep)
        lt.setName(name)
        lt.setMinimumValue(min_value)
        lt.setMaximumValue(max_value)
        self.equipment[name] = lt
        self.process.add(lt)
        return self

    def add_flow_transmitter(
        self,
        name: str,
        inlet: str,
        unit: str = "kg/hr",
        min_value: float = 0.0,
        max_value: float = 1000.0,
    ) -> "ProcessBuilder":
        """
        Add a volume/mass flow transmitter to the process.

        Args:
            name: Name of the transmitter.
            inlet: Name of stream to measure.
            unit: Flow unit (default 'kg/hr').
            min_value: Minimum value for scaling.
            max_value: Maximum value for scaling.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        ft = jneqsim.process.measurementdevice.VolumeFlowTransmitter(inlet_stream)
        ft.setName(name)
        ft.setUnit(unit)
        ft.setMinimumValue(min_value)
        ft.setMaximumValue(max_value)
        self.equipment[name] = ft
        self.process.add(ft)
        return self

    def add_temperature_transmitter(
        self,
        name: str,
        inlet: str,
        unit: str = "C",
        min_value: float = -50.0,
        max_value: float = 200.0,
    ) -> "ProcessBuilder":
        """
        Add a temperature transmitter to the process.

        Args:
            name: Name of the transmitter.
            inlet: Name of stream to measure.
            unit: Temperature unit (default 'C').
            min_value: Minimum value for scaling.
            max_value: Maximum value for scaling.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        tt = jneqsim.process.measurementdevice.TemperatureTransmitter(inlet_stream)
        tt.setName(name)
        tt.setUnit(unit)
        tt.setMinimumValue(min_value)
        tt.setMaximumValue(max_value)
        self.equipment[name] = tt
        self.process.add(tt)
        return self

    # ============ CONTROLLERS ============

    def add_pid_controller(
        self,
        name: str,
        transmitter: str,
        setpoint: float,
        kp: float = 1.0,
        ti: float = 100.0,
        td: float = 0.0,
        reverse_acting: bool = False,
    ) -> "ProcessBuilder":
        """
        Add a PID controller to the process.

        Args:
            name: Name of the controller.
            transmitter: Name of transmitter to use as input.
            setpoint: Controller setpoint value.
            kp: Proportional gain (default 1.0).
            ti: Integral time constant (default 100.0).
            td: Derivative time constant (default 0.0).
            reverse_acting: If True, controller output decreases when
                process variable increases (default False).

        Returns:
            Self for method chaining.

        Note:
            After adding, use builder.get(name) to access the controller and
            attach it to equipment with equipment.setController(controller).
        """
        trans = self.equipment.get(transmitter)
        if trans is None:
            raise ValueError(f"Transmitter '{transmitter}' not found")
        ctrl = jneqsim.process.controllerdevice.ControllerDeviceBaseClass(name)
        ctrl.setTransmitter(trans)
        ctrl.setControllerSetPoint(setpoint)
        ctrl.setControllerParameters(kp, ti, td)
        ctrl.setReverseActing(reverse_acting)
        self.equipment[name] = ctrl
        # Note: Controllers are not added to process.add() in NeqSim
        # They are attached to equipment using equipment.setController()
        return self

    # ============ FLOW UTILITIES ============

    def add_flow_setter(
        self,
        name: str,
        inlet: str,
        gas_flow: float = None,
        oil_flow: float = None,
        water_flow: float = None,
        gas_unit: str = "Sm3/day",
        oil_unit: str = "m3/hr",
        water_unit: str = "m3/hr",
    ) -> "ProcessBuilder":
        """
        Add a flow setter to the process.

        Flow setters adjust the composition and flow rates of a stream
        to match specified gas, oil, and water rates.

        Args:
            name: Name of the flow setter.
            inlet: Name of inlet equipment.
            gas_flow: Desired gas flow rate.
            oil_flow: Desired oil flow rate.
            water_flow: Desired water flow rate.
            gas_unit: Gas flow unit (default 'Sm3/day').
            oil_unit: Oil flow unit (default 'm3/hr').
            water_unit: Water flow unit (default 'm3/hr').

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        fs = jneqsim.process.equipment.util.FlowSetter(name, inlet_stream)
        if gas_flow is not None:
            fs.setGasFlowRate(gas_flow, gas_unit)
        if oil_flow is not None:
            fs.setOilFlowRate(oil_flow, oil_unit)
        if water_flow is not None:
            fs.setWaterFlowRate(water_flow, water_unit)
        self.equipment[name] = fs
        self.process.add(fs)
        return self

    def add_flow_rate_adjuster(
        self,
        name: str,
        inlet: str,
        gas_flow: float = None,
        oil_flow: float = None,
        water_flow: float = None,
        unit: str = "Sm3/hr",
    ) -> "ProcessBuilder":
        """
        Add a flow rate adjuster to the process.

        Flow rate adjusters modify stream composition to achieve
        desired phase flow rates.

        Args:
            name: Name of the flow rate adjuster.
            inlet: Name of inlet equipment.
            gas_flow: Desired gas flow rate.
            oil_flow: Desired oil flow rate.
            water_flow: Desired water flow rate (optional).
            unit: Flow rate unit for all phases (default 'Sm3/hr').

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        fra = jneqsim.process.equipment.util.FlowRateAdjuster(name, inlet_stream)
        if water_flow is not None:
            fra.setAdjustedFlowRates(gas_flow or 0.0, oil_flow or 0.0, water_flow, unit)
        elif gas_flow is not None or oil_flow is not None:
            fra.setAdjustedFlowRates(gas_flow or 0.0, oil_flow or 0.0, unit)
        self.equipment[name] = fra
        self.process.add(fra)
        return self

    # ============ STREAM VARIANTS ============

    def add_neq_stream(
        self,
        name: str,
        thermo_system: Any,
        temperature: float = None,
        pressure: float = None,
        flow_rate: float = None,
        flow_unit: str = "kg/sec",
    ) -> "ProcessBuilder":
        """
        Add a non-equilibrium stream to the process.

        NeqStream uses non-equilibrium thermodynamics for better accuracy
        in some conditions.

        Args:
            name: Name of the stream.
            thermo_system: Fluid/thermodynamic system.
            temperature: Optional temperature in Kelvin.
            pressure: Optional pressure in bara.
            flow_rate: Optional flow rate.
            flow_unit: Unit for flow rate (default 'kg/sec').

        Returns:
            Self for method chaining.
        """
        if temperature is not None:
            thermo_system.setTemperature(temperature)
        if pressure is not None:
            thermo_system.setPressure(pressure)
        if flow_rate is not None:
            thermo_system.setTotalFlowRate(flow_rate, flow_unit)
        s = jneqsim.process.equipment.stream.NeqStream(name, thermo_system)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_energy_stream(self, name: str, duty: float = 0.0) -> "ProcessBuilder":
        """
        Add an energy stream to the process.

        Energy streams are used to connect heat/work flows between equipment.

        Args:
            name: Name of the energy stream.
            duty: Initial energy/duty in kW (default 0.0).

        Returns:
            Self for method chaining.
        """
        es = jneqsim.process.equipment.stream.EnergyStream(name)
        if duty != 0.0:
            es.setDuty(duty)
        self.equipment[name] = es
        self.process.add(es)
        return self

    # ============ ENHANCED SEPARATOR ============

    def add_separator_with_dimensions(
        self,
        name: str,
        inlet: str,
        three_phase: bool = False,
        length: float = None,
        diameter: float = None,
        liquid_level: float = None,
        orientation: str = None,
    ) -> "ProcessBuilder":
        """
        Add a separator with physical dimensions to the process.

        Used for dynamic simulations and mechanical design calculations.

        Args:
            name: Name of the separator.
            inlet: Name of inlet equipment.
            three_phase: If True, creates a ThreePhaseSeparator.
            length: Separator length in meters.
            diameter: Internal diameter in meters.
            liquid_level: Initial liquid level (0-1 fraction).
            orientation: 'horizontal' or 'vertical'.

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        if three_phase:
            sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(
                name, inlet_stream
            )
        else:
            sep = jneqsim.process.equipment.separator.Separator(name, inlet_stream)

        if length is not None:
            sep.setSeparatorLength(length)
        if diameter is not None:
            sep.setInternalDiameter(diameter)
        if liquid_level is not None:
            sep.setLiquidLevel(liquid_level)
        if orientation is not None:
            sep.setOrientation(orientation)
        self.equipment[name] = sep
        self.process.add(sep)
        return self

    # ============ ENHANCED COMPRESSOR ============

    def add_polytopic_compressor(
        self,
        name: str,
        inlet: str,
        pressure: float = None,
        polytopic_efficiency: float = 0.75,
        use_polytopic_calc: bool = True,
    ) -> "ProcessBuilder":
        """
        Add a compressor using polytropic calculation method.

        Args:
            name: Name of the compressor.
            inlet: Name of inlet equipment.
            pressure: Outlet pressure in bara.
            polytopic_efficiency: Polytropic efficiency (0-1, default 0.75).
            use_polytopic_calc: If True, use polytropic calculation (default True).

        Returns:
            Self for method chaining.
        """
        inlet_stream = self._get_outlet(inlet)
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        if pressure is not None:
            comp.setOutletPressure(pressure)
        comp.setPolytropicEfficiency(polytopic_efficiency)
        comp.setUsePolytropicCalc(use_polytopic_calc)
        self.equipment[name] = comp
        self.process.add(comp)
        return self

    # ============ MIXERS ============

    def add_static_mixer(self, name: str, inlets: List[str] = None) -> "ProcessBuilder":
        """
        Add a static mixer to the process.

        Static mixers instantaneously mix streams without pressure drop.

        Args:
            name: Name of the mixer.
            inlets: List of inlet equipment names (optional, can add later).

        Returns:
            Self for method chaining.
        """
        m = jneqsim.process.equipment.mixer.StaticMixer(name)
        if inlets:
            for inlet in inlets:
                inlet_stream = self._get_outlet(inlet)
                m.addStream(inlet_stream)
        self.equipment[name] = m
        self.process.add(m)
        return self

    def add_static_phase_mixer(
        self, name: str, inlets: List[str] = None
    ) -> "ProcessBuilder":
        """
        Add a static phase mixer to the process.

        Static phase mixers mix phases without equilibrium calculation.

        Args:
            name: Name of the mixer.
            inlets: List of inlet equipment names (optional).

        Returns:
            Self for method chaining.
        """
        m = jneqsim.process.equipment.mixer.StaticPhaseMixer(name)
        if inlets:
            for inlet in inlets:
                inlet_stream = self._get_outlet(inlet)
                m.addStream(inlet_stream)
        self.equipment[name] = m
        self.process.add(m)
        return self

    # ============ TRANSIENT SIMULATION HELPERS ============

    def set_transient_mode(
        self, equipment_name: str, steady_state: bool = False
    ) -> "ProcessBuilder":
        """
        Set equipment to transient calculation mode.

        Args:
            equipment_name: Name of equipment to configure.
            steady_state: If False, use transient calculation (default False).

        Returns:
            Self for method chaining.
        """
        eq = self.equipment.get(equipment_name)
        if eq is None:
            raise ValueError(f"Equipment '{equipment_name}' not found")
        if hasattr(eq, "setCalculateSteadyState"):
            eq.setCalculateSteadyState(steady_state)
        else:
            raise ValueError(
                f"Equipment '{equipment_name}' does not support transient mode"
            )
        return self

    def set_valve_opening(
        self, valve_name: str, opening: float, min_opening: float = None
    ) -> "ProcessBuilder":
        """
        Set valve opening percentage.

        Args:
            valve_name: Name of the valve.
            opening: Valve opening percentage (0-100).
            min_opening: Minimum valve opening percentage (optional).

        Returns:
            Self for method chaining.
        """
        valve = self.equipment.get(valve_name)
        if valve is None:
            raise ValueError(f"Valve '{valve_name}' not found")
        valve.setPercentValveOpening(opening)
        if min_opening is not None:
            valve.setMinimumValveOpening(min_opening)
        return self

    def attach_controller(
        self, equipment_name: str, controller_name: str
    ) -> "ProcessBuilder":
        """
        Attach a controller to equipment.

        Args:
            equipment_name: Name of equipment to attach controller to.
            controller_name: Name of the controller.

        Returns:
            Self for method chaining.
        """
        eq = self.equipment.get(equipment_name)
        if eq is None:
            raise ValueError(f"Equipment '{equipment_name}' not found")
        ctrl = self.equipment.get(controller_name)
        if ctrl is None:
            raise ValueError(f"Controller '{controller_name}' not found")
        if hasattr(eq, "setController"):
            eq.setController(ctrl)
        else:
            raise ValueError(
                f"Equipment '{equipment_name}' does not support controllers"
            )
        return self

    # ============ REACTOR ============

    def add_reactor(
        self,
        name: str,
        inlet: str = None,
        reactor_type: str = "gibbs",
    ) -> "ProcessBuilder":
        """
        Add a reactor to the process.

        Args:
            name: Name of the reactor.
            inlet: Name of inlet equipment (optional).
            reactor_type: Type of reactor - 'gibbs' (default), 'plug_flow', etc.

        Returns:
            Self for method chaining.
        """
        if reactor_type.lower() == "gibbs":
            r = jneqsim.process.equipment.reactor.GibbsReactor(name)
        else:
            r = jneqsim.process.equipment.reactor.GibbsReactor(name)

        if inlet is not None:
            inlet_stream = self._get_outlet(inlet)
            r.addStream(inlet_stream)
        self.equipment[name] = r
        self.process.add(r)
        return self

    # ============ ABSORPTION/STRIPPING ============

    def add_simple_absorber(
        self,
        name: str,
        gas_inlet: str = None,
        liquid_inlet: str = None,
        stages: int = 5,
    ) -> "ProcessBuilder":
        """
        Add a simple absorber to the process.

        Args:
            name: Name of the absorber.
            gas_inlet: Name of gas inlet stream.
            liquid_inlet: Name of liquid inlet stream (e.g., lean TEG).
            stages: Number of equilibrium stages (default 5).

        Returns:
            Self for method chaining.
        """
        absorber = jneqsim.process.equipment.absorber.SimpleTEGAbsorber(name)
        absorber.setNumberOfStages(stages)
        if gas_inlet is not None:
            gas_stream = self._get_outlet(gas_inlet)
            absorber.addGasInStream(gas_stream)
        if liquid_inlet is not None:
            liquid_stream = self._get_outlet(liquid_inlet)
            absorber.addSolventInStream(liquid_stream)
        self.equipment[name] = absorber
        self.process.add(absorber)
        return self

    # ============ WELL/RESERVOIR ============

    def add_well_stream(
        self,
        name: str,
        thermo_system: Any,
        gor: float = None,
        wc: float = None,
        flow_rate: float = None,
        flow_unit: str = "Sm3/day",
    ) -> "ProcessBuilder":
        """
        Add a well stream with GOR and water cut specifications.

        Args:
            name: Name of the stream.
            thermo_system: Fluid/thermodynamic system.
            gor: Gas-oil ratio (Sm3/Sm3).
            wc: Water cut (fraction 0-1).
            flow_rate: Oil flow rate.
            flow_unit: Flow rate unit (default 'Sm3/day').

        Returns:
            Self for method chaining.
        """
        s = jneqsim.process.equipment.stream.Stream(name, thermo_system)
        if flow_rate is not None:
            s.setFlowRate(flow_rate, flow_unit)
        self.equipment[name] = s
        self.process.add(s)
        return self

    def add_stream_to(self, target: str, source: str) -> "ProcessBuilder":
        """
        Add a stream from one equipment to another (e.g., adding feed to separator).

        Some equipment types like ThreePhaseSeparator allow multiple inlets.

        Args:
            target: Name of target equipment to add stream to.
            source: Name of source equipment (the stream to add).

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_stream_to('separator', 'recycle_stream')
        """
        target_eq = self.equipment.get(target)
        if target_eq is None:
            raise ValueError(f"Target equipment '{target}' not found")

        source_stream = self._get_outlet(source)

        if hasattr(target_eq, "addStream"):
            target_eq.addStream(source_stream)
        else:
            raise ValueError(f"Equipment '{target}' does not support addStream()")

        return self

    def add_equipment(
        self, equipment_type: str, name: str, **kwargs
    ) -> "ProcessBuilder":
        """
        Add equipment by type name. Useful for configuration-driven design.

        Args:
            equipment_type: Type of equipment ('stream', 'compressor', 'separator', etc.)
            name: Name of the equipment.
            **kwargs: Equipment-specific parameters.

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_equipment('compressor', 'comp1', inlet='inlet', pressure=100.0)
        """
        method_map = {
            "stream": self.add_stream,
            "separator": self.add_separator,
            "compressor": self.add_compressor,
            "pump": self.add_pump,
            "expander": self.add_expander,
            "valve": self.add_valve,
            "heater": self.add_heater,
            "cooler": self.add_cooler,
            "mixer": self.add_mixer,
            "splitter": self.add_splitter,
            "heat_exchanger": self.add_heat_exchanger,
            "pipe": self.add_pipe,
            "gas_scrubber": self.add_gas_scrubber,
            "recycle": self.add_recycle,
            "distillation_column": self.add_distillation_column,
            "teg_absorber": self.add_teg_absorber,
            "water_stripper": self.add_water_stripper,
            "component_splitter": self.add_component_splitter,
            "saturator": self.add_saturator,
            "filter": self.add_filter,
            "calculator": self.add_calculator,
            "setpoint": self.add_setpoint,
            "adjuster": self.add_adjuster,
            "ejector": self.add_ejector,
            "flare": self.add_flare,
            "tank": self.add_tank,
            "virtual_stream": self.add_virtual_stream,
            # Extended equipment types
            "water_stream": self.add_water_stream,
            "three_phase_separator": self.add_three_phase_separator,
            "manifold": self.add_manifold,
            "compressor_with_chart": self.add_compressor_with_chart,
            "valve_with_options": self.add_valve_with_options,
            "splitter_with_flowrates": self.add_splitter_with_flowrates,
            "gas_scrubber_with_options": self.add_gas_scrubber_with_options,
            "stream_from_outlet": self.add_stream_from_outlet,
            # Pipeline equipment
            "beggs_brill_pipe": self.add_beggs_brill_pipe,
            "two_phase_pipe": self.add_two_phase_pipe,
            # Measurement devices
            "pressure_transmitter": self.add_pressure_transmitter,
            "level_transmitter": self.add_level_transmitter,
            "flow_transmitter": self.add_flow_transmitter,
            "temperature_transmitter": self.add_temperature_transmitter,
            # Controllers
            "pid_controller": self.add_pid_controller,
            # Flow utilities
            "flow_setter": self.add_flow_setter,
            "flow_rate_adjuster": self.add_flow_rate_adjuster,
            # Stream variants
            "neq_stream": self.add_neq_stream,
            "energy_stream": self.add_energy_stream,
            # Enhanced equipment
            "separator_with_dimensions": self.add_separator_with_dimensions,
            "polytopic_compressor": self.add_polytopic_compressor,
            "polytropic_compressor": self.add_polytopic_compressor,  # Alias
            # Mixers
            "static_mixer": self.add_static_mixer,
            "static_phase_mixer": self.add_static_phase_mixer,
            # Reactor
            "reactor": self.add_reactor,
            "gibbs_reactor": self.add_reactor,
            # Absorption
            "simple_absorber": self.add_simple_absorber,
            # Well
            "well_stream": self.add_well_stream,
            # Recycle helpers
            "recycle_loop": self.setup_recycle_loop,
            "close_recycle": self.close_recycle_loop,
        }
        method = method_map.get(equipment_type.lower())
        if method is None:
            raise ValueError(
                f"Unknown equipment type: {equipment_type}. "
                f"Available: {list(method_map.keys())}"
            )
        return method(name, **kwargs)

    def add_from_config(
        self, equipment_list: List[Dict[str, Any]], fluids: Dict[str, Any] = None
    ) -> "ProcessBuilder":
        """
        Add multiple equipment items from a configuration list.

        Args:
            equipment_list: List of equipment configurations. Each item should have
                'type', 'name', and equipment-specific parameters.
            fluids: Dictionary mapping fluid names to fluid objects. Used for streams.

        Returns:
            Self for method chaining.

        Example:
            >>> config = [
            ...     {'type': 'stream', 'name': 'inlet', 'fluid': 'feed'},
            ...     {'type': 'compressor', 'name': 'comp1', 'inlet': 'inlet', 'pressure': 100.0}
            ... ]
            >>> builder.add_from_config(config, fluids={'feed': my_fluid})
        """
        fluids = fluids or {}

        for item in equipment_list:
            item = item.copy()  # Don't modify original
            eq_type = item.pop("type")
            name = item.pop("name")

            # Handle fluid reference for streams
            if eq_type == "stream" and "fluid" in item:
                fluid_name = item.pop("fluid")
                if fluid_name in fluids:
                    item["thermo_system"] = fluids[fluid_name]
                else:
                    raise ValueError(f"Fluid '{fluid_name}' not found in fluids dict")

            self.add_equipment(eq_type, name, **item)

        return self

    @classmethod
    def from_dict(
        cls, config: Dict[str, Any], fluids: Dict[str, Any] = None
    ) -> "ProcessBuilder":
        """
        Create a ProcessBuilder from a dictionary configuration.

        Args:
            config: Dictionary with 'name' and 'equipment' keys.
            fluids: Dictionary mapping fluid names to fluid objects.

        Returns:
            ProcessBuilder instance (not yet run).

        Example:
            >>> config = {
            ...     'name': 'Compression Train',
            ...     'equipment': [
            ...         {'type': 'stream', 'name': 'inlet', 'fluid': 'feed'},
            ...         {'type': 'separator', 'name': 'sep1', 'inlet': 'inlet'},
            ...         {'type': 'compressor', 'name': 'comp1', 'inlet': 'sep1', 'pressure': 100.0}
            ...     ]
            ... }
            >>> process = ProcessBuilder.from_dict(config, fluids={'feed': my_fluid}).run()
        """
        builder = cls(config.get("name", ""))
        if "equipment" in config:
            builder.add_from_config(config["equipment"], fluids)
        return builder

    @classmethod
    def from_json(
        cls, json_path: str, fluids: Dict[str, Any] = None
    ) -> "ProcessBuilder":
        """
        Create a ProcessBuilder from a JSON file.

        Args:
            json_path: Path to JSON configuration file.
            fluids: Dictionary mapping fluid names to fluid objects.

        Returns:
            ProcessBuilder instance (not yet run).

        Example:
            >>> # process_config.json:
            >>> # {
            >>> #   "name": "Compression Train",
            >>> #   "equipment": [
            >>> #     {"type": "stream", "name": "inlet", "fluid": "feed"},
            >>> #     {"type": "compressor", "name": "comp1", "inlet": "inlet", "pressure": 100}
            >>> #   ]
            >>> # }
            >>> process = ProcessBuilder.from_json('process_config.json',
            ...                                    fluids={'feed': my_fluid}).run()
        """
        json_file = _resolve_path_in_cwd(
            json_path, allowed_suffixes={".json"}, must_exist=True
        )
        with json_file.open("r", encoding="utf-8") as f:
            config = json.load(f)
        return cls.from_dict(config, fluids)

    @classmethod
    def from_yaml(
        cls, yaml_path: str, fluids: Dict[str, Any] = None
    ) -> "ProcessBuilder":
        """
        Create a ProcessBuilder from a YAML file.

        Requires PyYAML to be installed (pip install pyyaml).

        Args:
            yaml_path: Path to YAML configuration file.
            fluids: Dictionary mapping fluid names to fluid objects.

        Returns:
            ProcessBuilder instance (not yet run).

        Example:
            >>> # process_config.yaml:
            >>> # name: Compression Train
            >>> # equipment:
            >>> #   - type: stream
            >>> #     name: inlet
            >>> #     fluid: feed
            >>> #   - type: compressor
            >>> #     name: comp1
            >>> #     inlet: inlet
            >>> #     pressure: 100.0
            >>> process = ProcessBuilder.from_yaml('process_config.yaml',
            ...                                    fluids={'feed': my_fluid}).run()
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "PyYAML is required for YAML support. Install with: pip install pyyaml"
            )

        yaml_file = _resolve_path_in_cwd(
            yaml_path, allowed_suffixes=_YAML_SUFFIXES, must_exist=True
        )
        with yaml_file.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return cls.from_dict(config, fluids)

    def run(self) -> "ProcessBuilder":
        """
        Run the process simulation.

        Returns:
            Self for method chaining.
        """
        self.process.run()
        return self

    def get(self, name: str) -> Any:
        """
        Get equipment by name.

        Args:
            name: Name of the equipment.

        Returns:
            The equipment object.
        """
        return self.equipment.get(name)

    def get_process(self) -> Any:
        """Get the underlying ProcessSystem object."""
        return self.process

    def results_json(self) -> Dict[str, Any]:
        """
        Get simulation results as a JSON-compatible dictionary.

        Returns:
            Dictionary with all process results.

        Example:
            >>> process = ProcessBuilder("Test").add_stream(...).run()
            >>> results = process.results_json()
            >>> print(json.dumps(results, indent=2))
        """
        json_report = str(self.process.getReport_json())
        return json.loads(json_report)

    def results_dataframe(self) -> pd.DataFrame:
        """
        Get simulation results as a pandas DataFrame.

        Returns:
            DataFrame with equipment results including temperatures,
            pressures, flow rates, power, and duties.

        Example:
            >>> process = ProcessBuilder("Test").add_stream(...).run()
            >>> df = process.results_dataframe()
            >>> print(df)
        """
        rows = []
        for name, eq in self.equipment.items():
            row = {"Equipment": name}

            # Get outlet stream properties
            out_stream = None
            if hasattr(eq, "getOutletStream"):
                out_stream = eq.getOutletStream()
            elif hasattr(eq, "getOutStream"):
                out_stream = eq.getOutStream()
            elif hasattr(eq, "getGasOutStream"):
                out_stream = eq.getGasOutStream()

            if out_stream:
                try:
                    row["T_out (°C)"] = round(out_stream.getTemperature() - 273.15, 2)
                except:
                    pass
                try:
                    row["P_out (bara)"] = round(out_stream.getPressure(), 2)
                except:
                    pass
                try:
                    row["Flow (kg/hr)"] = round(out_stream.getFlowRate("kg/hr"), 1)
                except:
                    pass

            # Get power/duty
            if hasattr(eq, "getPower"):
                try:
                    row["Power (kW)"] = round(eq.getPower() / 1e3, 2)
                except:
                    pass
            if hasattr(eq, "getDuty"):
                try:
                    row["Duty (kW)"] = round(eq.getDuty() / 1e3, 2)
                except:
                    pass

            rows.append(row)

        return pd.DataFrame(rows)

    def print_results(self) -> "ProcessBuilder":
        """
        Print a formatted summary of simulation results.

        Returns:
            Self for method chaining.

        Example:
            >>> (ProcessBuilder("Test")
            ...     .add_stream('inlet', feed)
            ...     .add_compressor('comp1', 'inlet', pressure=100)
            ...     .run()
            ...     .print_results())
        """
        print(f"\n{'='*60}")
        print(f"Process Results: {self._name}")
        print(f"{'='*60}\n")

        for name, eq in self.equipment.items():
            print(f"📦 {name}")

            # Get outlet stream properties
            out_stream = None
            if hasattr(eq, "getOutletStream"):
                out_stream = eq.getOutletStream()
            elif hasattr(eq, "getOutStream"):
                out_stream = eq.getOutStream()
            elif hasattr(eq, "getGasOutStream"):
                out_stream = eq.getGasOutStream()

            if out_stream:
                try:
                    print(
                        f"   Temperature: {out_stream.getTemperature() - 273.15:.1f} °C"
                    )
                except:
                    pass
                try:
                    print(f"   Pressure: {out_stream.getPressure():.1f} bara")
                except:
                    pass
                try:
                    print(f"   Flow rate: {out_stream.getFlowRate('kg/hr'):.0f} kg/hr")
                except:
                    pass

            if hasattr(eq, "getPower"):
                try:
                    print(f"   Power: {eq.getPower()/1e3:.2f} kW")
                except:
                    pass
            if hasattr(eq, "getDuty"):
                try:
                    print(f"   Duty: {eq.getDuty()/1e3:.2f} kW")
                except:
                    pass
            print()

        return self

    # =========================================================================
    # GUI HELPER METHODS
    # =========================================================================

    @classmethod
    def get_equipment_types(cls) -> List[str]:
        """
        Get a list of all available equipment types.

        This is useful for GUI development to populate dropdown menus
        or equipment palettes.

        Returns:
            List of equipment type strings that can be used with add().

        Example:
            >>> types = ProcessBuilder.get_equipment_types()
            >>> print(types)
            ['stream', 'compressor', 'separator', 'valve', ...]
        """
        # This mirrors the method_map keys
        return [
            # Core equipment
            "stream",
            "separator",
            "three_phase_separator",
            "compressor",
            "pump",
            "valve",
            "heater",
            "cooler",
            "mixer",
            "splitter",
            "heat_exchanger",
            "pipe",
            "gas_scrubber",
            "recycle",
            "virtual_stream",
            # Extended equipment
            "distillation_column",
            "teg_absorber",
            "water_stripper",
            "component_splitter",
            "saturator",
            "filter",
            "calculator",
            "setpoint",
            "adjuster",
            "ejector",
            "flare",
            "tank",
            # Pipeline
            "beggs_brill_pipe",
            "two_phase_pipe",
            # Measurement
            "pressure_transmitter",
            "level_transmitter",
            "flow_transmitter",
            "temperature_transmitter",
            # Control
            "pid_controller",
            # Flow utilities
            "flow_setter",
            "flow_rate_adjuster",
            # Streams
            "neq_stream",
            "energy_stream",
            "water_stream",
            "well_stream",
            # Enhanced
            "separator_with_dimensions",
            "polytopic_compressor",
            "compressor_with_chart",
            # Mixers
            "static_mixer",
            "static_phase_mixer",
            # Reactor
            "reactor",
            "simple_absorber",
        ]

    @classmethod
    def get_equipment_parameters(cls, equipment_type: str) -> Dict[str, Any]:
        """
        Get parameter schema for an equipment type.

        Returns a dictionary describing the parameters for the specified
        equipment type, useful for generating dynamic forms in a GUI.

        Args:
            equipment_type: Type of equipment (e.g., 'compressor', 'separator')

        Returns:
            Dictionary with parameter names, types, defaults, and descriptions.

        Example:
            >>> schema = ProcessBuilder.get_equipment_parameters('compressor')
            >>> print(schema)
            {
                'inlet': {'type': 'str', 'required': True, 'description': 'Inlet equipment name'},
                'outlet_pressure': {'type': 'float', 'required': False, 'unit': 'bara'},
                ...
            }
        """
        # Parameter schemas for common equipment types
        schemas = {
            "stream": {
                "fluid": {
                    "type": "fluid",
                    "required": True,
                    "description": "Thermodynamic system",
                },
                "temperature": {
                    "type": "float",
                    "required": False,
                    "unit": "K",
                    "description": "Temperature",
                },
                "pressure": {
                    "type": "float",
                    "required": False,
                    "unit": "bara",
                    "description": "Pressure",
                },
                "flow_rate": {
                    "type": "float",
                    "required": False,
                    "description": "Flow rate",
                },
                "flow_unit": {
                    "type": "str",
                    "required": False,
                    "default": "kg/sec",
                    "options": ["kg/sec", "kg/hr", "MSm3/day", "Sm3/day", "mole/sec"],
                },
            },
            "separator": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
            },
            "three_phase_separator": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
            },
            "compressor": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "outlet_pressure": {
                    "type": "float",
                    "required": False,
                    "unit": "bara",
                    "description": "Outlet pressure",
                },
                "isentropic_efficiency": {
                    "type": "float",
                    "required": False,
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "description": "Isentropic efficiency",
                },
                "use_polytropic": {
                    "type": "bool",
                    "required": False,
                    "default": False,
                    "description": "Use polytropic calculation",
                },
            },
            "pump": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "outlet_pressure": {
                    "type": "float",
                    "required": False,
                    "unit": "bara",
                    "description": "Outlet pressure",
                },
                "efficiency": {
                    "type": "float",
                    "required": False,
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "description": "Pump efficiency",
                },
            },
            "valve": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "outlet_pressure": {
                    "type": "float",
                    "required": False,
                    "unit": "bara",
                    "description": "Outlet pressure",
                },
            },
            "heater": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "outlet_temperature": {
                    "type": "float",
                    "required": False,
                    "unit": "C",
                    "description": "Outlet temperature",
                },
            },
            "cooler": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "outlet_temperature": {
                    "type": "float",
                    "required": False,
                    "unit": "C",
                    "description": "Outlet temperature",
                },
            },
            "mixer": {
                "inlets": {
                    "type": "list[str]",
                    "required": False,
                    "description": "List of inlet equipment/stream names",
                },
            },
            "splitter": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "split_fractions": {
                    "type": "list[float]",
                    "required": False,
                    "description": "Split fractions for each outlet",
                },
            },
            "pipe": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
                "length": {
                    "type": "float",
                    "required": False,
                    "unit": "m",
                    "description": "Pipe length",
                },
                "diameter": {
                    "type": "float",
                    "required": False,
                    "unit": "m",
                    "description": "Pipe inner diameter",
                },
            },
            "gas_scrubber": {
                "inlet": {
                    "type": "str",
                    "required": True,
                    "description": "Inlet equipment/stream name",
                },
            },
            "virtual_stream": {
                "source": {
                    "type": "str",
                    "required": False,
                    "description": "Source stream to copy from",
                },
                "flow_rate": {
                    "type": "float",
                    "required": False,
                    "description": "Initial flow rate guess",
                },
                "flow_unit": {
                    "type": "str",
                    "required": False,
                    "default": "kg/hr",
                    "options": ["kg/hr", "kg/sec", "MSm3/day"],
                },
            },
            "recycle": {
                "inlet": {
                    "type": "str",
                    "required": False,
                    "description": "Actual stream to recycle",
                },
                "outlet": {
                    "type": "str",
                    "required": False,
                    "description": "Virtual stream to connect to",
                },
                "tolerance": {
                    "type": "float",
                    "required": False,
                    "default": 1e-4,
                    "description": "Convergence tolerance",
                },
                "priority": {
                    "type": "int",
                    "required": False,
                    "description": "Solve priority (higher = later)",
                },
            },
        }

        return schemas.get(equipment_type.lower(), {})

    def get_outlets(self, equipment_name: str) -> List[str]:
        """
        Get available outlet types for an equipment.

        Returns the outlet connection points available for the specified
        equipment, useful for drawing connections in a visual editor.

        Args:
            equipment_name: Name of equipment in the process.

        Returns:
            List of outlet names (e.g., ['gas', 'liquid', 'oil'] for 3-phase sep)

        Example:
            >>> builder.add_three_phase_separator('sep', 'feed')
            >>> outlets = builder.get_outlets('sep')
            >>> print(outlets)  # ['gas', 'liquid', 'oil', 'water']
        """
        equip = self.equipment.get(equipment_name)
        if equip is None:
            return []

        outlets = []

        # Check for various outlet methods
        if hasattr(equip, "getGasOutStream"):
            outlets.append("gas")
        if hasattr(equip, "getLiquidOutStream"):
            outlets.append("liquid")
        if hasattr(equip, "getOilOutStream"):
            outlets.append("oil")
        if hasattr(equip, "getWaterOutStream"):
            outlets.append("water")
        if hasattr(equip, "getOutletStream"):
            if not outlets:  # Only add 'out' if no specific outlets
                outlets.append("out")
        if hasattr(equip, "getOutStream"):
            if not outlets:
                outlets.append("out")

        # For manifolds, add mixed stream outlet
        if hasattr(equip, "getMixedStream"):
            outlets.append("mixed")

        # For splitters and manifolds, check for multiple split outlets
        if hasattr(equip, "getSplitStream"):
            # Splitters/Manifolds have numbered outlets
            try:
                for i in range(10):  # Check up to 10 outlets
                    if equip.getSplitStream(i) is not None:
                        outlets.append(f"split_{i}")
            except:
                pass

        return outlets if outlets else ["out"]

    def get_inlets(self, equipment_name: str) -> List[str]:
        """
        Get inlet connection points for an equipment.

        Args:
            equipment_name: Name of equipment in the process.

        Returns:
            List of inlet names (usually ['inlet'] or ['hot_inlet', 'cold_inlet'])
        """
        equip = self.equipment.get(equipment_name)
        if equip is None:
            return []

        inlets = []

        # Check for various inlet patterns
        if hasattr(equip, "addStream"):
            inlets.append("inlet")  # Mixers accept multiple
        if hasattr(equip, "setInletStream"):
            inlets.append("inlet")
        if hasattr(equip, "setFeedStream"):
            inlets.append("feed")

        # Heat exchangers have two inlets
        equip_class = type(equip).__name__
        if "HeatExchanger" in equip_class:
            inlets = ["hot_inlet", "cold_inlet"]

        return inlets if inlets else ["inlet"]

    def validate_connection(self, source: str, target_equipment: str) -> Dict[str, Any]:
        """
        Validate if a connection between equipment is valid.

        Checks if the source outlet exists and if the target can accept
        the connection. Useful for GUI validation before allowing connections.

        Args:
            source: Source in format 'equipment.outlet' or just 'equipment'
            target_equipment: Target equipment name

        Returns:
            Dictionary with 'valid' (bool), 'message' (str), and 'warnings' (list)

        Example:
            >>> result = builder.validate_connection('separator.gas', 'compressor')
            >>> if result['valid']:
            ...     builder.add_compressor('comp', 'separator.gas', ...)
        """
        result = {"valid": True, "message": "Connection is valid", "warnings": []}

        # Parse source
        if "." in source:
            equip_name, outlet_type = source.split(".", 1)
        else:
            equip_name = source
            outlet_type = None

        # Check source equipment exists
        source_equip = self.equipment.get(equip_name)
        if source_equip is None:
            result["valid"] = False
            result["message"] = f"Source equipment '{equip_name}' not found"
            return result

        # Check outlet type exists
        if outlet_type:
            available_outlets = self.get_outlets(equip_name)
            if outlet_type.lower() not in [o.lower() for o in available_outlets]:
                result["valid"] = False
                result["message"] = (
                    f"Outlet '{outlet_type}' not available on '{equip_name}'. "
                    f"Available: {available_outlets}"
                )
                return result

        # Check target equipment exists (if already added)
        if target_equipment in self.equipment:
            result["warnings"].append(
                f"Target '{target_equipment}' already exists - will reconnect"
            )

        # Try to get the actual stream to validate it works
        try:
            stream = self._get_outlet(source)
            if stream is None:
                result["valid"] = False
                result["message"] = f"Could not get stream from '{source}'"
                return result
        except Exception as e:
            result["valid"] = False
            result["message"] = f"Error accessing '{source}': {str(e)}"
            return result

        return result

    def to_dict(self) -> Dict[str, Any]:
        """
        Export current process configuration as a dictionary.

        This can be used to save process designs, or to recreate
        the process later using from_dict().

        Returns:
            Dictionary representation of the process.

        Example:
            >>> config = builder.to_dict()
            >>> # Save to file
            >>> import json
            >>> with open('process.json', 'w') as f:
            ...     json.dump(config, f, indent=2)
        """
        config = {
            "process": {"name": self._name},
            "equipment": [],
            "connections": [],
        }

        # Note: This captures equipment names but not full reconstruction info
        # For full reconstruction, use YAML config from the start
        for name, equip in self.equipment.items():
            equip_info = {
                "name": name,
                "type": type(equip).__name__,
            }

            # Try to get outlet info
            outlets = self.get_outlets(name)
            if outlets:
                equip_info["outlets"] = outlets

            # Try to get some properties
            try:
                if hasattr(equip, "getOutletStream"):
                    stream = equip.getOutletStream()
                    if stream:
                        equip_info["outlet_temperature_C"] = round(
                            stream.getTemperature("C"), 2
                        )
                        equip_info["outlet_pressure_bara"] = round(
                            stream.getPressure("bara"), 2
                        )
            except:
                pass

            config["equipment"].append(equip_info)

        return config

    def to_yaml(self) -> str:
        """
        Export current process configuration as a YAML string.

        Returns:
            YAML string representation of the process.

        Example:
            >>> yaml_str = builder.to_yaml()
            >>> print(yaml_str)
            >>> # Or save to file
            >>> with open('process.yaml', 'w') as f:
            ...     f.write(yaml_str)
        """
        import yaml

        config = self.to_dict()
        return yaml.dump(config, default_flow_style=False, sort_keys=False)

    def get_equipment_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of all equipment with their properties.

        Useful for populating equipment lists in GUI.

        Returns:
            List of dictionaries with equipment info.

        Example:
            >>> equipment = builder.get_equipment_list()
            >>> for eq in equipment:
            ...     print(f"{eq['name']}: {eq['type']}")
        """
        equipment_list = []
        for name, equip in self.equipment.items():
            info = {
                "name": name,
                "type": type(equip).__name__,
                "outlets": self.get_outlets(name),
                "inlets": self.get_inlets(name),
            }
            equipment_list.append(info)
        return equipment_list

    def get_connection_graph(self) -> Dict[str, List[str]]:
        """
        Get the connection graph of the process.

        Returns a dictionary where keys are equipment names and values
        are lists of downstream equipment names. Useful for drawing
        process flow diagrams.

        Returns:
            Dictionary mapping equipment to their downstream connections.

        Example:
            >>> graph = builder.get_connection_graph()
            >>> print(graph)
            {'feed': ['separator'], 'separator': ['compressor', 'pump'], ...}
        """
        # This is a simplified version - full implementation would track
        # actual connections made during build
        graph = {name: [] for name in self.equipment}

        # For now, return empty graph - connections aren't tracked
        # A full implementation would require tracking during add_* calls
        return graph

    def save_results(self, filename: str, format: str = "json") -> "ProcessBuilder":
        """
        Save simulation results to a file.

        Args:
            filename: Output file path.
            format: Output format - 'json', 'csv', or 'excel'.

        Returns:
            Self for method chaining.

        Example:
            >>> process.run().save_results('results.json')
            >>> process.save_results('results.csv', format='csv')
            >>> process.save_results('results.xlsx', format='excel')
        """
        if format == "json":
            out_file = _resolve_path_in_cwd(filename, allowed_suffixes={".json"})
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(self.results_json(), f, indent=2)
        elif format == "csv":
            out_file = _resolve_path_in_cwd(filename, allowed_suffixes={".csv"})
            out_file.parent.mkdir(parents=True, exist_ok=True)
            self.results_dataframe().to_csv(str(out_file), index=False)
        elif format == "excel":
            out_file = _resolve_path_in_cwd(
                filename, allowed_suffixes={".xlsx", ".xls"}
            )
            out_file.parent.mkdir(parents=True, exist_ok=True)
            self.results_dataframe().to_excel(str(out_file), index=False)
        else:
            raise ValueError(
                f"Unknown format: {format}. Use 'json', 'csv', or 'excel'."
            )

        print(f"Results saved to {out_file}")
        return self


def _add_to_process(equipment: Any, process: Any = None) -> None:
    """
    Helper to add equipment to a process.

    If process is provided, adds to that process.
    Otherwise, adds to global processoperations if not in loop mode.
    """
    if process is not None:
        if isinstance(process, ProcessContext):
            process.add(equipment)
        elif isinstance(process, ProcessBuilder):
            process.equipment[equipment.getName()] = equipment
            process.process.add(equipment)
        else:
            process.add(equipment)
    elif not _loop_mode:
        processoperations.add(equipment)


def newProcess(name: str = "") -> Any:
    """
    Create a new process simulation object.

    Args:
        name: The name of the process. Defaults to empty string.

    Returns:
        ProcessSystem: A new process system object.

    Example:
        >>> process = newProcess("MyProcess")
    """
    global processoperations
    processoperations = jneqsim.process.processmodel.ProcessSystem(name)
    return processoperations


def set_loop_mode(loop_mode: bool) -> None:
    """
    Set the loop mode for process operations.

    When loop mode is enabled, unit operations are not automatically added
    to the global process. This is useful for creating reusable process
    components or running optimization loops.

    Args:
        loop_mode: If True, enables loop mode.

    Example:
        >>> set_loop_mode(True)
        >>> # Create units without adding to global process
        >>> set_loop_mode(False)
    """
    global _loop_mode
    _loop_mode = loop_mode


def stream(
    name: str, thermoSystem: Any, t: float = 0, p: float = 0, process: Any = None
) -> Any:
    """
    Create a stream with the given name and thermodynamic system.

    A stream represents a material flow in the process simulation.
    Optionally set temperature and pressure.

    Args:
        name: The name of the stream.
        thermoSystem: The thermodynamic system (fluid) for the stream.
        t: Temperature to set (optional). If 0, uses system default.
        p: Pressure to set (optional). If 0, uses system default.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Stream: The created stream object.

    Example:
        >>> from neqsim.thermo import fluid
        >>> my_fluid = fluid('srk')
        >>> my_fluid.addComponent('methane', 1.0)
        >>> inlet_stream = stream('inlet', my_fluid, t=25.0, p=10.0)

        # With explicit process:
        >>> my_process = newProcess('MyProcess')
        >>> inlet = stream('inlet', my_fluid, process=my_process)
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    s = jneqsim.process.equipment.stream.Stream(name, thermoSystem)
    _add_to_process(s, process)
    return s


def virtualstream(name, streamIn):
    """
    Create a virtual stream in the process simulation.

    Parameters:
    name (str): The name of the virtual stream.
    streamIn (Stream): The input stream to be virtualized.

    Returns:
    VirtualStream: The created virtual stream object.
    """
    stream = jneqsim.process.equipment.stream.VirtualStream(name, streamIn)
    if not _loop_mode:
        processoperations.add(stream)
    return stream


def neqstream(name, thermoSystem, t=0, p=0):
    """
    Create a NeqStream with the specified name and thermodynamic system, optionally setting temperature and pressure.

    Parameters:
    name (str): The name of the stream.
    thermoSystem (ThermodynamicSystem): The thermodynamic system to be used in the stream.
    t (float, optional): The temperature to set for the thermodynamic system. Defaults to 0.
    p (float, optional): The pressure to set for the thermodynamic system. Defaults to 0.

    Returns:
    NeqStream: The created NeqStream object.
    """
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
    stream = jneqsim.process.equipment.stream.NeqStream(name, thermoSystem)
    stream.setName(name)
    if not _loop_mode:
        processoperations.add(stream)
    return stream


def recycle(name, stream=None):
    """
    Create a recycle process unit and optionally add a stream to it.

    Parameters:
    name (str): The name of the recycle unit.
    stream (optional): The stream to be added to the recycle unit. Default is None.

    Returns:
    Recycle: The created recycle process unit.
    """
    recycle1 = jneqsim.process.equipment.util.Recycle(name)
    if not stream is None:
        recycle1.addStream(stream)
    if not _loop_mode:
        processoperations.add(recycle1)
    return recycle1


def saturator(name, teststream):
    """
    Create a StreamSaturatorUtil object and add it to the process operations.

    Parameters:
    name (str): The name of the saturator.
    teststream (Stream): The stream to be saturated.

    Returns:
    StreamSaturatorUtil: The created StreamSaturatorUtil object.
    """
    streamsaturator = jneqsim.process.equipment.util.StreamSaturatorUtil(
        name, teststream
    )
    if not _loop_mode:
        processoperations.add(streamsaturator)
    return streamsaturator


def glycoldehydrationlmodule(name, teststream):
    dehydrationlmodule = (
        jneqsim.process.processmodel.processModules.GlycolDehydrationlModule(name)
    )
    dehydrationlmodule.addInputStream("gasStreamToAbsorber", teststream)
    if not _loop_mode:
        processoperations.add(dehydrationlmodule)
    return dehydrationlmodule


def openprocess(filename):
    file_path = _resolve_path_in_cwd(filename, must_exist=True)
    processoperations = jneqsim.process.processmodel.ProcessSystem.open(str(file_path))
    return processoperations


def separator(name: str, teststream: Any, process: Any = None) -> Any:
    """
    Create a two phase separator process equipment.

    Args:
        name: The name of the separator.
        teststream: The inlet stream to be separated.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Separator: The created separator object.

    Example:
        >>> sep = separator('HP separator', inlet_stream)
        >>> gas = sep.getGasOutStream()
        >>> liquid = sep.getLiquidOutStream()
    """
    sep = jneqsim.process.equipment.separator.Separator(name, teststream)
    sep.setName(name)
    _add_to_process(sep, process)
    return sep


def GORfitter(name, teststream):
    """
    Create and configure a GORfitter process equipment.

    Parameters:
    name (str): The name of the GORfitter.
    teststream (Stream): The test stream to be used by the GORfitter.

    Returns:
    GORfitter: The configured GORfitter object.
    """
    GORfitter1 = jneqsim.process.equipment.util.GORfitter(name, teststream)
    GORfitter1.setName(name)
    if not _loop_mode:
        processoperations.add(GORfitter1)
    return GORfitter1


def simpleTEGAbsorber(name):
    absorber = jneqsim.process.equipment.absorber.SimpleTEGAbsorber(name)
    absorber.setName(name)
    if not _loop_mode:
        processoperations.add(absorber)
    return absorber


def waterStripperColumn(name):
    stripper = jneqsim.process.equipment.absorber.WaterStripperColumn(name)
    stripper.setName(name)
    if not _loop_mode:
        processoperations.add(stripper)
    return stripper


def gasscrubber(name, teststream):
    separator = jneqsim.process.equipment.separator.GasScrubber(name, teststream)
    separator.setName(name)
    if not _loop_mode:
        processoperations.add(separator)
    return separator


def separator3phase(name: str, teststream: Any, process: Any = None) -> Any:
    """
    Create a three-phase separator.

    Args:
        name: The name of the separator.
        teststream: The inlet stream to be separated.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        ThreePhaseSeparator: The created three-phase separator object.

    Example:
        >>> sep3 = separator3phase('3-phase sep', inlet_stream)
        >>> gas = sep3.getGasOutStream()
        >>> oil = sep3.getOilOutStream()
        >>> water = sep3.getWaterOutStream()
    """
    sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(name, teststream)
    sep.setName(name)
    _add_to_process(sep, process)
    return sep


def valve(name: str, teststream: Any, p: float = 1.0, process: Any = None) -> Any:
    """
    Create a throttling valve in the process simulation.

    Args:
        name: The name of the valve.
        teststream: The inlet stream.
        p: The outlet pressure in bara. Default is 1.0.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        ThrottlingValve: The created throttling valve object.

    Example:
        >>> v = valve('letdown valve', inlet_stream, p=10.0)
        >>> runProcess()
        >>> print(f"dT = {v.getOutletStream().getTemperature() - v.getInletStream().getTemperature():.1f} K")
    """
    v = jneqsim.process.equipment.valve.ThrottlingValve(name, teststream)
    v.setOutletPressure(p)
    v.setName(name)
    _add_to_process(v, process)
    return v


def calculator(name):
    calc2 = jneqsim.process.equipment.util.Calculator(name)
    if not _loop_mode:
        processoperations.add(calc2)
    return calc2


def setpoint(name1, unit1, name2, unit2):
    setp = jneqsim.process.equipment.util.SetPoint(name1, unit1, name2, unit2)
    if not _loop_mode:
        processoperations.add(setp)
    return setp


def filters(name, teststream):
    filter2 = jneqsim.process.equipment.filter.Filter(name, teststream)
    if not _loop_mode:
        processoperations.add(filter2)
    return filter2


def compressor(
    name: str, teststream: Any, pres: float = 10.0, process: Any = None
) -> Any:
    """
    Create and configure a compressor for a given stream.

    Args:
        name: The name of the compressor.
        teststream: The inlet stream to be compressed.
        pres: The outlet pressure in bara. Defaults to 10.0.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Compressor: The configured compressor object.

    Example:
        >>> comp = compressor('comp1', inlet_stream, pres=50.0)
        >>> runProcess()
        >>> print(f"Power: {comp.getPower()/1e6:.2f} MW")
        >>> print(f"Polytropic efficiency: {comp.getPolytropicEfficiency():.2%}")

        # With explicit process:
        >>> my_process = newProcess('Compression')
        >>> comp = compressor('comp1', inlet, pres=50.0, process=my_process)
    """
    comp = jneqsim.process.equipment.compressor.Compressor(name, teststream)
    comp.setOutletPressure(pres)
    _add_to_process(comp, process)
    return comp


def compressorChart(compressor, curveConditions, speed, flow, head, polyEff):
    compressor.getCompressorChart().setCurves(
        _as_float_list(curveConditions),
        _as_float_list(speed),
        _as_float_matrix(flow),
        _as_float_matrix(head),
        _as_float_matrix(polyEff),
    )


def pumpChart(pump, curveConditions, speed, flow, head, polyEff):
    pump.getPumpChart().setCurves(
        _as_float_list(curveConditions),
        _as_float_list(speed),
        _as_float_matrix(flow),
        _as_float_matrix(head),
        _as_float_matrix(polyEff),
    )


def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    compressor.getCompressorChart().getSurgeCurve().setCurve(
        _as_float_list(curveConditions),
        _as_float_list(surgeflow),
        _as_float_list(surgehead),
    )


def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    compressor.getCompressorChart().getStoneWallCurve().setCurve(
        _as_float_list(curveConditions),
        _as_float_list(stoneWallflow),
        _as_float_list(stoneWallHead),
    )


def pump(name: str, teststream: Any, p: float = 1.0, process: Any = None) -> Any:
    """
    Create a pump process equipment.

    Args:
        name: The name of the pump.
        teststream: The inlet stream to be pumped.
        p: The outlet pressure in bara. Default is 1.0.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Pump: The created pump object.

    Example:
        >>> p = pump('feed pump', liquid_stream, p=50.0)
        >>> runProcess()
        >>> print(f"Power: {p.getPower()/1e3:.1f} kW")
    """
    pmp = jneqsim.process.equipment.pump.Pump(name, teststream)
    pmp.setOutletPressure(p)
    _add_to_process(pmp, process)
    return pmp


def expander(name: str, teststream: Any, p: float, process: Any = None) -> Any:
    """
    Create and configure an expander for the process simulation.

    Args:
        name: The name of the expander.
        teststream: The inlet stream to be expanded.
        p: The outlet pressure in bara.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Expander: The configured expander object.

    Example:
        >>> exp = expander('turbo expander', gas_stream, p=20.0)
        >>> runProcess()
        >>> print(f"Power generated: {-exp.getPower()/1e6:.2f} MW")
    """
    exp = jneqsim.process.equipment.expander.Expander(name, teststream)
    exp.setOutletPressure(p)
    exp.setName(name)
    _add_to_process(exp, process)
    return exp


def mixer(name: str = "", process: Any = None) -> Any:
    """
    Create and add a mixer to the process.

    Args:
        name: The name of the mixer. Default is empty string.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Mixer: An instance of the Mixer class.

    Example:
        >>> m = mixer('gas mixer')
        >>> m.addStream(stream1)
        >>> m.addStream(stream2)
        >>> runProcess()
        >>> mixed = m.getOutletStream()
    """
    m = jneqsim.process.equipment.mixer.Mixer(name)
    _add_to_process(m, process)
    return m


def phasemixer(name):
    mixer = jneqsim.process.equipment.mixer.StaticPhaseMixer(name)
    if not _loop_mode:
        processoperations.add(mixer)
    return mixer


def nequnit(
    teststream, equipment="pipeline", flowpattern="stratified", numberOfNodes=100
):
    neqUn = jneqsim.process.equipment.util.NeqSimUnit(
        teststream, equipment, flowpattern
    )
    neqUn.setNumberOfNodes(numberOfNodes)
    if not _loop_mode:
        processoperations.add(neqUn)
    return neqUn


def compsplitter(name, teststream, splitfactors):
    compSplitter = jneqsim.process.equipment.splitter.ComponentSplitter(
        name, teststream
    )
    compSplitter.setSplitFactors(splitfactors)
    if not _loop_mode:
        processoperations.add(compSplitter)
    return compSplitter


def splitter(
    name: str, teststream: Any, splitfactors: List[float] = None, process: Any = None
) -> Any:
    """
    Create a splitter process equipment.

    Args:
        name: The name of the splitter.
        teststream: The inlet stream to be split.
        splitfactors: List of split fractions. Length determines number of outlets.
            Values should sum to 1.0.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Splitter: The created splitter object.

    Example:
        >>> sp = splitter('flow split', inlet, splitfactors=[0.3, 0.7])
        >>> runProcess()
        >>> stream1 = sp.getSplitStream(0)
        >>> stream2 = sp.getSplitStream(1)
    """
    spl = jneqsim.process.equipment.splitter.Splitter(name, teststream)
    if splitfactors is not None and len(splitfactors) > 0:
        spl.setSplitNumber(len(splitfactors))
        spl.setSplitFactors(_as_float_list(splitfactors))
    _add_to_process(spl, process)
    return spl


def heater(name: str, teststream: Any, process: Any = None) -> Any:
    """
    Create a heater process equipment.

    Args:
        name: The name of the heater.
        teststream: The inlet stream to be heated.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Heater: The created heater object.

    Example:
        >>> h = heater('feed heater', cold_stream)
        >>> h.setOutTemperature(350.0)  # Kelvin
        >>> runProcess()
        >>> print(f"Duty: {h.getDuty()/1e6:.2f} MW")
    """
    h = jneqsim.process.equipment.heatexchanger.Heater(name, teststream)
    h.setName(name)
    _add_to_process(h, process)
    return h


def simplereservoir(
    name,
    fluid,
    gasvolume=10.0 * 1e7,
    oilvolume=120.0 * 1e6,
    watervolume=10.0e6,
):
    reserv = jneqsim.process.equipment.reservoir.SimpleReservoir(name)
    reserv.setReservoirFluid(fluid, gasvolume, oilvolume, watervolume)
    if not _loop_mode:
        processoperations.add(reserv)
    return reserv


def cooler(name: str, teststream: Any, process: Any = None) -> Any:
    """
    Create and configure a cooler process equipment.

    Args:
        name: The name of the cooler.
        teststream: The inlet stream to be cooled.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        Cooler: The configured cooler object.

    Example:
        >>> c = cooler('discharge cooler', hot_stream)
        >>> c.setOutTemperature(303.15)  # 30°C in Kelvin
        >>> runProcess()
        >>> print(f"Duty: {c.getDuty()/1e6:.2f} MW")
    """
    c = jneqsim.process.equipment.heatexchanger.Cooler(name, teststream)
    c.setName(name)
    _add_to_process(c, process)
    return c


def heatExchanger(
    name: str, stream1: Any, stream2: Any = None, process: Any = None
) -> Any:
    """
    Create a heat exchanger process unit.

    Args:
        name: The name of the heat exchanger.
        stream1: The first (hot) input stream.
        stream2: The second (cold) input stream. If not provided,
            creates a single-stream heat exchanger.
        process: Optional ProcessSystem, ProcessContext, or ProcessBuilder
            to add this equipment to. If None, uses global process.

    Returns:
        HeatExchanger: The created heat exchanger object.

    Example:
        >>> hx = heatExchanger('economizer', hot_gas, cold_feed)
        >>> hx.setApproachTemperature(10.0)  # 10 K approach
        >>> runProcess()
    """
    if stream2 is None:
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(name, stream1)
    else:
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(
            name, stream1, stream2
        )
    hx.setName(name)
    _add_to_process(hx, process)
    return hx


def distillationColumn(name, trays=5, reboil=True, condenser=True):
    distillationColumn = jneqsim.process.equipment.distillation.DistillationColumn(
        name, trays, reboil, condenser
    )
    if not _loop_mode:
        processoperations.add(distillationColumn)
    return distillationColumn


def neqheater(name, teststream):
    neqheater = jneqsim.process.equipment.heatexchanger.NeqHeater(name, teststream)
    if not _loop_mode:
        processoperations.add(neqheater)
    return neqheater


def twophasepipe(name, teststream, position, diameter, height, outTemp, rough):
    pipe = jneqsim.process.equipment.pipeline.TwoPhasePipeLine(name, teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    pipe.setInitialFlowPattern("annular")
    numberOfLegs = len(position) - 1
    numberOfNodesInLeg = 60
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(position)
    pipe.setHeightProfile(height)
    pipe.setPipeDiameters(diameter)
    pipe.setPipeWallRoughness(rough)
    pipe.setOuterTemperatures(outTemp)
    pipe.setEquilibriumMassTransfer(0)
    pipe.setEquilibriumHeatTransfer(1)
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def pipe(name, teststream, length, deltaElevation, diameter, rough):
    pipe = jneqsim.process.equipment.pipeline.AdiabaticPipe(name, teststream)
    pipe.setDiameter(diameter)
    pipe.setLength(length)
    pipe.setPipeWallRoughness(rough)
    pipe.setInletElevation(0.0)
    pipe.setOutletElevation(deltaElevation)
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def pipeline(
    name,
    teststream,
    position,
    diameter,
    height,
    outTemp,
    rough,
    outerHeatTransferCoefficients,
    pipeWallHeatTransferCoefficients,
    numberOfNodesInLeg=50,
):
    pipe = jneqsim.process.equipment.pipeline.OnePhasePipeLine(name, teststream)
    pipe.setOutputFileName("c:/tempNew20.nc")
    numberOfLegs = len(position) - 1
    pipe.setNumberOfLegs(numberOfLegs)
    pipe.setNumberOfNodesInLeg(numberOfNodesInLeg)
    pipe.setLegPositions(position)
    pipe.setHeightProfile(height)
    pipe.setPipeDiameters(diameter)
    pipe.setPipeWallRoughness(rough)
    pipe.setPipeOuterHeatTransferCoefficients(outerHeatTransferCoefficients)
    pipe.setPipeWallHeatTransferCoefficients(pipeWallHeatTransferCoefficients)
    pipe.setOuterTemperatures(outTemp)
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def clear():
    """
    Clear all process operations.

    This function calls the `clearAll` method from the `processoperations` module
    to remove all existing process operations.
    """
    processoperations.clearAll()


def run():
    """
    Execute the process operations.

    This function calls the `run` method of the `processoperations` module to
    perform the necessary process operations.
    """
    processoperations.run()


def clearProcess():
    """
    Clear all process operations.

    This function clears all the process operations by calling the clearAll method
    from the processoperations module.
    """
    clear()


def runProcess():
    """
    Execute the process operations.

    This function triggers the execution of the process operations by calling
    the `run` method from the `processoperations` module.
    """
    run()


def runProcessAsThread():
    return processoperations.runAsThread()


def getProcess():
    return processoperations


def runtrans():
    processoperations.runTransient()


def view():
    processoperations.displayResult()


def viewProcess():
    processoperations.displayResult()


def waterDewPointAnalyser(name, teststream):
    waterDewPointAnalyser = jneqsim.process.measurementdevice.WaterDewPointAnalyser(
        teststream
    )
    waterDewPointAnalyser.setName(name)
    if not _loop_mode:
        processoperations.add(waterDewPointAnalyser)
    return waterDewPointAnalyser


def hydrateEquilibriumTemperatureAnalyser(name, teststream):
    hydrateEquilibriumTemperatureAnalyser = (
        jneqsim.process.measurementdevice.HydrateEquilibriumTemperatureAnalyser(
            name, teststream
        )
    )
    hydrateEquilibriumTemperatureAnalyser.setName(name)
    if not _loop_mode:
        processoperations.add(hydrateEquilibriumTemperatureAnalyser)
    return hydrateEquilibriumTemperatureAnalyser


def process_report(process: Optional[Any] = None) -> pd.DataFrame:
    """
    Generate a summary DataFrame of all streams and unit operations in the process.

    This is a convenience function that extracts key information from the process
    simulation results into a pandas DataFrame for easy analysis and display.

    Args:
        process: The process object. If None, uses the global processoperations.

    Returns:
        pd.DataFrame: A DataFrame containing unit operation names, types,
                      and key properties like temperature, pressure, and flow rates.

    Example:
        >>> runProcess()
        >>> df = process_report()
        >>> print(df)
        >>> df.to_excel('process_results.xlsx')
    """
    if process is None:
        process = processoperations

    try:
        json_report = str(process.getReport_json())
        results = json.loads(json_report)

        rows = []
        for unit_name, unit_data in results.items():
            if isinstance(unit_data, dict):
                row = {"Unit Name": unit_name}
                # Extract common properties
                if "feed" in unit_data:
                    feed = unit_data["feed"]
                    if "temperature" in feed:
                        row["Feed Temp [C]"] = feed.get("temperature", {}).get("value")
                    if "pressure" in feed:
                        row["Feed Pres [bara]"] = feed.get("pressure", {}).get("value")
                if "product" in unit_data:
                    product = unit_data["product"]
                    if "temperature" in product:
                        row["Product Temp [C]"] = product.get("temperature", {}).get(
                            "value"
                        )
                    if "pressure" in product:
                        row["Product Pres [bara]"] = product.get("pressure", {}).get(
                            "value"
                        )
                if "power" in unit_data:
                    row["Power [kW]"] = unit_data.get("power", {}).get("value")
                rows.append(row)

        if rows:
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame({"Message": ["No unit operations found in process"]})

    except Exception as e:
        return pd.DataFrame({"Error": [f"Failed to generate report: {e}"]})


def results_json(process, filename=None):
    """
    Generate a JSON report from the process and optionally save it to a file.

    Parameters:
    process: The process object to generate the report from.
    filename (str, optional): The file path to save the JSON report. If None, the report is not saved.

    Returns:
    dict: The JSON report as a Python dictionary.
    """
    try:
        # Generate the JSON report
        json_report = str(process.getReport_json())
        results = json.loads(json_report)

        # Save to file if a filename is provided
        if filename:
            out_file = _resolve_path_in_cwd(filename, allowed_suffixes={".json"})
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with out_file.open("w", encoding="utf-8") as json_file:
                json.dump(results, json_file, indent=4)
            print(f"JSON report saved to {out_file}")

        return results
    except Exception as e:
        print(f"Error generating JSON report: {e}")
        return None


def ejector(name: str, motive_stream: Any, suction_stream: Any) -> Any:
    """
    Create an ejector (gas/steam jet) for mixing streams.

    An ejector uses a high-pressure motive stream to entrain and compress
    a low-pressure suction stream. Commonly used in vacuum systems and
    refrigeration cycles.

    Args:
        name: Name of the ejector unit.
        motive_stream: High-pressure driving stream.
        suction_stream: Low-pressure stream to be entrained.

    Returns:
        Ejector: The created ejector object.

    Example:
        >>> ejector1 = ejector('ej1', high_p_stream, low_p_stream)
        >>> runProcess()
        >>> print(ejector1.getOutletStream().getPressure('bara'))
    """
    ejector_unit = jneqsim.process.equipment.ejector.Ejector(
        name, motive_stream, suction_stream
    )
    if not _loop_mode:
        processoperations.add(ejector_unit)
    return ejector_unit


def flare(
    name: str,
    inlet_stream: Any,
    flame_height: float = 30.0,
    radiant_fraction: float = 0.18,
    tip_diameter: float = 0.3,
) -> Any:
    """
    Create a flare unit for combustion of relief gases.

    A flare safely combusts emergency relief gases, typically from PSVs
    or blowdown systems. Calculates heat release, CO2 emissions, and
    thermal radiation.

    Args:
        name: Name of the flare unit.
        inlet_stream: Stream of gas to be flared.
        flame_height: Effective flame height in meters (default 30.0).
        radiant_fraction: Fraction of heat radiated (default 0.18).
        tip_diameter: Flare tip diameter in meters (default 0.3).

    Returns:
        Flare: The created flare object.

    Example:
        >>> flare1 = flare('main_flare', relief_gas, flame_height=50.0)
        >>> runProcess()
        >>> print(f"Heat duty: {flare1.getHeatDuty('MW'):.2f} MW")
        >>> print(f"CO2: {flare1.getCO2Emission('kg/hr'):.0f} kg/hr")
    """
    flare_unit = jneqsim.process.equipment.flare.Flare(name, inlet_stream)
    flare_unit.setFlameHeight(flame_height)
    flare_unit.setRadiantFraction(radiant_fraction)
    flare_unit.setTipDiameter(tip_diameter)
    if not _loop_mode:
        processoperations.add(flare_unit)
    return flare_unit


def safety_valve(
    name: str,
    inlet_stream: Any,
    set_pressure: float,
    full_open_pressure: float = None,
    blowdown: float = 7.0,
) -> Any:
    """
    Create a Pressure Safety Valve (PSV) for overpressure protection.

    A PSV provides mechanical overpressure protection as a final safety
    layer. Opens when pressure exceeds set pressure and reseats after
    pressure drops below the blowdown threshold.

    Args:
        name: Name of the safety valve.
        inlet_stream: Stream connected to the protected equipment.
        set_pressure: Pressure at which PSV starts to open (bara).
        full_open_pressure: Pressure at which PSV is fully open (bara).
                          If None, defaults to set_pressure * 1.1.
        blowdown: Percentage below set pressure at which PSV reseats
                 (default 7.0, meaning reseats at 93% of set pressure).

    Returns:
        SafetyValve: The created safety valve object.

    Example:
        >>> psv = safety_valve('PSV-001', sep_gas_out, set_pressure=55.0)
        >>> runProcess()
        >>> if psv.getPercentValveOpening() > 0:
        ...     print("PSV is relieving!")
    """
    psv = jneqsim.process.equipment.valve.SafetyValve(name, inlet_stream)
    psv.setPressureSpec(set_pressure)
    if full_open_pressure is None:
        full_open_pressure = set_pressure * 1.1
    psv.setFullOpenPressure(full_open_pressure)
    psv.setBlowdown(blowdown)
    if not _loop_mode:
        processoperations.add(psv)
    return psv


def beggs_brill_pipe(
    name: str,
    inlet_stream: Any,
    length: float,
    diameter: float,
    elevation: float = 0.0,
    roughness: float = 50e-6,
) -> Any:
    """
    Create a Beggs and Brill multiphase pipeline.

    Uses the Beggs and Brill correlation for multiphase flow including
    flow pattern prediction, liquid holdup, and pressure drop with
    elevation effects.

    Args:
        name: Name of the pipeline.
        inlet_stream: Inlet stream to the pipeline.
        length: Pipeline length in meters.
        diameter: Internal diameter in meters.
        elevation: Elevation change (outlet - inlet) in meters. Positive
                  for uphill, negative for downhill. Default 0.0.
        roughness: Pipe wall roughness in meters (default 50e-6).

    Returns:
        PipeBeggsAndBrills: The created pipeline object.

    Example:
        >>> pipe = beggs_brill_pipe('export', inlet, length=10000,
        ...                         diameter=0.3, elevation=100)
        >>> runProcess()
        >>> print(f"Outlet P: {pipe.getOutletStream().getPressure('bara'):.1f}")
    """
    pipe = jneqsim.process.equipment.pipeline.PipeBeggsAndBrills(name, inlet_stream)
    pipe.setLength(length)
    pipe.setDiameter(diameter)
    pipe.setElevation(elevation)
    pipe.setPipeWallRoughness(roughness)
    if not _loop_mode:
        processoperations.add(pipe)
    return pipe


def create_equipment(name: str, equipment_type: str) -> Any:
    """
    Create process equipment using the equipment factory.

    Allows dynamic creation of equipment by type name string, useful
    for configuration-driven process design.

    Args:
        name: Name of the equipment.
        equipment_type: Type of equipment. Valid types include:
            'Stream', 'Compressor', 'Pump', 'Separator', 'HeatExchanger',
            'ThrottlingValve', 'Mixer', 'Splitter', 'Cooler', 'Heater',
            'Expander', 'Pipeline', 'WindTurbine', etc.

    Returns:
        ProcessEquipmentInterface: The created equipment object.

    Example:
        >>> valve = create_equipment('v1', 'ThrottlingValve')
        >>> sep = create_equipment('sep1', 'Separator')
    """
    return jneqsim.process.equipment.EquipmentFactory.createEquipment(
        name, equipment_type
    )


def staticmixer(name: str) -> Any:
    """
    Create a static mixer without thermodynamic equilibrium flash.

    A static mixer combines streams without performing a flash calculation,
    preserving the phase distribution from the inlet streams. Useful for
    mixing streams where you want to maintain phase compositions.

    Args:
        name: Name of the static mixer.

    Returns:
        StaticMixer: The created static mixer object.

    Example:
        >>> smixer = staticmixer('makeup_mixer')
        >>> smixer.addStream(lean_stream)
        >>> smixer.addStream(makeup_stream)
        >>> runProcess()
    """
    static_mixer = jneqsim.process.equipment.mixer.StaticMixer(name)
    if not _loop_mode:
        processoperations.add(static_mixer)
    return static_mixer


def tank(name: str, inlet_stream: Any = None) -> Any:
    """
    Create a storage tank with separate gas and liquid outlets.

    A tank provides holdup volume for process fluids and separates
    gas and liquid phases. Can be used for buffer storage or as
    an atmospheric separator.

    Args:
        name: Name of the tank.
        inlet_stream: Optional inlet stream to the tank.

    Returns:
        Tank: The created tank object.

    Example:
        >>> storage = tank('oil_storage', feed_stream)
        >>> storage.setLiquidVolume(1000.0)  # m3
        >>> storage.setGasVolume(500.0)  # m3
        >>> runProcess()
        >>> oil_out = storage.getLiquidOutStream()
        >>> gas_out = storage.getGasOutStream()
    """
    if inlet_stream is not None:
        tank_unit = jneqsim.process.equipment.tank.Tank(name, inlet_stream)
    else:
        tank_unit = jneqsim.process.equipment.tank.Tank(name)
    if not _loop_mode:
        processoperations.add(tank_unit)
    return tank_unit


def adjuster(name: str) -> Any:
    """
    Create an adjuster for process variable control.

    An adjuster modifies an adjusted variable to match a target value.
    Useful for solving process specifications like maintaining a
    certain flow rate, pressure, or temperature.

    Args:
        name: Name of the adjuster.

    Returns:
        Adjuster: The created adjuster object.

    Example:
        >>> adj = adjuster('flow_controller')
        >>> adj.setAdjustedVariable(inlet_stream, 'flow', 'kg/hr')
        >>> adj.setTargetVariable(outlet_stream, 'pressure', 50.0, 'bara')
        >>> runProcess()
    """
    adjuster_unit = jneqsim.process.equipment.util.Adjuster(name)
    if not _loop_mode:
        processoperations.add(adjuster_unit)
    return adjuster_unit


def flowrateadjuster(name: str, inlet_stream: Any = None) -> Any:
    """
    Create a flow rate adjuster for setting gas/oil/water rates.

    Adjusts the outlet stream to match specified gas, oil, and water
    flow rates. Useful for well modeling or flow allocation.

    Args:
        name: Name of the flow rate adjuster.
        inlet_stream: Optional inlet stream.

    Returns:
        FlowRateAdjuster: The created flow rate adjuster object.

    Example:
        >>> fra = flowrateadjuster('well_rates', well_stream)
        >>> fra.setAdjustedFlowRates(100000, 5000, 1000, 'Sm3/day')  # gas, oil, water
        >>> runProcess()
    """
    if inlet_stream is not None:
        fra = jneqsim.process.equipment.util.FlowRateAdjuster(name, inlet_stream)
    else:
        fra = jneqsim.process.equipment.util.FlowRateAdjuster(name)
    if not _loop_mode:
        processoperations.add(fra)
    return fra


def manifold(name: str) -> Any:
    """
    Create a manifold for collecting multiple streams.

    A manifold combines multiple inlet streams into a single outlet,
    similar to a mixer but representing physical piping manifolds.

    Args:
        name: Name of the manifold.

    Returns:
        Manifold: The created manifold object.

    Example:
        >>> prod_manifold = manifold('production_manifold')
        >>> prod_manifold.addStream(well1_stream)
        >>> prod_manifold.addStream(well2_stream)
        >>> runProcess()
    """
    manifold_unit = jneqsim.process.equipment.manifold.Manifold(name)
    if not _loop_mode:
        processoperations.add(manifold_unit)
    return manifold_unit


def flarestack(name: str, inlet_stream: Any = None) -> Any:
    """
    Create a flare stack for emergency gas disposal.

    A flare stack is a vertical structure for safely burning waste
    gases at elevation. Includes flame arrestor and pilot systems.

    Args:
        name: Name of the flare stack.
        inlet_stream: Optional inlet stream of gas to be flared.

    Returns:
        FlareStack: The created flare stack object.

    Example:
        >>> flare = flarestack('emergency_flare', relief_gas)
        >>> flare.setStackHeight(60.0)  # meters
        >>> runProcess()
    """
    if inlet_stream is not None:
        flare = jneqsim.process.equipment.flare.FlareStack(name, inlet_stream)
    else:
        flare = jneqsim.process.equipment.flare.FlareStack(name)
    if not _loop_mode:
        processoperations.add(flare)
    return flare


def windturbine(name: str, power_output: float = 5.0) -> Any:
    """
    Create a wind turbine for power generation.

    Models a wind turbine converting wind energy to electrical power.
    Can be used in hybrid energy system simulations.

    Args:
        name: Name of the wind turbine.
        power_output: Rated power output in MW (default 5.0).

    Returns:
        WindTurbine: The created wind turbine object.

    Example:
        >>> turbine = windturbine('offshore_turbine', power_output=8.0)
        >>> turbine.setWindSpeed(12.0)  # m/s
        >>> runProcess()
        >>> print(f"Power: {turbine.getPower('MW'):.1f} MW")
    """
    wt = jneqsim.process.equipment.powergeneration.WindTurbine(name)
    wt.setPower(power_output * 1e6)  # Convert MW to W
    if not _loop_mode:
        processoperations.add(wt)
    return wt


def solarpanel(name: str, area: float = 100.0) -> Any:
    """
    Create a solar panel array for power generation.

    Models photovoltaic panels converting solar radiation to
    electrical power. Can be used in hybrid energy system simulations.

    Args:
        name: Name of the solar panel array.
        area: Total panel area in m² (default 100.0).

    Returns:
        SolarPanel: The created solar panel object.

    Example:
        >>> solar = solarpanel('roof_panels', area=500.0)
        >>> solar.setSolarIrradiance(800.0)  # W/m²
        >>> runProcess()
        >>> print(f"Power: {solar.getPower('kW'):.1f} kW")
    """
    sp = jneqsim.process.equipment.powergeneration.SolarPanel(name)
    sp.setArea(area)
    if not _loop_mode:
        processoperations.add(sp)
    return sp


def batterystorage(name: str, capacity: float = 100.0) -> Any:
    """
    Create a battery storage system.

    Models battery energy storage for grid stabilization or
    backup power. Can charge from or discharge to the grid.

    Args:
        name: Name of the battery storage.
        capacity: Storage capacity in MWh (default 100.0).

    Returns:
        BatteryStorage: The created battery storage object.

    Example:
        >>> battery = batterystorage('grid_battery', capacity=50.0)
        >>> battery.setChargeRate(10.0)  # MW
        >>> runProcess()
    """
    bs = jneqsim.process.equipment.battery.BatteryStorage(name)
    bs.setCapacity(capacity)
    if not _loop_mode:
        processoperations.add(bs)
    return bs


def fuelcell(name: str, inlet_stream: Any = None) -> Any:
    """
    Create a fuel cell for power generation from hydrogen.

    Models a fuel cell converting hydrogen and oxygen to
    electricity and water. Used in hydrogen economy simulations.

    Args:
        name: Name of the fuel cell.
        inlet_stream: Optional hydrogen feed stream.

    Returns:
        FuelCell: The created fuel cell object.

    Example:
        >>> fc = fuelcell('hydrogen_fc', h2_stream)
        >>> fc.setEfficiency(0.55)
        >>> runProcess()
        >>> print(f"Power: {fc.getPower('MW'):.2f} MW")
    """
    if inlet_stream is not None:
        fc = jneqsim.process.equipment.powergeneration.FuelCell(name, inlet_stream)
    else:
        fc = jneqsim.process.equipment.powergeneration.FuelCell(name)
    if not _loop_mode:
        processoperations.add(fc)
    return fc


def electrolyzer(name: str, inlet_stream: Any = None) -> Any:
    """
    Create an electrolyzer for hydrogen production.

    Models water electrolysis to produce hydrogen and oxygen
    using electrical power. Used in green hydrogen simulations.

    Args:
        name: Name of the electrolyzer.
        inlet_stream: Optional water feed stream.

    Returns:
        Electrolyzer: The created electrolyzer object.

    Example:
        >>> elec = electrolyzer('h2_production', water_stream)
        >>> elec.setPower(10.0, 'MW')
        >>> runProcess()
        >>> h2_stream = elec.getOutletStream()
    """
    if inlet_stream is not None:
        elec = jneqsim.process.equipment.electrolyzer.Electrolyzer(name, inlet_stream)
    else:
        elec = jneqsim.process.equipment.electrolyzer.Electrolyzer(name)
    if not _loop_mode:
        processoperations.add(elec)
    return elec


def co2electrolyzer(name: str, inlet_stream: Any = None) -> Any:
    """
    Create a CO2 electrolyzer for carbon utilization.

    Models electrochemical conversion of CO2 to valuable products
    like syngas, formic acid, or methanol using electrical power.

    Args:
        name: Name of the CO2 electrolyzer.
        inlet_stream: Optional CO2 feed stream.

    Returns:
        CO2Electrolyzer: The created CO2 electrolyzer object.

    Example:
        >>> co2elec = co2electrolyzer('co2_conversion', co2_stream)
        >>> co2elec.setPower(5.0, 'MW')
        >>> runProcess()
    """
    if inlet_stream is not None:
        elec = jneqsim.process.equipment.electrolyzer.CO2Electrolyzer(
            name, inlet_stream
        )
    else:
        elec = jneqsim.process.equipment.electrolyzer.CO2Electrolyzer(name)
    if not _loop_mode:
        processoperations.add(elec)
    return elec


def flowsetter(name: str, inlet_stream: Any) -> Any:
    """
    Create a flow setter for specifying stream flow rates.

    Sets the gas, oil, and water flow rates of a stream based
    on a reference process. Useful for well testing analysis.

    Args:
        name: Name of the flow setter.
        inlet_stream: Input stream to adjust.

    Returns:
        FlowSetter: The created flow setter object.

    Example:
        >>> fs = flowsetter('well_test', well_stream)
        >>> fs.setGasFlowRate(50000, 'Sm3/hr')
        >>> fs.setOilFlowRate(100, 'm3/hr')
        >>> runProcess()
    """
    fs = jneqsim.process.equipment.util.FlowSetter(name, inlet_stream)
    if not _loop_mode:
        processoperations.add(fs)
    return fs


def setter(name: str) -> Any:
    """
    Create a setter for modifying equipment parameters.

    A setter allows programmatic modification of equipment
    parameters during process simulation.

    Args:
        name: Name of the setter.

    Returns:
        Setter: The created setter object.

    Example:
        >>> s = setter('pressure_setter')
        >>> s.setVariable(compressor, 'outletPressure', 50.0)
        >>> runProcess()
    """
    setter_unit = jneqsim.process.equipment.util.Setter(name)
    if not _loop_mode:
        processoperations.add(setter_unit)
    return setter_unit


def wellflow(
    name: str, inlet_stream: Any, well_depth: float = 1000.0, well_diameter: float = 0.1
) -> Any:
    """
    Create a well flow model for production or injection wells.

    Models fluid flow in a wellbore including pressure drop,
    temperature change, and phase behavior.

    Args:
        name: Name of the well.
        inlet_stream: Inlet stream (bottomhole for producer, wellhead for injector).
        well_depth: True vertical depth in meters (default 1000.0).
        well_diameter: Well tubing internal diameter in meters (default 0.1).

    Returns:
        Well flow object.

    Example:
        >>> well = wellflow('prod_well_1', reservoir_stream,
        ...                 well_depth=2500.0, well_diameter=0.1)
        >>> runProcess()
        >>> wellhead = well.getOutletStream()
    """
    well = jneqsim.process.equipment.pipeline.PipeBeggsAndBrills(name, inlet_stream)
    well.setLength(well_depth)
    well.setDiameter(well_diameter)
    well.setElevation(-well_depth)  # Negative for upward flow
    if not _loop_mode:
        processoperations.add(well)
    return well


def energystream(name: str, power: float = 0.0) -> Any:
    """
    Create an energy stream for heat/power transfer.

    An energy stream represents the transfer of thermal or
    electrical energy between equipment units.

    Args:
        name: Name of the energy stream.
        power: Power in Watts (default 0.0).

    Returns:
        EnergyStream: The created energy stream object.

    Example:
        >>> heat = energystream('reboiler_heat', power=5e6)  # 5 MW
        >>> column.setReboilerEnergy(heat)
        >>> runProcess()
    """
    es = jneqsim.process.equipment.stream.EnergyStream(name)
    es.setDuty(power)
    if not _loop_mode:
        processoperations.add(es)
    return es


# =============================================================================
# YAML/Config-Based Process Creation Functions
# =============================================================================


def create_fluid_from_config(config: Dict[str, Any]) -> Any:
    """
    Create a fluid (thermodynamic system) from a configuration dictionary.

    Supports various fluid creation methods:
    - Predefined types: 'dry gas', 'black oil', etc.
    - Custom compositions with equation of state
    - DataFrame-based reservoir fluids

    Args:
        config: Dictionary with fluid configuration. Supported keys:
            - type: 'predefined', 'custom', or 'dataframe' (default 'custom')
            - model: Equation of state ('srk', 'pr', 'cpa', etc.)
            - name: Predefined fluid name (for type='predefined')
            - temperature: Initial temperature in Kelvin (default 298.15)
            - pressure: Initial pressure in bara (default 1.01325)
            - components: List of component definitions for custom fluids
            - dataframe: Dict with 'data' for DataFrame-based fluids

    Returns:
        Fluid object (thermodynamic system).

    Example:
        >>> # Predefined fluid
        >>> config = {'type': 'predefined', 'name': 'dry gas'}
        >>> fluid = create_fluid_from_config(config)

        >>> # Custom fluid with composition
        >>> config = {
        ...     'model': 'srk',
        ...     'temperature': 303.15,
        ...     'pressure': 50.0,
        ...     'components': [
        ...         {'name': 'methane', 'moles': 0.9},
        ...         {'name': 'ethane', 'moles': 0.05},
        ...         {'name': 'propane', 'moles': 0.03},
        ...         {'name': 'n-butane', 'moles': 0.02}
        ...     ]
        ... }
        >>> fluid = create_fluid_from_config(config)

        >>> # Custom with flow rates
        >>> config = {
        ...     'model': 'cpa',
        ...     'temperature': 288.15,
        ...     'pressure': 100.0,
        ...     'components': [
        ...         {'name': 'water', 'rate': 100.0, 'unit': 'kg/hr'},
        ...         {'name': 'MEG', 'rate': 500.0, 'unit': 'kg/hr'}
        ...     ]
        ... }
        >>> fluid = create_fluid_from_config(config)
    """
    from neqsim.thermo import thermoTools

    fluid_type = config.get("type", "custom")

    # Predefined fluid types
    if fluid_type == "predefined":
        name = config.get("name", "dry gas")
        return thermoTools.createfluid(name)

    # Custom fluid with components
    model = config.get("model", "srk")
    temperature = config.get("temperature", 298.15)
    pressure = config.get("pressure", 1.01325)

    # Create base fluid
    thermo_system = thermoTools.fluid(model, temperature, pressure)

    # Add components
    components = config.get("components", [])
    for comp in components:
        comp_name = comp.get("name")
        if comp_name is None:
            continue

        # Support different ways to specify amount
        if "moles" in comp:
            thermoTools.addComponent(thermo_system, comp_name, comp["moles"])
        elif "rate" in comp:
            rate = comp["rate"]
            unit = comp.get("unit", "mol/sec")
            thermoTools.addComponent(thermo_system, comp_name, rate, unit)
        elif "mole_fraction" in comp:
            # Will normalize later
            thermoTools.addComponent(thermo_system, comp_name, comp["mole_fraction"])
        else:
            # Default to 1 mole
            thermoTools.addComponent(thermo_system, comp_name, 1.0)

    # Apply mixing rule if specified
    mixing_rule = config.get("mixing_rule")
    if mixing_rule:
        ge_model = config.get("ge_model", "")
        thermoTools.mixingRule(thermo_system, mixing_rule, ge_model)

    # Enable multiphase if specified
    if config.get("multiphase", False):
        thermoTools.multiphase(thermo_system, 1)

    # Enable solid check if specified
    if config.get("solid_check", False):
        thermoTools.solidcheck(thermo_system, 1)

    return thermo_system


def create_process_from_config(
    config: Union[str, Dict[str, Any]],
    fluids: Dict[str, Any] = None,
    run: bool = True,
) -> "ProcessBuilder":
    """
    Create a complete process from a YAML file or configuration dictionary.

    This is a general-purpose function for building NeqSim processes from
    configuration files. It can automatically create fluids from configuration
    or use pre-created fluid objects.

    Args:
        config: Either a path to a YAML file (relative to the current working
            directory) or a configuration dictionary.
        fluids: Optional dictionary mapping fluid names to fluid objects.
            If the config includes a 'fluids' section, fluids are created
            automatically and merged with this dictionary.
        run: If True (default), run the process after building.

    Returns:
        ProcessBuilder instance with the built process.

    YAML Format:
        The YAML file should have this structure:

        ```yaml
        # Process configuration
        name: "My Process"

        # Optional: Define fluids inline (auto-created)
        fluids:
          feed:
            model: srk
            temperature: 303.15
            pressure: 50.0
            components:
              - name: methane
                moles: 0.85
              - name: ethane
                moles: 0.10
              - name: propane
                moles: 0.05

          glycol:
            model: cpa
            temperature: 298.15
            pressure: 1.0
            components:
              - name: MEG
                rate: 100.0
                unit: kg/hr

        # Equipment list (processed in order)
        equipment:
          - type: stream
            name: inlet
            fluid: feed  # References fluid defined above or in fluids dict
            temperature: 303.15
            pressure: 50.0
            flow_rate: 10.0
            flow_unit: MSm3/day

          - type: heater
            name: heater1
            inlet: inlet
            temperature: 320.0

          - type: separator
            name: sep1
            inlet: heater1

          - type: compressor
            name: comp1
            inlet: sep1.gas
            pressure: 100.0

          - type: cooler
            name: cooler1
            inlet: comp1
            temperature: 303.15

          - type: splitter
            name: split1
            inlet: cooler1
            split_factors: [0.7, 0.3]

          - type: mixer
            name: mixer1
            inlets:
              - split1.split_0
              - some_other_stream
        ```

    Equipment Types:
        The following equipment types are supported (use lowercase):
        - stream: Process stream (requires 'fluid' reference)
        - heater, cooler: Temperature changers
        - separator, three_phase_separator: Phase separators
        - compressor, expander: Pressure changers
        - pump, valve: Liquid/gas handling
        - heat_exchanger: Two-stream heat exchange
        - mixer, splitter: Stream combining/splitting
        - manifold: Multiple inlet/outlet handling
        - recycle, virtual_stream: Recycle loops
        - distillation_column, absorber: Columns
        - And many more...

    Outlet Notation:
        For equipment with multiple outlets, use dot notation:
        - separator: .gas, .liquid
        - three_phase_separator: .gas, .oil, .water
        - splitter: .split_0, .split_1, .split_2, ...
        - manifold: .mixed (combined), .split_0, .split_1, ...
        - virtual_stream: .out

    Example:
        >>> # From YAML file
        >>> process = create_process_from_config('process.yaml')
        >>> print(process.results_dataframe())

        >>> # From dictionary with pre-created fluids
        >>> from neqsim.thermo import fluid, addComponent
        >>> feed = fluid('srk')
        >>> addComponent(feed, 'methane', 0.9)
        >>> addComponent(feed, 'ethane', 0.1)
        >>>
        >>> config = {
        ...     'name': 'Simple Compression',
        ...     'equipment': [
        ...         {'type': 'stream', 'name': 'inlet', 'fluid': 'feed',
        ...          'temperature': 300, 'pressure': 10, 'flow_rate': 5},
        ...         {'type': 'compressor', 'name': 'comp1', 'inlet': 'inlet',
        ...          'pressure': 50}
        ...     ]
        ... }
        >>> process = create_process_from_config(config, fluids={'feed': feed})

        >>> # Don't run immediately
        >>> process = create_process_from_config('process.yaml', run=False)
        >>> # ... modify process ...
        >>> process.run()

    See Also:
        - ProcessBuilder.from_yaml(): Class method for YAML loading
        - ProcessBuilder.from_dict(): Class method for dict loading
        - create_fluid_from_config(): Create fluids from config
    """
    # Load config from file if string path provided
    if isinstance(config, str):
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "PyYAML is required for YAML support. Install with: pip install pyyaml"
            )

        yaml_file = _resolve_path_in_cwd(
            config, allowed_suffixes=_YAML_SUFFIXES, must_exist=True
        )
        with yaml_file.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

    # Initialize fluids dictionary
    all_fluids = fluids.copy() if fluids else {}

    # Create fluids from config if 'fluids' section exists
    if "fluids" in config:
        for fluid_name, fluid_config in config["fluids"].items():
            if fluid_name not in all_fluids:  # Don't override provided fluids
                all_fluids[fluid_name] = create_fluid_from_config(fluid_config)

    # Build process using ProcessBuilder
    builder = ProcessBuilder.from_dict(config, all_fluids)

    # Run if requested
    if run:
        builder.run()

    return builder


def load_process_config(yaml_path: str) -> Dict[str, Any]:
    """
    Load a process configuration from a YAML file without creating the process.

    Useful for inspecting or modifying configurations before building.

    Args:
        yaml_path: Path to YAML configuration file (relative to the current working directory).

    Returns:
        Dictionary with the configuration.

    Example:
        >>> config = load_process_config('process.yaml')
        >>> # Modify configuration
        >>> config['equipment'][0]['pressure'] = 100.0
        >>> # Now create process
        >>> process = create_process_from_config(config)
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "PyYAML is required for YAML support. Install with: pip install pyyaml"
        )

    yaml_file = _resolve_path_in_cwd(
        yaml_path, allowed_suffixes=_YAML_SUFFIXES, must_exist=True
    )
    with yaml_file.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_process_config(config: Dict[str, Any], yaml_path: str) -> None:
    """
    Save a process configuration to a YAML file.

    Args:
        config: Configuration dictionary.
        yaml_path: Path to save the YAML file (relative to the current working directory).

    Example:
        >>> config = {
        ...     'name': 'My Process',
        ...     'equipment': [...]
        ... }
        >>> save_process_config(config, 'process.yaml')
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "PyYAML is required for YAML support. Install with: pip install pyyaml"
        )

    yaml_file = _resolve_path_in_cwd(yaml_path, allowed_suffixes=_YAML_SUFFIXES)
    yaml_file.parent.mkdir(parents=True, exist_ok=True)
    with yaml_file.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
