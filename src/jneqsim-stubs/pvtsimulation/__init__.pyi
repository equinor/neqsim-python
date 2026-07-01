import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.pvtsimulation.flowassurance
import jneqsim.pvtsimulation.modeltuning
import jneqsim.pvtsimulation.regression
import jneqsim.pvtsimulation.reservoirproperties
import jneqsim.pvtsimulation.simulation
import jneqsim.pvtsimulation.util
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.pvtsimulation")``.

    flowassurance: jneqsim.pvtsimulation.flowassurance.__module_protocol__
    modeltuning: jneqsim.pvtsimulation.modeltuning.__module_protocol__
    regression: jneqsim.pvtsimulation.regression.__module_protocol__
    reservoirproperties: jneqsim.pvtsimulation.reservoirproperties.__module_protocol__
    simulation: jneqsim.pvtsimulation.simulation.__module_protocol__
    util: jneqsim.pvtsimulation.util.__module_protocol__
