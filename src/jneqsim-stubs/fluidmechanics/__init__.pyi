import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flowleg
import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flowsolver
import jneqsim.fluidmechanics.flowsystem
import jneqsim.fluidmechanics.geometrydefinitions
import jneqsim.fluidmechanics.util
import typing

class FluidMech:
    def __init__(self): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics")``.

    FluidMech: typing.Type[FluidMech]
    flowleg: jneqsim.fluidmechanics.flowleg.__module_protocol__
    flownode: jneqsim.fluidmechanics.flownode.__module_protocol__
    flowsolver: jneqsim.fluidmechanics.flowsolver.__module_protocol__
    flowsystem: jneqsim.fluidmechanics.flowsystem.__module_protocol__
    geometrydefinitions: jneqsim.fluidmechanics.geometrydefinitions.__module_protocol__
    util: jneqsim.fluidmechanics.util.__module_protocol__
