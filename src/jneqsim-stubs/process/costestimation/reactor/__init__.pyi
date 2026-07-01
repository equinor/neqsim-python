import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign.reactor
import typing

class ReactorCostEstimate(jneqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(
        self,
        reactorMechanicalDesign: jneqsim.process.mechanicaldesign.reactor.ReactorMechanicalDesign,
    ): ...
    def setCatalystCostUSDPerKg(self, double: float) -> None: ...
    def setInternalsFraction(self, double: float) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.reactor")``.

    ReactorCostEstimate: typing.Type[ReactorCostEstimate]
