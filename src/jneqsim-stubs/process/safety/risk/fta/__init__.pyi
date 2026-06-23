import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import typing

class FaultTreeAnalyzer(java.io.Serializable):
    def __init__(self): ...
    def minimalCutSets(
        self, faultTreeNode: "FaultTreeNode", int: int
    ) -> java.util.Set[java.util.List[java.lang.String]]: ...
    def topEventProbability(self, faultTreeNode: "FaultTreeNode") -> float: ...

    class GateType(java.lang.Enum["FaultTreeAnalyzer.GateType"]):
        AND: typing.ClassVar["FaultTreeAnalyzer.GateType"] = ...
        OR: typing.ClassVar["FaultTreeAnalyzer.GateType"] = ...
        VOTING: typing.ClassVar["FaultTreeAnalyzer.GateType"] = ...
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
            string: typing.Union[java.lang.String, str],
        ) -> "FaultTreeAnalyzer.GateType": ...
        @staticmethod
        def values() -> typing.MutableSequence["FaultTreeAnalyzer.GateType"]: ...

class FaultTreeNode(java.io.Serializable):
    name: java.lang.String = ...
    gate: FaultTreeAnalyzer.GateType = ...
    basicProbability: float = ...
    children: java.util.List = ...
    kOfN: int = ...
    betaCCF: float = ...
    @staticmethod
    def and_(
        string: typing.Union[java.lang.String, str], *faultTreeNode: "FaultTreeNode"
    ) -> "FaultTreeNode": ...
    @staticmethod
    def basic(
        string: typing.Union[java.lang.String, str], double: float
    ) -> "FaultTreeNode": ...
    def isBasic(self) -> bool: ...
    @staticmethod
    def or_(
        string: typing.Union[java.lang.String, str], *faultTreeNode: "FaultTreeNode"
    ) -> "FaultTreeNode": ...
    @staticmethod
    def voting(
        string: typing.Union[java.lang.String, str],
        int: int,
        *faultTreeNode: "FaultTreeNode",
    ) -> "FaultTreeNode": ...
    def withCCF(self, double: float) -> "FaultTreeNode": ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.risk.fta")``.

    FaultTreeAnalyzer: typing.Type[FaultTreeAnalyzer]
    FaultTreeNode: typing.Type[FaultTreeNode]
