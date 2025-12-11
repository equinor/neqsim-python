
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flownode
import neqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode
import neqsim.fluidmechanics.geometrydefinitions
import neqsim.thermo.system
import typing



class onePhaseFlowNode(neqsim.fluidmechanics.flownode.FlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface, geometryDefinitionInterface: neqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    def calcReynoldsNumber(self) -> float: ...
    def clone(self) -> 'onePhaseFlowNode': ...
    def increaseMolarRate(self, double: float) -> None: ...
    def init(self) -> None: ...
    def initFlowCalc(self) -> None: ...
    def updateMolarFlow(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flownode.onephasenode")``.

    onePhaseFlowNode: typing.Type[onePhaseFlowNode]
    onephasepipeflownode: neqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode.__module_protocol__
