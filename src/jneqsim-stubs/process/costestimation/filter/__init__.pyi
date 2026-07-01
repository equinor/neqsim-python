
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign.filter
import typing



class FilterCostEstimate(jneqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, filterMechanicalDesign: jneqsim.process.mechanicaldesign.filter.FilterMechanicalDesign): ...
    def setAuxiliariesFraction(self, double: float) -> None: ...
    def setElementCostUSD(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.filter")``.

    FilterCostEstimate: typing.Type[FilterCostEstimate]
