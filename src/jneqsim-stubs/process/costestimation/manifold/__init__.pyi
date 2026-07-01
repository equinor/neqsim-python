
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign.manifold
import typing



class ManifoldCostEstimate(jneqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, manifoldMechanicalDesign: jneqsim.process.mechanicaldesign.manifold.ManifoldMechanicalDesign): ...
    def setBaseCostUSDPerKg(self, double: float) -> None: ...
    def setBranchAllowanceUSD(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.manifold")``.

    ManifoldCostEstimate: typing.Type[ManifoldCostEstimate]
