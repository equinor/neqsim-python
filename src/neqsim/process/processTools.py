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
from typing import Any, Optional, List, Dict, Union

import pandas as pd
from jpype.types import JDouble
from jpype.types import *

from neqsim import jneqsim

processoperations = jneqsim.process.processmodel.ProcessSystem()
_loop_mode: bool = False


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
    
    def __enter__(self) -> 'ProcessContext':
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
        if hasattr(equipment, 'getName'):
            self.equipment[equipment.getName()] = equipment
        return equipment
    
    def run(self) -> 'ProcessContext':
        """
        Run the process simulation.
        
        Returns:
            Self for method chaining.
        """
        self.process.run()
        return self
    
    def run_transient(self, dt: float, time: float) -> 'ProcessContext':
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
        sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(name, inlet_stream)
        return self.add(sep)
    
    def compressor(self, name: str, inlet_stream: Any, pres: float = 0, 
                   efficiency: float = 0.75) -> Any:
        """Create a compressor and add to this process."""
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        if pres > 0:
            comp.setOutletPressure(pres)
        comp.setIsentropicEfficiency(efficiency)
        return self.add(comp)
    
    def pump(self, name: str, inlet_stream: Any, pres: float = 0,
             efficiency: float = 0.75) -> Any:
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
    
    def splitter(self, name: str, inlet_stream: Any, split_factors: List[float] = None) -> Any:
        """Create a splitter and add to this process."""
        s = jneqsim.process.equipment.splitter.Splitter(name, inlet_stream)
        if split_factors:
            s.setSplitFactors(split_factors)
        return self.add(s)
    
    def heat_exchanger(self, name: str, hot_stream: Any, cold_stream: Any,
                       approach_temp: float = 10.0) -> Any:
        """Create a heat exchanger and add to this process."""
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(name, hot_stream, cold_stream)
        hx.setApproachTemperature(approach_temp)
        return self.add(hx)
    
    def pipe(self, name: str, inlet_stream: Any, length: float = 100.0,
             diameter: float = 0.1) -> Any:
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


class ProcessBuilder:
    """
    Fluent builder for constructing process simulations.
    
    ProcessBuilder provides a chainable API for building processes
    step by step. Equipment is referenced by name, making it easy
    to construct processes from configuration data.
    
    Example:
        >>> from neqsim.thermo import fluid
        >>> from neqsim.process import ProcessBuilder
        >>> 
        >>> feed = fluid('srk')
        >>> feed.addComponent('methane', 0.9)
        >>> feed.addComponent('ethane', 0.1)
        >>> feed.setPressure(30.0, 'bara')
        >>> feed.setTemperature(30.0, 'C')
        >>> 
        >>> process = (ProcessBuilder("Compression Train")
        ...     .add_stream('inlet', feed)
        ...     .add_compressor('comp1', 'inlet', pressure=60.0)
        ...     .add_cooler('cooler1', 'comp1', temperature=303.15)
        ...     .add_compressor('comp2', 'cooler1', pressure=120.0)
        ...     .run())
        >>> 
        >>> print(f"Stage 1 power: {process.get('comp1').getPower()/1e6:.2f} MW")
        >>> print(f"Stage 2 power: {process.get('comp2').getPower()/1e6:.2f} MW")
    """
    
    def __init__(self, name: str = ""):
        """Create a new ProcessBuilder."""
        self.process = jneqsim.process.processmodel.ProcessSystem(name)
        self.equipment: Dict[str, Any] = {}
        self._name = name
    
    def _get_outlet(self, ref: Union[str, Any]) -> Any:
        """Get outlet stream from equipment reference (name or object)."""
        if isinstance(ref, str):
            equip = self.equipment.get(ref)
            if equip is None:
                raise ValueError(f"Equipment '{ref}' not found")
            if hasattr(equip, 'getOutletStream'):
                return equip.getOutletStream()
            elif hasattr(equip, 'getOutStream'):
                return equip.getOutStream()
            elif hasattr(equip, 'getGasOutStream'):
                return equip.getGasOutStream()
            return equip
        return ref
    
    def add_stream(self, name: str, thermo_system: Any, 
                   temperature: float = None, pressure: float = None) -> 'ProcessBuilder':
        """
        Add a stream to the process.
        
        Args:
            name: Name of the stream.
            thermo_system: Fluid/thermodynamic system.
            temperature: Optional temperature in Kelvin.
            pressure: Optional pressure in bara.
            
        Returns:
            Self for method chaining.
        """
        if temperature is not None:
            thermo_system.setTemperature(temperature)
        if pressure is not None:
            thermo_system.setPressure(pressure)
        s = jneqsim.process.equipment.stream.Stream(name, thermo_system)
        self.equipment[name] = s
        self.process.add(s)
        return self
    
    def add_separator(self, name: str, inlet: str, three_phase: bool = False) -> 'ProcessBuilder':
        """Add a separator to the process."""
        inlet_stream = self._get_outlet(inlet)
        if three_phase:
            sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(name, inlet_stream)
        else:
            sep = jneqsim.process.equipment.separator.Separator(name, inlet_stream)
        self.equipment[name] = sep
        self.process.add(sep)
        return self
    
    def add_compressor(self, name: str, inlet: str, pressure: float = None,
                       efficiency: float = 0.75) -> 'ProcessBuilder':
        """Add a compressor to the process."""
        inlet_stream = self._get_outlet(inlet)
        comp = jneqsim.process.equipment.compressor.Compressor(name, inlet_stream)
        if pressure is not None:
            comp.setOutletPressure(pressure)
        comp.setIsentropicEfficiency(efficiency)
        self.equipment[name] = comp
        self.process.add(comp)
        return self
    
    def add_pump(self, name: str, inlet: str, pressure: float = None,
                 efficiency: float = 0.75) -> 'ProcessBuilder':
        """Add a pump to the process."""
        inlet_stream = self._get_outlet(inlet)
        p = jneqsim.process.equipment.pump.Pump(name, inlet_stream)
        if pressure is not None:
            p.setOutletPressure(pressure)
        p.setIsentropicEfficiency(efficiency)
        self.equipment[name] = p
        self.process.add(p)
        return self
    
    def add_expander(self, name: str, inlet: str, pressure: float = None) -> 'ProcessBuilder':
        """Add an expander to the process."""
        inlet_stream = self._get_outlet(inlet)
        exp = jneqsim.process.equipment.expander.Expander(name, inlet_stream)
        if pressure is not None:
            exp.setOutletPressure(pressure)
        self.equipment[name] = exp
        self.process.add(exp)
        return self
    
    def add_valve(self, name: str, inlet: str, pressure: float = None) -> 'ProcessBuilder':
        """Add a valve to the process."""
        inlet_stream = self._get_outlet(inlet)
        v = jneqsim.process.equipment.valve.ThrottlingValve(name, inlet_stream)
        if pressure is not None:
            v.setOutletPressure(pressure)
        self.equipment[name] = v
        self.process.add(v)
        return self
    
    def add_heater(self, name: str, inlet: str, temperature: float = None,
                   duty: float = None) -> 'ProcessBuilder':
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
    
    def add_cooler(self, name: str, inlet: str, temperature: float = None,
                   duty: float = None) -> 'ProcessBuilder':
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
    
    def add_mixer(self, name: str, inlets: List[str]) -> 'ProcessBuilder':
        """Add a mixer to the process."""
        m = jneqsim.process.equipment.mixer.Mixer(name)
        for inlet in inlets:
            inlet_stream = self._get_outlet(inlet)
            m.addStream(inlet_stream)
        self.equipment[name] = m
        self.process.add(m)
        return self
    
    def add_splitter(self, name: str, inlet: str, 
                     split_factors: List[float] = None) -> 'ProcessBuilder':
        """Add a splitter to the process."""
        inlet_stream = self._get_outlet(inlet)
        s = jneqsim.process.equipment.splitter.Splitter(name, inlet_stream)
        if split_factors:
            s.setSplitFactors(split_factors)
        self.equipment[name] = s
        self.process.add(s)
        return self
    
    def add_heat_exchanger(self, name: str, hot_inlet: str, cold_inlet: str,
                           approach_temp: float = 10.0) -> 'ProcessBuilder':
        """Add a heat exchanger to the process."""
        hot_stream = self._get_outlet(hot_inlet)
        cold_stream = self._get_outlet(cold_inlet)
        hx = jneqsim.process.equipment.heatexchanger.HeatExchanger(name, hot_stream, cold_stream)
        hx.setApproachTemperature(approach_temp)
        self.equipment[name] = hx
        self.process.add(hx)
        return self
    
    def add_pipe(self, name: str, inlet: str, length: float = 100.0,
                 diameter: float = 0.1, elevation: float = 0.0) -> 'ProcessBuilder':
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
    
    def run(self) -> 'ProcessBuilder':
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


def stream(name: str, thermoSystem: Any, t: float = 0, p: float = 0, 
           process: Any = None) -> Any:
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
    processoperations = jneqsim.process.processmodel.ProcessSystem.open(filename)
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
    sep = jneqsim.process.equipment.separator.ThreePhaseSeparator(
        name, teststream
    )
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


def compressor(name: str, teststream: Any, pres: float = 10.0, 
               process: Any = None) -> Any:
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
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def pumpChart(pump, curveConditions, speed, flow, head, polyEff):
    pump.getPumpChart().setCurves(
        JDouble[:](curveConditions),
        JDouble[:](speed),
        JDouble[:][:](flow),
        JDouble[:][:](head),
        JDouble[:][:](polyEff),
    )


def compressorSurgeCurve(compressor, curveConditions, surgeflow, surgehead):
    compressor.getCompressorChart().getSurgeCurve().setCurve(
        JDouble[:](curveConditions), JDouble[:](surgeflow), JDouble[:](surgehead)
    )


def compressorStoneWallCurve(compressor, curveConditions, stoneWallflow, stoneWallHead):
    compressor.getCompressorChart().getStoneWallCurve().setCurve(
        JDouble[:](curveConditions),
        JDouble[:](stoneWallflow),
        JDouble[:](stoneWallHead),
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


def splitter(name: str, teststream: Any, splitfactors: List[float] = None, 
             process: Any = None) -> Any:
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
        spl.setSplitFactors(JDouble[:](splitfactors))
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


def heatExchanger(name: str, stream1: Any, stream2: Any = None, 
                  process: Any = None) -> Any:
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
                row = {'Unit Name': unit_name}
                # Extract common properties
                if 'feed' in unit_data:
                    feed = unit_data['feed']
                    if 'temperature' in feed:
                        row['Feed Temp [C]'] = feed.get('temperature', {}).get('value')
                    if 'pressure' in feed:
                        row['Feed Pres [bara]'] = feed.get('pressure', {}).get('value')
                if 'product' in unit_data:
                    product = unit_data['product']
                    if 'temperature' in product:
                        row['Product Temp [C]'] = product.get('temperature', {}).get('value')
                    if 'pressure' in product:
                        row['Product Pres [bara]'] = product.get('pressure', {}).get('value')
                if 'power' in unit_data:
                    row['Power [kW]'] = unit_data.get('power', {}).get('value')
                rows.append(row)

        if rows:
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame({'Message': ['No unit operations found in process']})

    except Exception as e:
        return pd.DataFrame({'Error': [f'Failed to generate report: {e}']})


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
            with open(filename, "w") as json_file:
                json.dump(results, json_file, indent=4)
            print(f"JSON report saved to {filename}")

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
    ejector_unit = jneqsim.process.equipment.ejector.Ejector(name, motive_stream, suction_stream)
    if not _loop_mode:
        processoperations.add(ejector_unit)
    return ejector_unit


def flare(name: str, inlet_stream: Any, flame_height: float = 30.0,
          radiant_fraction: float = 0.18, tip_diameter: float = 0.3) -> Any:
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


def safety_valve(name: str, inlet_stream: Any, set_pressure: float,
                 full_open_pressure: float = None, blowdown: float = 7.0) -> Any:
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


def beggs_brill_pipe(name: str, inlet_stream: Any, length: float,
                     diameter: float, elevation: float = 0.0,
                     roughness: float = 50e-6) -> Any:
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
    return jneqsim.process.equipment.EquipmentFactory.createEquipment(name, equipment_type)


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
        elec = jneqsim.process.equipment.electrolyzer.CO2Electrolyzer(name, inlet_stream)
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


def wellflow(name: str, inlet_stream: Any, well_depth: float = 1000.0,
             well_diameter: float = 0.1) -> Any:
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