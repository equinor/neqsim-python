import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.stirredcellsolver
import jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flowsolver.twophaseflowsolver")``.

    stirredcellsolver: (
        jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.stirredcellsolver.__module_protocol__
    )
    twophasepipeflowsolver: (
        jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver.__module_protocol__
    )
