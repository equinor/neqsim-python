
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowleg
import neqsim.fluidmechanics.flownode
import typing



class PipeLeg(neqsim.fluidmechanics.flowleg.FlowLeg):
    def __init__(self): ...
    @typing.overload
    def createFlowNodes(self) -> None: ...
    @typing.overload
    def createFlowNodes(self, flowNodeInterface: neqsim.fluidmechanics.flownode.FlowNodeInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flowleg.pipeleg")``.

    PipeLeg: typing.Type[PipeLeg]
