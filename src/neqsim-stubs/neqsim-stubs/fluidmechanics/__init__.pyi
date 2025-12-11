
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowleg
import neqsim.fluidmechanics.flownode
import neqsim.fluidmechanics.flowsolver
import neqsim.fluidmechanics.flowsystem
import neqsim.fluidmechanics.geometrydefinitions
import neqsim.fluidmechanics.util
import typing



class FluidMech:
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics")``.

    FluidMech: typing.Type[FluidMech]
    flowleg: neqsim.fluidmechanics.flowleg.__module_protocol__
    flownode: neqsim.fluidmechanics.flownode.__module_protocol__
    flowsolver: neqsim.fluidmechanics.flowsolver.__module_protocol__
    flowsystem: neqsim.fluidmechanics.flowsystem.__module_protocol__
    geometrydefinitions: neqsim.fluidmechanics.geometrydefinitions.__module_protocol__
    util: neqsim.fluidmechanics.util.__module_protocol__
