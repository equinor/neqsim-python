
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc
import neqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.flownode.fluidboundary")``.

    heatmasstransfercalc: neqsim.fluidmechanics.flownode.fluidboundary.heatmasstransfercalc.__module_protocol__
    interphasetransportcoefficient: neqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.__module_protocol__
