import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc
import jneqsim.thermo.system
import typing

class EquilibriumFluidBoundary(
    jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundary
):
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def calcFluxes(self) -> typing.MutableSequence[float]: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def solve(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.equilibriumfluidboundary")``.

    EquilibriumFluidBoundary: typing.Type[EquilibriumFluidBoundary]
