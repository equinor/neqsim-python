
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flownode
import neqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization
import typing



class TwoPhaseFlowNodeVisualization(neqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization.FlowNodeVisualization):
    def __init__(self): ...
    def setData(self, flowNodeInterface: neqsim.fluidmechanics.flownode.FlowNodeInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization.twophaseflownodevisualization")``.

    TwoPhaseFlowNodeVisualization: typing.Type[TwoPhaseFlowNodeVisualization]
