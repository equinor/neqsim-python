import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.thermo.system
import jneqsim.thermodynamicoperations
import org.jfree.chart
import typing

class PloadingCurve(jneqsim.thermodynamicoperations.OperationInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def addData(
        self,
        string: typing.Union[java.lang.String, str],
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
    ) -> None: ...
    def displayResult(self) -> None: ...
    def get(
        self, string: typing.Union[java.lang.String, str]
    ) -> typing.MutableSequence[float]: ...
    def getJFreeChart(
        self, string: typing.Union[java.lang.String, str]
    ) -> org.jfree.chart.JFreeChart: ...
    def getPoints(
        self, int: int
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getResultTable(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    def getThermoSystem(self) -> jneqsim.thermo.system.SystemInterface: ...
    def printToFile(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def run(self) -> None: ...

class PloadingCurve2(jneqsim.thermodynamicoperations.BaseOperation):
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def displayResult(self) -> None: ...
    def get(
        self, string: typing.Union[java.lang.String, str]
    ) -> typing.MutableSequence[float]: ...
    def getJFreeChart(
        self, string: typing.Union[java.lang.String, str]
    ) -> org.jfree.chart.JFreeChart: ...
    def getPoints(
        self, int: int
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getResultTable(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    def getThermoSystem(self) -> jneqsim.thermo.system.SystemInterface: ...
    def printToFile(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def run(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermodynamicoperations.phaseenvelopeops.reactivecurves")``.

    PloadingCurve: typing.Type[PloadingCurve]
    PloadingCurve2: typing.Type[PloadingCurve2]
