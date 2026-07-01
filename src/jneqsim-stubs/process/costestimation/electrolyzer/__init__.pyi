import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign.electrolyzer
import typing

class ElectrolyzerCostEstimate(
    jneqsim.process.costestimation.UnitCostEstimateBaseClass
):
    def __init__(
        self,
        electrolyzerMechanicalDesign: jneqsim.process.mechanicaldesign.electrolyzer.ElectrolyzerMechanicalDesign,
    ): ...
    def getSpecificCapexUsdPerKw(self) -> float: ...
    def getTechnology(self) -> java.lang.String: ...
    def setIncludeBalanceOfPlant(self, boolean: bool) -> None: ...
    def setTechnology(self, string: typing.Union[java.lang.String, str]) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.electrolyzer")``.

    ElectrolyzerCostEstimate: typing.Type[ElectrolyzerCostEstimate]
