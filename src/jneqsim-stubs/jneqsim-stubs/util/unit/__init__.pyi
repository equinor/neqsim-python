import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.thermo
import typing

class NeqSimUnitSet:
    def __init__(self): ...
    def getComponentConcentrationUnit(self) -> java.lang.String: ...
    def getFlowRateUnit(self) -> java.lang.String: ...
    def getPressureUnit(self) -> java.lang.String: ...
    def getTemperatureUnit(self) -> java.lang.String: ...
    def setComponentConcentrationUnit(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...
    def setFlowRateUnit(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @staticmethod
    def setNeqSimUnits(string: typing.Union[java.lang.String, str]) -> None: ...
    def setPressureUnit(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setTemperatureUnit(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...

class Unit:
    def getSIvalue(self) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class Units:
    activeUnits: typing.ClassVar[java.util.HashMap] = ...
    defaultUnits: typing.ClassVar[java.util.HashMap] = ...
    metricUnits: typing.ClassVar[java.util.HashMap] = ...
    def __init__(self): ...
    @staticmethod
    def activateDefaultUnits() -> None: ...
    @staticmethod
    def activateFieldUnits() -> None: ...
    @staticmethod
    def activateMetricUnits() -> None: ...
    @staticmethod
    def activateSIUnits() -> None: ...
    def getMolarVolumeUnits(self) -> typing.MutableSequence[java.lang.String]: ...
    def getPressureUnits(self) -> typing.MutableSequence[java.lang.String]: ...
    @staticmethod
    def getSymbol(string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    @staticmethod
    def getSymbolName(
        string: typing.Union[java.lang.String, str]
    ) -> java.lang.String: ...
    def getTemperatureUnits(self) -> typing.MutableSequence[java.lang.String]: ...
    @staticmethod
    def setUnit(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> None: ...

    class UnitDescription:
        symbol: java.lang.String = ...
        symbolName: java.lang.String = ...
        def __init__(
            self,
            units: "Units",
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
        ): ...

class BaseUnit(Unit, jneqsim.thermo.ThermodynamicConstantsInterface):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...
    def getSIvalue(self) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class EnergyUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...
    def getConversionFactor(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class LengthUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...

class PowerUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...
    def getConversionFactor(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class PressureUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...
    def getConversionFactor(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class RateUnit(BaseUnit):
    def __init__(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        double2: float,
        double3: float,
        double4: float,
    ): ...
    def getConversionFactor(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    def getSIvalue(self) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class TemperatureUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...
    def getConversionFactor(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @typing.overload
    def getValue(
        self,
        double: float,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...

class TimeUnit(BaseUnit):
    def __init__(self, double: float, string: typing.Union[java.lang.String, str]): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.util.unit")``.

    BaseUnit: typing.Type[BaseUnit]
    EnergyUnit: typing.Type[EnergyUnit]
    LengthUnit: typing.Type[LengthUnit]
    NeqSimUnitSet: typing.Type[NeqSimUnitSet]
    PowerUnit: typing.Type[PowerUnit]
    PressureUnit: typing.Type[PressureUnit]
    RateUnit: typing.Type[RateUnit]
    TemperatureUnit: typing.Type[TemperatureUnit]
    TimeUnit: typing.Type[TimeUnit]
    Unit: typing.Type[Unit]
    Units: typing.Type[Units]
