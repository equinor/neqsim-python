import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jneqsim.process.equipment.pipeline
import jneqsim.process.equipment.stream
import jneqsim.process.processmodel
import typing

class MassBalanceLeakDetector(java.io.Serializable):
    @typing.overload
    def __init__(
        self,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        streamInterface2: jneqsim.process.equipment.stream.StreamInterface,
    ): ...
    @typing.overload
    def __init__(self, processSystem: jneqsim.process.processmodel.ProcessSystem): ...
    def calculateSensitivity(
        self,
    ) -> "MassBalanceLeakDetector.LeakDetectionSensitivityResult": ...
    @staticmethod
    def fromPipe(
        pipeLineInterface: jneqsim.process.equipment.pipeline.PipeLineInterface,
    ) -> "MassBalanceLeakDetector": ...
    def setConfidenceMultiplier(self, double: float) -> "MassBalanceLeakDetector": ...
    def setDetectionWindowS(self, double: float) -> "MassBalanceLeakDetector": ...
    def setFlowMeasurementUncertaintyFraction(
        self, double: float
    ) -> "MassBalanceLeakDetector": ...
    def setLinepackVolumeM3(self, double: float) -> "MassBalanceLeakDetector": ...
    def setPressureUncertaintyBara(
        self, double: float
    ) -> "MassBalanceLeakDetector": ...
    def setTemperatureUncertaintyK(
        self, double: float
    ) -> "MassBalanceLeakDetector": ...

    class LeakDetectionSensitivityResult(java.io.Serializable):
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
            double: float,
            double2: float,
            double3: float,
            double4: float,
            double5: float,
            double6: float,
            double7: float,
            double8: float,
            double9: float,
            double10: float,
        ): ...
        def getMinimumDetectableLeakFraction(self) -> float: ...
        def getMinimumDetectableLeakRateKgPerS(self) -> float: ...
        def toJson(self) -> java.lang.String: ...
        def toMap(self) -> java.util.Map[java.lang.String, typing.Any]: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.leakdetection")``.

    MassBalanceLeakDetector: typing.Type[MassBalanceLeakDetector]
