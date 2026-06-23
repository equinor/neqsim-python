import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.nio.file
import java.util
import jpype.protocol
import jneqsim.process.equipment.pipeline
import jneqsim.process.equipment.pipeline.twophasepipe.validation
import typing

class TwoFluidPipeReport:
    @staticmethod
    def capture(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> "TwoFluidPipeReport.ProfileSnapshot": ...
    @staticmethod
    def newSnapshotList() -> java.util.List["TwoFluidPipeReport.ProfileSnapshot"]: ...
    @staticmethod
    def toComparisonCsv(
        comparison: jneqsim.process.equipment.pipeline.twophasepipe.validation.TwoFluidBenchmarkHarness.Comparison,
    ) -> java.lang.String: ...
    @staticmethod
    def toSlugAndFlowAssuranceCsv(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> java.lang.String: ...
    @staticmethod
    def toSteadyStateProfileCsv(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> java.lang.String: ...
    @staticmethod
    def toSummaryJson(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> java.lang.String: ...
    @staticmethod
    def toSummaryText(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
    ) -> java.lang.String: ...
    @staticmethod
    def toTransientProfileCsv(
        list: java.util.List["TwoFluidPipeReport.ProfileSnapshot"],
    ) -> java.lang.String: ...
    @staticmethod
    def writeComparisonCsv(
        comparison: jneqsim.process.equipment.pipeline.twophasepipe.validation.TwoFluidBenchmarkHarness.Comparison,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @staticmethod
    def writeSlugAndFlowAssuranceCsv(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @staticmethod
    def writeSteadyStateProfileCsv(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @staticmethod
    def writeSummaryJson(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @staticmethod
    def writeSummaryText(
        twoFluidPipe: jneqsim.process.equipment.pipeline.TwoFluidPipe,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @staticmethod
    def writeTransientProfileCsv(
        list: java.util.List["TwoFluidPipeReport.ProfileSnapshot"],
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...

    class ProfileSnapshot:
        def getTimeSeconds(self) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.pipeline.twophasepipe.reporting")``.

    TwoFluidPipeReport: typing.Type[TwoFluidPipeReport]
