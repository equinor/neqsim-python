import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver.fluidboundaryreactivesolver
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem
import typing

class FluidBoundarySolverInterface:
    def getMolarFlux(self, int: int) -> float: ...
    def solve(self) -> None: ...

class FluidBoundarySolver(FluidBoundarySolverInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self,
        fluidBoundarySystemInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.FluidBoundarySystemInterface,
    ): ...
    @typing.overload
    def __init__(
        self,
        fluidBoundarySystemInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.FluidBoundarySystemInterface,
        boolean: bool,
    ): ...
    def getMolarFlux(self, int: int) -> float: ...
    def initComposition(self, int: int) -> None: ...
    def initMatrix(self) -> None: ...
    def initProfiles(self) -> None: ...
    def setComponentConservationMatrix(self, int: int) -> None: ...
    def solve(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver")``.

    FluidBoundarySolver: typing.Type[FluidBoundarySolver]
    FluidBoundarySolverInterface: typing.Type[FluidBoundarySolverInterface]
    fluidboundaryreactivesolver: (
        jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver.fluidboundaryreactivesolver.__module_protocol__
    )
