import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jpype
import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.twophasenode.twophasepipeflownode
import jneqsim.fluidmechanics.flownode.twophasenode.twophasereactorflownode
import jneqsim.fluidmechanics.flownode.twophasenode.twophasestirredcellnode
import jneqsim.fluidmechanics.geometrydefinitions
import jneqsim.thermo.system
import typing

class TwoPhaseFlowNode(jneqsim.fluidmechanics.flownode.FlowNode):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self,
        systemInterface: jneqsim.thermo.system.SystemInterface,
        geometryDefinitionInterface: jneqsim.fluidmechanics.geometrydefinitions.GeometryDefinitionInterface,
    ): ...
    def calcContactLength(self) -> float: ...
    def calcFluxes(self) -> None: ...
    def calcGasLiquidContactArea(self) -> float: ...
    def calcHydraulicDiameter(self) -> float: ...
    def calcReynoldNumber(self) -> float: ...
    def calcWallFrictionFactor(self) -> float: ...
    def clone(self) -> "TwoPhaseFlowNode": ...
    def init(self) -> None: ...
    def initFlowCalc(self) -> None: ...
    def initVelocity(self) -> float: ...
    def setFluxes(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...
    @typing.overload
    def update(self) -> None: ...
    @typing.overload
    def update(self, double: float) -> None: ...
    def updateMolarFlow(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.twophasenode")``.

    TwoPhaseFlowNode: typing.Type[TwoPhaseFlowNode]
    twophasepipeflownode: (
        jneqsim.fluidmechanics.flownode.twophasenode.twophasepipeflownode.__module_protocol__
    )
    twophasereactorflownode: (
        jneqsim.fluidmechanics.flownode.twophasenode.twophasereactorflownode.__module_protocol__
    )
    twophasestirredcellnode: (
        jneqsim.fluidmechanics.flownode.twophasenode.twophasestirredcellnode.__module_protocol__
    )
