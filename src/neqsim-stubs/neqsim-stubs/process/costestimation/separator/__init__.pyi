
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.process.costestimation
import neqsim.process.mechanicaldesign.separator
import typing



class SeparatorCostEstimate(neqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, separatorMechanicalDesign: neqsim.process.mechanicaldesign.separator.SeparatorMechanicalDesign): ...
    def getTotalCost(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.costestimation.separator")``.

    SeparatorCostEstimate: typing.Type[SeparatorCostEstimate]
