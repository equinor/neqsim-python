
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flowsolver.twophaseflowsolver.stirredcellsolver
import neqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flowsolver.twophaseflowsolver")``.

    stirredcellsolver: neqsim.fluidmechanics.flowsolver.twophaseflowsolver.stirredcellsolver.__module_protocol__
    twophasepipeflowsolver: neqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver.__module_protocol__
