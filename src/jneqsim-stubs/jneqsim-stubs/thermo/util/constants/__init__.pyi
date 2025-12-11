
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import typing



class FurstElectrolyteConstants(java.io.Serializable):
    furstParams: typing.ClassVar[typing.MutableSequence[float]] = ...
    furstParamsCPA: typing.ClassVar[typing.MutableSequence[float]] = ...
    furstParamsCPA_MDEA: typing.ClassVar[typing.MutableSequence[float]] = ...
    @staticmethod
    def getFurstParam(int: int) -> float: ...
    @staticmethod
    def getFurstParamMDEA(int: int) -> float: ...
    @staticmethod
    def setFurstParam(int: int, double: float) -> None: ...
    @staticmethod
    def setFurstParams(string: typing.Union[java.lang.String, str]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.constants")``.

    FurstElectrolyteConstants: typing.Type[FurstElectrolyteConstants]
