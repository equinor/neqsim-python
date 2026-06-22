
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jneqsim.process.advisory
import jneqsim.process.alarm
import jneqsim.process.automation
import jneqsim.process.calibration
import jneqsim.process.chemistry
import jneqsim.process.conditionmonitor
import jneqsim.process.controllerdevice
import jneqsim.process.corrosion
import jneqsim.process.costestimation
import jneqsim.process.design
import jneqsim.process.diagnostics
import jneqsim.process.dynamics
import jneqsim.process.electricaldesign
import jneqsim.process.equipment
import jneqsim.process.examples
import jneqsim.process.fielddevelopment
import jneqsim.process.hydrogen
import jneqsim.process.instrumentdesign
import jneqsim.process.integration
import jneqsim.process.logic
import jneqsim.process.materials
import jneqsim.process.measurementdevice
import jneqsim.process.mechanicaldesign
import jneqsim.process.ml
import jneqsim.process.mpc
import jneqsim.process.operations
import jneqsim.process.optimization
import jneqsim.process.processmodel
import jneqsim.process.research
import jneqsim.process.safety
import jneqsim.process.streaming
import jneqsim.process.sustainability
import jneqsim.process.synthesis
import jneqsim.process.util
import jneqsim.util
import typing



class ProcessElementInterface(jneqsim.util.NamedInterface, java.io.Serializable): ...

class SimulationInterface(jneqsim.util.NamedInterface, java.lang.Runnable, java.io.Serializable):
    def getCalculateSteadyState(self) -> bool: ...
    def getCalculationIdentifier(self) -> java.util.UUID: ...
    def getReport_json(self) -> java.lang.String: ...
    def getTime(self) -> float: ...
    def increaseTime(self, double: float) -> None: ...
    def isRunInSteps(self) -> bool: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def runTransient(self, double: float) -> None: ...
    @typing.overload
    def runTransient(self, double: float, uUID: java.util.UUID) -> None: ...
    @typing.overload
    def run_step(self, uUID: java.util.UUID) -> None: ...
    @typing.overload
    def run_step(self) -> None: ...
    def setCalculateSteadyState(self, boolean: bool) -> None: ...
    def setCalculationIdentifier(self, uUID: java.util.UUID) -> None: ...
    def setRunInSteps(self, boolean: bool) -> None: ...
    def setTime(self, double: float) -> None: ...
    def solved(self) -> bool: ...

class SimulationBaseClass(jneqsim.util.NamedBaseClass, SimulationInterface):
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    def getCalculateSteadyState(self) -> bool: ...
    def getCalculationIdentifier(self) -> java.util.UUID: ...
    def getTime(self) -> float: ...
    def increaseTime(self, double: float) -> None: ...
    def isRunInSteps(self) -> bool: ...
    def setCalculateSteadyState(self, boolean: bool) -> None: ...
    def setCalculationIdentifier(self, uUID: java.util.UUID) -> None: ...
    def setRunInSteps(self, boolean: bool) -> None: ...
    def setTime(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process")``.

    ProcessElementInterface: typing.Type[ProcessElementInterface]
    SimulationBaseClass: typing.Type[SimulationBaseClass]
    SimulationInterface: typing.Type[SimulationInterface]
    advisory: jneqsim.process.advisory.__module_protocol__
    alarm: jneqsim.process.alarm.__module_protocol__
    automation: jneqsim.process.automation.__module_protocol__
    calibration: jneqsim.process.calibration.__module_protocol__
    chemistry: jneqsim.process.chemistry.__module_protocol__
    conditionmonitor: jneqsim.process.conditionmonitor.__module_protocol__
    controllerdevice: jneqsim.process.controllerdevice.__module_protocol__
    corrosion: jneqsim.process.corrosion.__module_protocol__
    costestimation: jneqsim.process.costestimation.__module_protocol__
    design: jneqsim.process.design.__module_protocol__
    diagnostics: jneqsim.process.diagnostics.__module_protocol__
    dynamics: jneqsim.process.dynamics.__module_protocol__
    electricaldesign: jneqsim.process.electricaldesign.__module_protocol__
    equipment: jneqsim.process.equipment.__module_protocol__
    examples: jneqsim.process.examples.__module_protocol__
    fielddevelopment: jneqsim.process.fielddevelopment.__module_protocol__
    hydrogen: jneqsim.process.hydrogen.__module_protocol__
    instrumentdesign: jneqsim.process.instrumentdesign.__module_protocol__
    integration: jneqsim.process.integration.__module_protocol__
    logic: jneqsim.process.logic.__module_protocol__
    materials: jneqsim.process.materials.__module_protocol__
    measurementdevice: jneqsim.process.measurementdevice.__module_protocol__
    mechanicaldesign: jneqsim.process.mechanicaldesign.__module_protocol__
    ml: jneqsim.process.ml.__module_protocol__
    mpc: jneqsim.process.mpc.__module_protocol__
    operations: jneqsim.process.operations.__module_protocol__
    optimization: jneqsim.process.optimization.__module_protocol__
    processmodel: jneqsim.process.processmodel.__module_protocol__
    research: jneqsim.process.research.__module_protocol__
    safety: jneqsim.process.safety.__module_protocol__
    streaming: jneqsim.process.streaming.__module_protocol__
    sustainability: jneqsim.process.sustainability.__module_protocol__
    synthesis: jneqsim.process.synthesis.__module_protocol__
    util: jneqsim.process.util.__module_protocol__
