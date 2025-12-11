
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowsystem
import neqsim.fluidmechanics.flowsystem.onephaseflowsystem.pipeflowsystem
import neqsim.fluidmechanics.geometrydefinitions.pipe
import neqsim.thermo.system
import typing



class OnePhaseFlowSystem(neqsim.fluidmechanics.flowsystem.FlowSystem):
    pipe: neqsim.fluidmechanics.geometrydefinitions.pipe.PipeData = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flowsystem.onephaseflowsystem")``.

    OnePhaseFlowSystem: typing.Type[OnePhaseFlowSystem]
    pipeflowsystem: neqsim.fluidmechanics.flowsystem.onephaseflowsystem.pipeflowsystem.__module_protocol__
