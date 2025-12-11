
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.fluidboundarynonreactivenode
import neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.fluidboundaryreactivenode
import neqsim.thermo.system
import typing



class FluidBoundaryNodeInterface:
    def getBulkSystem(self) -> neqsim.thermo.system.SystemInterface: ...

class FluidBoundaryNode(FluidBoundaryNodeInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface): ...
    def getBulkSystem(self) -> neqsim.thermo.system.SystemInterface: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode")``.

    FluidBoundaryNode: typing.Type[FluidBoundaryNode]
    FluidBoundaryNodeInterface: typing.Type[FluidBoundaryNodeInterface]
    fluidboundarynonreactivenode: neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.fluidboundarynonreactivenode.__module_protocol__
    fluidboundaryreactivenode: neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.finitevolumeboundary.fluidboundarynode.fluidboundaryreactivenode.__module_protocol__
