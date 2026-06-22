
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode
import jneqsim.fluidmechanics.geometrydefinitions
import jneqsim.thermo.system
import typing



class onePhaseFlowNode(jneqsim.fluidmechanics.flownode.FlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface, geometryDefinitionInterface: jneqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    def calcReynoldsNumber(self) -> float: ...
    def clone(self) -> 'onePhaseFlowNode': ...
    def increaseMolarRate(self, double: float) -> None: ...
    def init(self) -> None: ...
    def initFlowCalc(self) -> None: ...
    def updateMolarFlow(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.onephasenode")``.

    onePhaseFlowNode: typing.Type[onePhaseFlowNode]
    onephasepipeflownode: jneqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode.__module_protocol__
