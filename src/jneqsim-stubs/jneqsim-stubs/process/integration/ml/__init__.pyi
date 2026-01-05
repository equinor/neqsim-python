import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import jneqsim.process.equipment.stream
import typing

class FeatureExtractor:
    STANDARD_STREAM_FEATURES: typing.ClassVar[
        typing.MutableSequence[java.lang.String]
    ] = ...
    MINIMAL_STREAM_FEATURES: typing.ClassVar[
        typing.MutableSequence[java.lang.String]
    ] = ...
    @staticmethod
    def extractFeature(
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        string: typing.Union[java.lang.String, str],
    ) -> float: ...
    @staticmethod
    def extractFeatures(
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def extractMinimalFeatures(
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def extractStandardFeatures(
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def normalizeMinMax(
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        doubleArray3: typing.Union[typing.List[float], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def normalizeZScore(
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        doubleArray3: typing.Union[typing.List[float], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...

class MLCorrectionInterface:
    def correct(
        self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def correctBatch(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
    ) -> typing.MutableSequence[float]: ...
    def getConfidence(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def getFeatureCount(self) -> int: ...
    def getFeatureNames(self) -> typing.MutableSequence[java.lang.String]: ...
    def getModelVersion(self) -> java.lang.String: ...
    def getUncertainty(
        self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def isReady(self) -> bool: ...
    def onModelUpdate(
        self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]
    ) -> None: ...

class HybridModelAdapter(MLCorrectionInterface, java.io.Serializable):
    def __init__(
        self,
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
        combinationStrategy: "HybridModelAdapter.CombinationStrategy",
    ): ...
    @staticmethod
    def additive(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> "HybridModelAdapter": ...
    def correct(
        self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def getBias(self) -> float: ...
    def getConfidence(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def getFeatureCount(self) -> int: ...
    def getFeatureNames(self) -> typing.MutableSequence[java.lang.String]: ...
    def getModelVersion(self) -> java.lang.String: ...
    def getStrategy(self) -> "HybridModelAdapter.CombinationStrategy": ...
    def getUncertainty(
        self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> float: ...
    def getWeights(self) -> typing.MutableSequence[float]: ...
    def isReady(self) -> bool: ...
    @staticmethod
    def multiplicative(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> "HybridModelAdapter": ...
    def onModelUpdate(
        self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]
    ) -> None: ...
    def setConfidenceThreshold(self, double: float) -> None: ...
    def setLinearModel(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        double2: float,
    ) -> None: ...
    def setStrategy(
        self, combinationStrategy: "HybridModelAdapter.CombinationStrategy"
    ) -> None: ...
    def trainLinear(
        self,
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
    ) -> None: ...

    class CombinationStrategy(java.lang.Enum["HybridModelAdapter.CombinationStrategy"]):
        ADDITIVE: typing.ClassVar["HybridModelAdapter.CombinationStrategy"] = ...
        MULTIPLICATIVE: typing.ClassVar["HybridModelAdapter.CombinationStrategy"] = ...
        REPLACEMENT: typing.ClassVar["HybridModelAdapter.CombinationStrategy"] = ...
        WEIGHTED_AVERAGE: typing.ClassVar["HybridModelAdapter.CombinationStrategy"] = (
            ...
        )
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
            string: typing.Union[java.lang.String, str]
        ) -> "HybridModelAdapter.CombinationStrategy": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["HybridModelAdapter.CombinationStrategy"]
        ): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.integration.ml")``.

    FeatureExtractor: typing.Type[FeatureExtractor]
    HybridModelAdapter: typing.Type[HybridModelAdapter]
    MLCorrectionInterface: typing.Type[MLCorrectionInterface]
