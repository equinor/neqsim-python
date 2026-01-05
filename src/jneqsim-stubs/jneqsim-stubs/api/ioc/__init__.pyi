import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import typing

class CalculationResult:
    fluidProperties: typing.MutableSequence[typing.MutableSequence[float]] = ...
    calculationError: typing.MutableSequence[java.lang.String] = ...
    def __init__(
        self,
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ): ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.api.ioc")``.

    CalculationResult: typing.Type[CalculationResult]
