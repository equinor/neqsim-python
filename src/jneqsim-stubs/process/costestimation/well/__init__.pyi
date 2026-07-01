import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign
import typing

class WellFlowCostEstimate(jneqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(
        self, mechanicalDesign: jneqsim.process.mechanicaldesign.MechanicalDesign
    ): ...
    def calculateCostEstimate(self) -> None: ...
    def getTotalCost(self) -> float: ...
    def getWellCapexUsd(self) -> float: ...
    def setWellCapexUsd(self, double: float) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.well")``.

    WellFlowCostEstimate: typing.Type[WellFlowCostEstimate]
