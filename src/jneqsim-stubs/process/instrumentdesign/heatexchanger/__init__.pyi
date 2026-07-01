import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.process.equipment
import jneqsim.process.instrumentdesign
import typing

class HeatExchangerInstrumentDesign(jneqsim.process.instrumentdesign.InstrumentDesign):
    def __init__(
        self,
        processEquipmentInterface: jneqsim.process.equipment.ProcessEquipmentInterface,
    ): ...
    def calcDesign(self) -> None: ...
    def getHeatExchangerType(
        self,
    ) -> "HeatExchangerInstrumentDesign.HeatExchangerType": ...
    def setHeatExchangerType(
        self, heatExchangerType: "HeatExchangerInstrumentDesign.HeatExchangerType"
    ) -> None: ...

    class HeatExchangerType(
        java.lang.Enum["HeatExchangerInstrumentDesign.HeatExchangerType"]
    ):
        SHELL_AND_TUBE: typing.ClassVar[
            "HeatExchangerInstrumentDesign.HeatExchangerType"
        ] = ...
        AIR_COOLER: typing.ClassVar[
            "HeatExchangerInstrumentDesign.HeatExchangerType"
        ] = ...
        ELECTRIC_HEATER: typing.ClassVar[
            "HeatExchangerInstrumentDesign.HeatExchangerType"
        ] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str]
        ) -> "HeatExchangerInstrumentDesign.HeatExchangerType": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["HeatExchangerInstrumentDesign.HeatExchangerType"]
        ): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.instrumentdesign.heatexchanger")``.

    HeatExchangerInstrumentDesign: typing.Type[HeatExchangerInstrumentDesign]
