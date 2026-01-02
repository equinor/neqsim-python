
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
import jneqsim.process.calibration
import jneqsim.process.conditionmonitor
import jneqsim.process.controllerdevice
import jneqsim.process.costestimation
import jneqsim.process.equipment
import jneqsim.process.fielddevelopment
import jneqsim.process.integration
import jneqsim.process.logic
import jneqsim.process.measurementdevice
import jneqsim.process.mechanicaldesign
import jneqsim.process.ml
import jneqsim.process.mpc
import jneqsim.process.processmodel
import jneqsim.process.safety
import jneqsim.process.streaming
import jneqsim.process.sustainability
import jneqsim.process.util
import jneqsim.util
import typing



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

    SimulationBaseClass: typing.Type[SimulationBaseClass]
    SimulationInterface: typing.Type[SimulationInterface]
    advisory: jneqsim.process.advisory.__module_protocol__
    alarm: jneqsim.process.alarm.__module_protocol__
    calibration: jneqsim.process.calibration.__module_protocol__
    conditionmonitor: jneqsim.process.conditionmonitor.__module_protocol__
    controllerdevice: jneqsim.process.controllerdevice.__module_protocol__
    costestimation: jneqsim.process.costestimation.__module_protocol__
    equipment: jneqsim.process.equipment.__module_protocol__
    fielddevelopment: jneqsim.process.fielddevelopment.__module_protocol__
    integration: jneqsim.process.integration.__module_protocol__
    logic: jneqsim.process.logic.__module_protocol__
    measurementdevice: jneqsim.process.measurementdevice.__module_protocol__
    mechanicaldesign: jneqsim.process.mechanicaldesign.__module_protocol__
    ml: jneqsim.process.ml.__module_protocol__
    mpc: jneqsim.process.mpc.__module_protocol__
    processmodel: jneqsim.process.processmodel.__module_protocol__
    safety: jneqsim.process.safety.__module_protocol__
    streaming: jneqsim.process.streaming.__module_protocol__
    sustainability: jneqsim.process.sustainability.__module_protocol__
    util: jneqsim.process.util.__module_protocol__
