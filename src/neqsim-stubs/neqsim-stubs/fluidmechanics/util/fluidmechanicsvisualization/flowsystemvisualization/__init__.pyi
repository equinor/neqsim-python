
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.fluidmechanics.flowsystem
import neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.onephaseflowvisualization
import neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization
import typing



class FlowSystemVisualizationInterface:
    def displayResult(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: neqsim.fluidmechanics.flowsystem.FlowSystemInterface) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: neqsim.fluidmechanics.flowsystem.FlowSystemInterface, double: float) -> None: ...
    def setPoints(self) -> None: ...

class FlowSystemVisualization(FlowSystemVisualizationInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def displayResult(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: neqsim.fluidmechanics.flowsystem.FlowSystemInterface) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: neqsim.fluidmechanics.flowsystem.FlowSystemInterface, double: float) -> None: ...
    def setPoints(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization")``.

    FlowSystemVisualization: typing.Type[FlowSystemVisualization]
    FlowSystemVisualizationInterface: typing.Type[FlowSystemVisualizationInterface]
    onephaseflowvisualization: neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.onephaseflowvisualization.__module_protocol__
    twophaseflowvisualization: neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization.__module_protocol__
