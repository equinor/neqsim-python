import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.process.equipment
import jneqsim.process.equipment.valve
import jneqsim.process.logic
import jneqsim.process.processmodel
import typing

class PressureControlLogic(jneqsim.process.logic.ProcessLogic):
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        controlValve: jneqsim.process.equipment.valve.ControlValve,
        double: float,
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        controlValve: jneqsim.process.equipment.valve.ControlValve,
        double: float,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
    ): ...
    def activate(self) -> None: ...
    def deactivate(self) -> None: ...
    def execute(self, double: float) -> None: ...
    def getControlValve(self) -> jneqsim.process.equipment.valve.ControlValve: ...
    def getName(self) -> java.lang.String: ...
    def getState(self) -> jneqsim.process.logic.LogicState: ...
    def getStatusDescription(self) -> java.lang.String: ...
    def getTargetEquipment(
        self,
    ) -> java.util.List[jneqsim.process.equipment.ProcessEquipmentInterface]: ...
    def getTargetOpening(self) -> float: ...
    def isActive(self) -> bool: ...
    def isComplete(self) -> bool: ...
    def reset(self) -> bool: ...
    def toString(self) -> java.lang.String: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.logic.control")``.

    PressureControlLogic: typing.Type[PressureControlLogic]
