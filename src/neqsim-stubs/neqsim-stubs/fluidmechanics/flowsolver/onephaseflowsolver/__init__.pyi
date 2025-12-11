
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowsolver
import neqsim.fluidmechanics.flowsolver.onephaseflowsolver.onephasepipeflowsolver
import typing



class OnePhaseFlowSolver(neqsim.fluidmechanics.flowsolver.FlowSolver):
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flowsolver.onephaseflowsolver")``.

    OnePhaseFlowSolver: typing.Type[OnePhaseFlowSolver]
    onephasepipeflowsolver: neqsim.fluidmechanics.flowsolver.onephaseflowsolver.onephasepipeflowsolver.__module_protocol__
