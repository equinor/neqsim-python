import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flowsystem
import jneqsim.fluidmechanics.flowsystem.onephaseflowsystem.pipeflowsystem
import jneqsim.fluidmechanics.geometrydefinitions.pipe
import jneqsim.thermo.system
import typing

class OnePhaseFlowSystem(jneqsim.fluidmechanics.flowsystem.FlowSystem):
    pipe: jneqsim.fluidmechanics.geometrydefinitions.pipe.PipeData = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flowsystem.onephaseflowsystem")``.

    OnePhaseFlowSystem: typing.Type[OnePhaseFlowSystem]
    pipeflowsystem: (
        jneqsim.fluidmechanics.flowsystem.onephaseflowsystem.pipeflowsystem.__module_protocol__
    )
