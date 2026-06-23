import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.fluidboundarynonreactive
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.fluidboundarysystemreactive
import typing

class FluidBoundarySystemInterface:
    def addBoundary(
        self,
        fluidBoundaryInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface,
    ) -> None: ...
    def createSystem(self) -> None: ...
    def getFilmThickness(self) -> float: ...
    def getFluidBoundary(
        self,
    ) -> (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface
    ): ...
    def getNode(
        self, int: int
    ) -> (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.FluidBoundaryNodeInterface
    ): ...
    def getNodeLength(self) -> float: ...
    def getNumberOfNodes(self) -> int: ...
    def setFilmThickness(self, double: float) -> None: ...
    def setNumberOfNodes(self, int: int) -> None: ...
    def solve(self) -> None: ...

class FluidBoundarySystem(FluidBoundarySystemInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self,
        fluidBoundaryInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface,
    ): ...
    def addBoundary(
        self,
        fluidBoundaryInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface,
    ) -> None: ...
    def createSystem(self) -> None: ...
    def getFilmThickness(self) -> float: ...
    def getFluidBoundary(
        self,
    ) -> (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface
    ): ...
    def getNode(
        self, int: int
    ) -> (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.FluidBoundaryNodeInterface
    ): ...
    def getNodeLength(self) -> float: ...
    def getNumberOfNodes(self) -> int: ...
    def setFilmThickness(self, double: float) -> None: ...
    def setNumberOfNodes(self, int: int) -> None: ...
    def solve(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem")``.

    FluidBoundarySystem: typing.Type[FluidBoundarySystem]
    FluidBoundarySystemInterface: typing.Type[FluidBoundarySystemInterface]
    fluidboundarynonreactive: (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.fluidboundarynonreactive.__module_protocol__
    )
    fluidboundarysystemreactive: (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.fluidboundarysystemreactive.__module_protocol__
    )
