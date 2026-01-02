
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.equipment
import jneqsim.process.mechanicaldesign
import jneqsim.process.mechanicaldesign.separator.sectiontype
import typing



class SeparatorMechanicalDesign(jneqsim.process.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def displayResults(self) -> None: ...
    def readDesignSpecifications(self) -> None: ...
    def setDesign(self) -> None: ...

class GasScrubberMechanicalDesign(SeparatorMechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def readDesignSpecifications(self) -> None: ...
    def setDesign(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.mechanicaldesign.separator")``.

    GasScrubberMechanicalDesign: typing.Type[GasScrubberMechanicalDesign]
    SeparatorMechanicalDesign: typing.Type[SeparatorMechanicalDesign]
    sectiontype: jneqsim.process.mechanicaldesign.separator.sectiontype.__module_protocol__
