import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.equipment
import jneqsim.process.instrumentdesign
import typing

class PipelineInstrumentDesign(jneqsim.process.instrumentdesign.InstrumentDesign):
    def __init__(
        self,
        processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface,
    ): ...
    def calcDesign(self) -> None: ...
    def isIncludeLeakDetection(self) -> bool: ...
    def isIncludePigDetection(self) -> bool: ...
    def setIncludeLeakDetection(self, boolean: bool) -> None: ...
    def setIncludePigDetection(self, boolean: bool) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.instrumentdesign.pipeline")``.

    PipelineInstrumentDesign: typing.Type[PipelineInstrumentDesign]
