
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc
import jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem
import typing



class FluidBoundarySystemReactive(jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.FluidBoundarySystem):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, fluidBoundaryInterface: jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.FluidBoundaryInterface): ...
    def createSystem(self) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarysystem.fluidboundarysystemreactive")``.

    FluidBoundarySystemReactive: typing.Type[FluidBoundarySystemReactive]
