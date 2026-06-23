import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import typing

class EventTreeAnalyzer(java.io.Serializable):
    def __init__(self, string: typing.Union[java.lang.String, str], double: float): ...
    def addBranch(
        self, string: typing.Union[java.lang.String, str], double: float
    ) -> "EventTreeAnalyzer": ...
    def evaluate(self) -> java.util.List["EventTreeAnalyzer.Outcome"]: ...
    def report(self) -> java.lang.String: ...

    class Outcome(java.io.Serializable):
        path: java.lang.String = ...
        probability: float = ...
        frequencyPerYear: float = ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.risk.eta")``.

    EventTreeAnalyzer: typing.Type[EventTreeAnalyzer]
