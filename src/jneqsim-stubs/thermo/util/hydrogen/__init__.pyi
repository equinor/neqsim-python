import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import typing

class ParaOrthoH2Correction(java.io.Serializable):
    @staticmethod
    def estimateEquilibrationTimeSeconds(
        double: float, conversionCatalyst: "ParaOrthoH2Correction.ConversionCatalyst"
    ) -> float: ...
    @staticmethod
    def getConversionHeatJPerKg(
        double: float, double2: float, double3: float
    ) -> float: ...
    @staticmethod
    def getCpCorrectionJPerKgK(double: float) -> float: ...
    @staticmethod
    def getEquilibriumOrthoFraction(double: float) -> float: ...
    @staticmethod
    def getEquilibriumParaFraction(double: float) -> float: ...
    @staticmethod
    def getEquilibriumRotationalCpJPerKgK(double: float) -> float: ...
    @staticmethod
    def getFrozenNormalRotationalCpJPerKgK(double: float) -> float: ...
    @staticmethod
    def getNormalParaFraction() -> float: ...
    @staticmethod
    def getNormalToEquilibriumHeatJPerKg(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def getThermalConductivityCorrectionFactor(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def getThermalConductivityCorrectionFactor(
        double: float, double2: float
    ) -> float: ...

    class ConversionCatalyst(
        java.lang.Enum["ParaOrthoH2Correction.ConversionCatalyst"]
    ):
        NONE: typing.ClassVar["ParaOrthoH2Correction.ConversionCatalyst"] = ...
        ACTIVATED_CHARCOAL: typing.ClassVar[
            "ParaOrthoH2Correction.ConversionCatalyst"
        ] = ...
        HYDROUS_FERRIC_OXIDE: typing.ClassVar[
            "ParaOrthoH2Correction.ConversionCatalyst"
        ] = ...
        PARAMAGNETIC_OXIDE: typing.ClassVar[
            "ParaOrthoH2Correction.ConversionCatalyst"
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
            string: typing.Union[java.lang.String, str],
        ) -> "ParaOrthoH2Correction.ConversionCatalyst": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["ParaOrthoH2Correction.ConversionCatalyst"]
        ): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.hydrogen")``.

    ParaOrthoH2Correction: typing.Type[ParaOrthoH2Correction]
