
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.equipment
import jneqsim.process.instrumentdesign
import typing



class CompressorInstrumentDesign(jneqsim.process.instrumentdesign.InstrumentDesign):
    def __init__(self, processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def getNumberOfBearings(self) -> int: ...
    def isIncludeAntiSurge(self) -> bool: ...
    def setIncludeAntiSurge(self, boolean: bool) -> None: ...
    def setNumberOfBearings(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.instrumentdesign.compressor")``.

    CompressorInstrumentDesign: typing.Type[CompressorInstrumentDesign]
