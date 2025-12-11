
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowsystem
import neqsim.fluidmechanics.flowsystem.twophaseflowsystem.shipsystem
import neqsim.fluidmechanics.flowsystem.twophaseflowsystem.stirredcellsystem
import neqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasepipeflowsystem
import neqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasereactorflowsystem
import neqsim.fluidmechanics.geometrydefinitions.pipe
import neqsim.thermo.system
import typing



class TwoPhaseFlowSystem(neqsim.fluidmechanics.flowsystem.FlowSystem):
    pipe: neqsim.fluidmechanics.geometrydefinitions.pipe.PipeData = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flowsystem.twophaseflowsystem")``.

    TwoPhaseFlowSystem: typing.Type[TwoPhaseFlowSystem]
    shipsystem: neqsim.fluidmechanics.flowsystem.twophaseflowsystem.shipsystem.__module_protocol__
    stirredcellsystem: neqsim.fluidmechanics.flowsystem.twophaseflowsystem.stirredcellsystem.__module_protocol__
    twophasepipeflowsystem: neqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasepipeflowsystem.__module_protocol__
    twophasereactorflowsystem: neqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasereactorflowsystem.__module_protocol__
