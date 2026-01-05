import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.process.equipment
import jneqsim.process.equipment.stream
import typing

class CO2Electrolyzer(jneqsim.process.equipment.ProcessEquipmentBaseClass):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ): ...
    def getGasProductStream(
        self,
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    def getLiquidProductStream(
        self,
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    @typing.overload
    def getMassBalance(self) -> float: ...
    @typing.overload
    def getMassBalance(self, string: typing.Union[java.lang.String, str]) -> float: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    def setCO2Conversion(self, double: float) -> None: ...
    def setCellVoltage(self, double: float) -> None: ...
    def setCo2ComponentName(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...
    def setCurrentEfficiency(self, double: float) -> None: ...
    def setElectronsPerMoleProduct(
        self, string: typing.Union[java.lang.String, str], double: float
    ) -> None: ...
    def setGasProductSelectivity(
        self, string: typing.Union[java.lang.String, str], double: float
    ) -> None: ...
    def setInletStream(
        self, streamInterface: jneqsim.process.equipment.stream.StreamInterface
    ) -> None: ...
    def setLiquidProductSelectivity(
        self, string: typing.Union[java.lang.String, str], double: float
    ) -> None: ...
    def setProductFaradaicEfficiency(
        self, string: typing.Union[java.lang.String, str], double: float
    ) -> None: ...
    def setUseSelectivityModel(self, boolean: bool) -> None: ...

class Electrolyzer(jneqsim.process.equipment.ProcessEquipmentBaseClass):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ): ...
    def getHydrogenOutStream(
        self,
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    @typing.overload
    def getMassBalance(self) -> float: ...
    @typing.overload
    def getMassBalance(self, string: typing.Union[java.lang.String, str]) -> float: ...
    def getOxygenOutStream(
        self,
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    def setInletStream(
        self, streamInterface: jneqsim.process.equipment.stream.StreamInterface
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.electrolyzer")``.

    CO2Electrolyzer: typing.Type[CO2Electrolyzer]
    Electrolyzer: typing.Type[Electrolyzer]
