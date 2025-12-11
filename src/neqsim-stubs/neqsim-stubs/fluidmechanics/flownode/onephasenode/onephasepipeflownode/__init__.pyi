
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import neqsim.fluidmechanics.flownode.onephasenode
import neqsim.fluidmechanics.geometrydefinitions
import neqsim.thermo.system
import typing



class onePhasePipeFlowNode(neqsim.fluidmechanics.flownode.onephasenode.onePhaseFlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface, geometryDefinitionInterface: neqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    def calcReynoldsNumber(self) -> float: ...
    def clone(self) -> 'onePhasePipeFlowNode': ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode")``.

    onePhasePipeFlowNode: typing.Type[onePhasePipeFlowNode]
