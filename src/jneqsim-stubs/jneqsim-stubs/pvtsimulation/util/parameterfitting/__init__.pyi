import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.statistics.parameterfitting.nonlinearparameterfitting
import jneqsim.thermo.system
import typing

class CMEFunction(
    jneqsim.statistics.parameterfitting.nonlinearparameterfitting.LevenbergMarquardtFunction
):
    def __init__(self): ...
    def calcSaturationConditions(
        self, systemInterface: jneqsim.thermo.system.SystemInterface
    ) -> None: ...
    def calcValue(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    @typing.overload
    def setFittingParams(self, int: int, double: float) -> None: ...
    @typing.overload
    def setFittingParams(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...

class CVDFunction(
    jneqsim.statistics.parameterfitting.nonlinearparameterfitting.LevenbergMarquardtFunction
):
    def __init__(self): ...
    def calcSaturationConditions(
        self, systemInterface: jneqsim.thermo.system.SystemInterface
    ) -> None: ...
    def calcValue(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    @typing.overload
    def setFittingParams(self, int: int, double: float) -> None: ...
    @typing.overload
    def setFittingParams(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...

class DensityFunction(
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

class FunctionJohanSverderup(
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

class SaturationPressureFunction(
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

class TestFitToOilFieldFluid:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class TestSaturationPresFunction:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class TestWaxTuning:
    def __init__(self): ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class ViscosityFunction(
    jneqsim.statistics.parameterfitting.nonlinearparameterfitting.LevenbergMarquardtFunction
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    def calcValue(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    @typing.overload
    def setFittingParams(self, int: int, double: float) -> None: ...
    @typing.overload
    def setFittingParams(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...

class WaxFunction(
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
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.pvtsimulation.util.parameterfitting")``.

    CMEFunction: typing.Type[CMEFunction]
    CVDFunction: typing.Type[CVDFunction]
    DensityFunction: typing.Type[DensityFunction]
    FunctionJohanSverderup: typing.Type[FunctionJohanSverderup]
    SaturationPressureFunction: typing.Type[SaturationPressureFunction]
    TestFitToOilFieldFluid: typing.Type[TestFitToOilFieldFluid]
    TestSaturationPresFunction: typing.Type[TestSaturationPresFunction]
    TestWaxTuning: typing.Type[TestWaxTuning]
    ViscosityFunction: typing.Type[ViscosityFunction]
    WaxFunction: typing.Type[WaxFunction]
