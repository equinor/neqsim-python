
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.process.equipment
import neqsim.process.mechanicaldesign
import typing



class AdsorberMechanicalDesign(neqsim.process.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: neqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def getOuterDiameter(self) -> float: ...
    def getWallThickness(self) -> float: ...
    def readDesignSpecifications(self) -> None: ...
    def setDesign(self) -> None: ...
    def setOuterDiameter(self, double: float) -> None: ...
    def setWallThickness(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.mechanicaldesign.adsorber")``.

    AdsorberMechanicalDesign: typing.Type[AdsorberMechanicalDesign]
