import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver
import typing

class FluidBoundaryReactiveSolver(
    jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver.FluidBoundarySolver
):
    def __init__(self): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysolver.fluidboundaryreactivesolver")``.

    FluidBoundaryReactiveSolver: typing.Type[FluidBoundaryReactiveSolver]
