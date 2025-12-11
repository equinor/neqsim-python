
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization
import jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.util.fluidmechanicsvisualization")``.

    flownodevisualization: jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flownodevisualization.__module_protocol__
    flowsystemvisualization: jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.__module_protocol__
