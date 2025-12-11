
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization
import neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.util.fluidmechanicsvisualization")``.

    flownodevisualization: neqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization.__module_protocol__
    flowsystemvisualization: neqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.__module_protocol__
