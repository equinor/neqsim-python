
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.electricaldesign
import jneqsim.process.equipment
import typing



class PumpElectricalDesign(jneqsim.process.electricaldesign.ElectricalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface): ...
    def readDesignSpecifications(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.electricaldesign.pump")``.

    PumpElectricalDesign: typing.Type[PumpElectricalDesign]
