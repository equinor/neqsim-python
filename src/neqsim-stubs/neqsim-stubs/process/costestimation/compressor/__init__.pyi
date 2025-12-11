
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.process.costestimation
import neqsim.process.mechanicaldesign.compressor
import typing



class CompressorCostEstimate(neqsim.process.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, compressorMechanicalDesign: neqsim.process.mechanicaldesign.compressor.CompressorMechanicalDesign): ...
    def getTotalCost(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.costestimation.compressor")``.

    CompressorCostEstimate: typing.Type[CompressorCostEstimate]
