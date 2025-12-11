
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.statistics.experimentalequipmentdata
import typing



class WettedWallColumnData(neqsim.statistics.experimentalequipmentdata.ExperimentalEquipmentData):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    def getDiameter(self) -> float: ...
    def getLength(self) -> float: ...
    def getVolume(self) -> float: ...
    def setDiameter(self, double: float) -> None: ...
    def setLength(self, double: float) -> None: ...
    def setVolume(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.statistics.experimentalequipmentdata.wettedwallcolumndata")``.

    WettedWallColumnData: typing.Type[WettedWallColumnData]
