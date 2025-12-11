
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.fluidmechanics.flownode.onephasenode
import jneqsim.fluidmechanics.geometrydefinitions
import jneqsim.thermo.system
import typing



class onePhasePipeFlowNode(jneqsim.fluidmechanics.flownode.onephasenode.onePhaseFlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface, geometryDefinitionInterface: jneqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    def calcReynoldsNumber(self) -> float: ...
    def clone(self) -> 'onePhasePipeFlowNode': ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.onephasenode.onephasepipeflownode")``.

    onePhasePipeFlowNode: typing.Type[onePhasePipeFlowNode]
