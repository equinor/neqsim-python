
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import neqsim.fluidmechanics.flownode
import neqsim.fluidmechanics.flownode.multiphasenode
import neqsim.fluidmechanics.flownode.twophasenode.twophasepipeflownode
import neqsim.fluidmechanics.geometrydefinitions
import neqsim.thermo.system
import typing



class WaxDepositionFlowNode(neqsim.fluidmechanics.flownode.multiphasenode.MultiPhaseFlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface, geometryDefinitionInterface: neqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface, systemInterface2: neqsim.thermo.system.SystemInterface, geometryDefinitionInterface: neqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface): ...
    def calcContactLength(self) -> float: ...
    def clone(self) -> neqsim.fluidmechanics.flownode.twophasenode.twophasepipeflownode.StratifiedFlowNode: ...
    def getNextNode(self) -> neqsim.fluidmechanics.flownode.FlowNodeInterface: ...
    def init(self) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flownode.multiphasenode.waxnode")``.

    WaxDepositionFlowNode: typing.Type[WaxDepositionFlowNode]
