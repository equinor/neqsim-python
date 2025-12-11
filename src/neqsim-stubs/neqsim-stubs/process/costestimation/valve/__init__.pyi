
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.process.costestimation
import neqsim.process.mechanicaldesign.valve
import typing



class ValveCostEstimate(neqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, valveMechanicalDesign: neqsim.process.mechanicaldesign.valve.ValveMechanicalDesign): ...
    def getTotalCost(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.costestimation.valve")``.

    ValveCostEstimate: typing.Type[ValveCostEstimate]
