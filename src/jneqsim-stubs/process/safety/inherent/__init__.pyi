import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import typing

class InherentSafetyEvaluator(java.io.Serializable):
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    def getScore(self, pillar: "InherentSafetyEvaluator.Pillar") -> float: ...
    def overallIndex(self) -> float: ...
    def report(self) -> java.lang.String: ...
    def score(
        self,
        pillar: "InherentSafetyEvaluator.Pillar",
        double: float,
        string: typing.Union[java.lang.String, str],
    ) -> "InherentSafetyEvaluator": ...

    class Pillar(java.lang.Enum["InherentSafetyEvaluator.Pillar"]):
        SUBSTITUTE: typing.ClassVar["InherentSafetyEvaluator.Pillar"] = ...
        MINIMIZE: typing.ClassVar["InherentSafetyEvaluator.Pillar"] = ...
        MODERATE: typing.ClassVar["InherentSafetyEvaluator.Pillar"] = ...
        SIMPLIFY: typing.ClassVar["InherentSafetyEvaluator.Pillar"] = ...
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
        ) -> "InherentSafetyEvaluator.Pillar": ...
        @staticmethod
        def values() -> typing.MutableSequence["InherentSafetyEvaluator.Pillar"]: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.inherent")``.

    InherentSafetyEvaluator: typing.Type[InherentSafetyEvaluator]
