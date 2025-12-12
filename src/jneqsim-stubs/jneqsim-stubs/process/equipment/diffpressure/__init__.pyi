import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jpype
import jneqsim.process.equipment
import typing

class DifferentialPressureFlowCalculator:
    @typing.overload
    @staticmethod
    def calculate(
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        doubleArray3: typing.Union[typing.List[float], jpype.JArray],
        string: typing.Union[java.lang.String, str],
    ) -> "DifferentialPressureFlowCalculator.FlowCalculationResult": ...
    @typing.overload
    @staticmethod
    def calculate(
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        doubleArray3: typing.Union[typing.List[float], jpype.JArray],
        string: typing.Union[java.lang.String, str],
        doubleArray4: typing.Union[typing.List[float], jpype.JArray],
    ) -> "DifferentialPressureFlowCalculator.FlowCalculationResult": ...
    @typing.overload
    @staticmethod
    def calculate(
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        doubleArray3: typing.Union[typing.List[float], jpype.JArray],
        string: typing.Union[java.lang.String, str],
        doubleArray4: typing.Union[typing.List[float], jpype.JArray],
        list: java.util.List[typing.Union[java.lang.String, str]],
        doubleArray5: typing.Union[typing.List[float], jpype.JArray],
        boolean: bool,
    ) -> "DifferentialPressureFlowCalculator.FlowCalculationResult": ...

    class FlowCalculationResult:
        def getMassFlowKgPerHour(self) -> typing.MutableSequence[float]: ...
        def getMolecularWeightGPerMol(self) -> typing.MutableSequence[float]: ...
        def getStandardFlowMSm3PerDay(self) -> typing.MutableSequence[float]: ...
        def getVolumetricFlowM3PerHour(self) -> typing.MutableSequence[float]: ...

class Orifice(jneqsim.process.equipment.TwoPortEquipment):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
    ): ...
    def calc_dp(self) -> float: ...
    @staticmethod
    def calculateBetaRatio(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateDischargeCoefficient(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        string: typing.Union[java.lang.String, str],
    ) -> float: ...
    @staticmethod
    def calculateExpansibility(
        double: float, double2: float, double3: float, double4: float, double5: float
    ) -> float: ...
    @staticmethod
    def calculateMassFlowRate(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        string: typing.Union[java.lang.String, str],
    ) -> float: ...
    @staticmethod
    def calculatePressureDrop(
        double: float, double2: float, double3: float, double4: float, double5: float
    ) -> float: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    @typing.overload
    def runTransient(self, double: float) -> None: ...
    @typing.overload
    def runTransient(self, double: float, uUID: java.util.UUID) -> None: ...
    def setOrificeParameters(
        self, double: float, double2: float, double3: float
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.diffpressure")``.

    DifferentialPressureFlowCalculator: typing.Type[DifferentialPressureFlowCalculator]
    Orifice: typing.Type[Orifice]
