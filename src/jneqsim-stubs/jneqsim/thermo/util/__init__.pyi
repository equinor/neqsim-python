
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.thermo.system
import jneqsim.thermo.util.Vega
import jneqsim.thermo.util.benchmark
import jneqsim.thermo.util.constants
import jneqsim.thermo.util.derivatives
import jneqsim.thermo.util.empiric
import jneqsim.thermo.util.gerg
import jneqsim.thermo.util.humidair
import jneqsim.thermo.util.jni
import jneqsim.thermo.util.leachman
import jneqsim.thermo.util.readwrite
import jneqsim.thermo.util.referenceequations
import jneqsim.thermo.util.spanwagner
import jneqsim.thermo.util.steam
import typing



class FluidClassifier:
    @staticmethod
    def calculateC7PlusContent(systemInterface: jneqsim.thermo.system.SystemInterface) -> float: ...
    @staticmethod
    def classify(systemInterface: jneqsim.thermo.system.SystemInterface) -> 'ReservoirFluidType': ...
    @staticmethod
    def classifyByC7Plus(double: float) -> 'ReservoirFluidType': ...
    @staticmethod
    def classifyByGOR(double: float) -> 'ReservoirFluidType': ...
    @staticmethod
    def classifyWithPhaseEnvelope(systemInterface: jneqsim.thermo.system.SystemInterface, double: float) -> 'ReservoirFluidType': ...
    @staticmethod
    def estimateAPIGravity(systemInterface: jneqsim.thermo.system.SystemInterface) -> float: ...
    @staticmethod
    def generateClassificationReport(systemInterface: jneqsim.thermo.system.SystemInterface) -> java.lang.String: ...

class ReservoirFluidType(java.lang.Enum['ReservoirFluidType']):
    DRY_GAS: typing.ClassVar['ReservoirFluidType'] = ...
    WET_GAS: typing.ClassVar['ReservoirFluidType'] = ...
    GAS_CONDENSATE: typing.ClassVar['ReservoirFluidType'] = ...
    VOLATILE_OIL: typing.ClassVar['ReservoirFluidType'] = ...
    BLACK_OIL: typing.ClassVar['ReservoirFluidType'] = ...
    HEAVY_OIL: typing.ClassVar['ReservoirFluidType'] = ...
    UNKNOWN: typing.ClassVar['ReservoirFluidType'] = ...
    def getDisplayName(self) -> java.lang.String: ...
    def getTypicalC7PlusRange(self) -> java.lang.String: ...
    def getTypicalGORRange(self) -> java.lang.String: ...
    def toString(self) -> java.lang.String: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: typing.Union[java.lang.String, str]) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: typing.Union[java.lang.String, str]) -> 'ReservoirFluidType': ...
    @staticmethod
    def values() -> typing.MutableSequence['ReservoirFluidType']: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util")``.

    FluidClassifier: typing.Type[FluidClassifier]
    ReservoirFluidType: typing.Type[ReservoirFluidType]
    Vega: jneqsim.thermo.util.Vega.__module_protocol__
    benchmark: jneqsim.thermo.util.benchmark.__module_protocol__
    constants: jneqsim.thermo.util.constants.__module_protocol__
    derivatives: jneqsim.thermo.util.derivatives.__module_protocol__
    empiric: jneqsim.thermo.util.empiric.__module_protocol__
    gerg: jneqsim.thermo.util.gerg.__module_protocol__
    humidair: jneqsim.thermo.util.humidair.__module_protocol__
    jni: jneqsim.thermo.util.jni.__module_protocol__
    leachman: jneqsim.thermo.util.leachman.__module_protocol__
    readwrite: jneqsim.thermo.util.readwrite.__module_protocol__
    referenceequations: jneqsim.thermo.util.referenceequations.__module_protocol__
    spanwagner: jneqsim.thermo.util.spanwagner.__module_protocol__
    steam: jneqsim.thermo.util.steam.__module_protocol__
