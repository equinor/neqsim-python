
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.equipment
import jneqsim.process.mechanicaldesign
import typing



class WellFlowMechanicalDesign(jneqsim.process.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def getWellCapexUsd(self) -> float: ...
    def setWellCapexUsd(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.mechanicaldesign.well")``.

    WellFlowMechanicalDesign: typing.Type[WellFlowMechanicalDesign]
