import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.nio.file
import java.util
import jpype
import jpype.protocol
import jneqsim.process.equipment.pipeline
import typing

class TwoFluidBenchmarkHarness:
    @staticmethod
    def capture(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> "TwoFluidBenchmarkHarness.Snapshot": ...
    @typing.overload
    @staticmethod
    def compare(
        list: java.util.List["TwoFluidBenchmarkHarness.Snapshot"],
        list2: java.util.List["TwoFluidBenchmarkHarness.BenchmarkPoint"],
    ) -> "TwoFluidBenchmarkHarness.Comparison": ...
    @typing.overload
    @staticmethod
    def compare(
        snapshot: "TwoFluidBenchmarkHarness.Snapshot",
        list: java.util.List["TwoFluidBenchmarkHarness.BenchmarkPoint"],
    ) -> "TwoFluidBenchmarkHarness.Comparison": ...
    @staticmethod
    def readCsv(
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> java.util.List["TwoFluidBenchmarkHarness.BenchmarkPoint"]: ...

    class BenchmarkPoint:
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            double: float,
            double2: float,
            string2: typing.Union[java.lang.String, str],
            double3: float,
            double4: float,
            double5: float,
            string3: typing.Union[java.lang.String, str],
        ): ...
        def getAbsoluteTolerance(self) -> float: ...
        def getCaseName(self) -> java.lang.String: ...
        def getPositionMeters(self) -> float: ...
        def getRelativeTolerance(self) -> float: ...
        def getSource(self) -> java.lang.String: ...
        def getTimeSeconds(self) -> float: ...
        def getValue(self) -> float: ...
        def getVariable(self) -> java.lang.String: ...

    class Comparison:
        def failureSummary(self) -> java.lang.String: ...
        def getFailureCount(self) -> int: ...
        def getMaximumRelativeError(self) -> float: ...
        def getRows(
            self,
        ) -> java.util.List["TwoFluidBenchmarkHarness.ComparisonRow"]: ...
        def isPassed(self) -> bool: ...

    class ComparisonRow:
        def getAbsoluteError(self) -> float: ...
        def getModelValue(self) -> float: ...
        def getReference(self) -> "TwoFluidBenchmarkHarness.BenchmarkPoint": ...
        def getRelativeError(self) -> float: ...
        def isPassed(self) -> bool: ...

    class Snapshot:
        def __init__(
            self,
            double: float,
            doubleArray: typing.Union[typing.List[float], jpype.JArray],
            map: typing.Union[
                java.util.Map[
                    typing.Union[java.lang.String, str],
                    typing.Union[typing.List[float], jpype.JArray],
                ],
                typing.Mapping[
                    typing.Union[java.lang.String, str],
                    typing.Union[typing.List[float], jpype.JArray],
                ],
            ],
        ): ...
        def getAvailableVariables(self) -> java.util.Set[java.lang.String]: ...
        def getTimeSeconds(self) -> float: ...
        def valueAt(
            self, string: typing.Union[java.lang.String, str], double: float
        ) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.pipeline.twophasepipe.validation")``.

    TwoFluidBenchmarkHarness: typing.Type[TwoFluidBenchmarkHarness]
