
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import neqsim.process.costestimation.compressor
import neqsim.process.costestimation.separator
import neqsim.process.costestimation.valve
import neqsim.process.mechanicaldesign
import typing



class CostEstimateBaseClass(java.io.Serializable):
    @typing.overload
    def __init__(self, systemMechanicalDesign: neqsim.process.mechanicaldesign.SystemMechanicalDesign): ...
    @typing.overload
    def __init__(self, systemMechanicalDesign: neqsim.process.mechanicaldesign.SystemMechanicalDesign, double: float): ...
    def equals(self, object: typing.Any) -> bool: ...
    def getCAPEXestimate(self) -> float: ...
    def getWeightBasedCAPEXEstimate(self) -> float: ...
    def hashCode(self) -> int: ...

class UnitCostEstimateBaseClass(java.io.Serializable):
    mechanicalEquipment: neqsim.process.mechanicaldesign.MechanicalDesign = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, mechanicalDesign: neqsim.process.mechanicaldesign.MechanicalDesign): ...
    def equals(self, object: typing.Any) -> bool: ...
    def getTotalCost(self) -> float: ...
    def hashCode(self) -> int: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.costestimation")``.

    CostEstimateBaseClass: typing.Type[CostEstimateBaseClass]
    UnitCostEstimateBaseClass: typing.Type[UnitCostEstimateBaseClass]
    compressor: neqsim.process.costestimation.compressor.__module_protocol__
    separator: neqsim.process.costestimation.separator.__module_protocol__
    valve: neqsim.process.costestimation.valve.__module_protocol__
