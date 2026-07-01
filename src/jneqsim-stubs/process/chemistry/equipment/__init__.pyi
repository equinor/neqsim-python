import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.process.chemistry
import jneqsim.process.equipment
import jneqsim.process.equipment.stream
import typing

class InhibitorInjectionPoint(jneqsim.process.equipment.TwoPortEquipment):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ): ...
    def getActiveIngredientPpmInWater(self) -> float: ...
    def getChemical(self) -> jneqsim.process.chemistry.ProductionChemical: ...
    def getInjectionRateKgPerHour(self) -> float: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    def setChemical(
        self, productionChemical: jneqsim.process.chemistry.ProductionChemical
    ) -> None: ...
    def setDoseInKgPerHour(self, double: float) -> None: ...
    def setDoseInPpmOnWater(self, double: float) -> None: ...
    def setDoseMode(self, doseMode: "InhibitorInjectionPoint.DoseMode") -> None: ...
    def setDoseValue(self, double: float) -> None: ...

    class DoseMode(java.lang.Enum["InhibitorInjectionPoint.DoseMode"]):
        PPM: typing.ClassVar["InhibitorInjectionPoint.DoseMode"] = ...
        PPM_TOTAL: typing.ClassVar["InhibitorInjectionPoint.DoseMode"] = ...
        KG_PER_HOUR: typing.ClassVar["InhibitorInjectionPoint.DoseMode"] = ...
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
        ) -> "InhibitorInjectionPoint.DoseMode": ...
        @staticmethod
        def values() -> typing.MutableSequence["InhibitorInjectionPoint.DoseMode"]: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.chemistry.equipment")``.

    InhibitorInjectionPoint: typing.Type[InhibitorInjectionPoint]
