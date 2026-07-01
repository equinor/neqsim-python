
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.fluidmechanics.flowsystem
import jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.onephaseflowvisualization
import jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization
import typing



class FlowSystemVisualizationInterface:
    def displayResult(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface, double: float) -> None: ...
    def setPoints(self) -> None: ...

class FlowSystemVisualization(FlowSystemVisualizationInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def displayResult(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface) -> None: ...
    @typing.overload
    def setNextData(self, flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface, double: float) -> None: ...
    def setPoints(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization")``.

    FlowSystemVisualization: typing.Type[FlowSystemVisualization]
    FlowSystemVisualizationInterface: typing.Type[FlowSystemVisualizationInterface]
    onephaseflowvisualization: jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.onephaseflowvisualization.__module_protocol__
    twophaseflowvisualization: jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization.__module_protocol__
