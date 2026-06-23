import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flowsystem
import jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.shipsystem
import jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.stirredcellsystem
import jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasepipeflowsystem
import jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasereactorflowsystem
import jneqsim.fluidmechanics.geometrydefinitions.pipe
import jneqsim.thermo.system
import typing

class TwoPhaseFlowSystem(jneqsim.fluidmechanics.flowsystem.FlowSystem):
    pipe: jneqsim.fluidmechanics.geometrydefinitions.pipe.PipeData = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flowsystem.twophaseflowsystem")``.

    TwoPhaseFlowSystem: typing.Type[TwoPhaseFlowSystem]
    shipsystem: (
        jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.shipsystem.__module_protocol__
    )
    stirredcellsystem: (
        jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.stirredcellsystem.__module_protocol__
    )
    twophasepipeflowsystem: (
        jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasepipeflowsystem.__module_protocol__
    )
    twophasereactorflowsystem: (
        jneqsim.fluidmechanics.flowsystem.twophaseflowsystem.twophasereactorflowsystem.__module_protocol__
    )
