
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.pvtsimulation.modeltuning
import neqsim.pvtsimulation.reservoirproperties
import neqsim.pvtsimulation.simulation
import neqsim.pvtsimulation.util
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.pvtsimulation")``.

    modeltuning: neqsim.pvtsimulation.modeltuning.__module_protocol__
    reservoirproperties: neqsim.pvtsimulation.reservoirproperties.__module_protocol__
    simulation: neqsim.pvtsimulation.simulation.__module_protocol__
    util: neqsim.pvtsimulation.util.__module_protocol__
