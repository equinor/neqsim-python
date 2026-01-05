import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.statistics.parameterfitting.nonlinearparameterfitting
import typing

class TestViscosityFit:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ViscosityFunction(
    jneqsim.statistics.parameterfitting.nonlinearparameterfitting.LevenbergMarquardtFunction
):
    def __init__(self): ...
    def calcValue(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    @typing.overload
    def setFittingParams(self, int: int, double: float) -> None: ...
    @typing.overload
    def setFittingParams(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.linearliquidmodel")``.

    TestViscosityFit: typing.Type[TestViscosityFit]
    ViscosityFunction: typing.Type[ViscosityFunction]
