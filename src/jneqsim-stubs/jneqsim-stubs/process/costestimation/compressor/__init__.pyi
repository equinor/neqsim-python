import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.costestimation
import jneqsim.process.mechanicaldesign.compressor
import typing

class CompressorCostEstimate(jneqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(
        self,
        compressorMechanicalDesign: jneqsim.process.mechanicaldesign.compressor.CompressorMechanicalDesign,
    ): ...
    def getTotalCost(self) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.costestimation.compressor")``.

    CompressorCostEstimate: typing.Type[CompressorCostEstimate]
