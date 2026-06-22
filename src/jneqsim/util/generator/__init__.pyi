
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jpype
import jneqsim.thermo.system
import typing



class PropertyGenerator:
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def calculate(self) -> java.util.HashMap[java.lang.String, typing.MutableSequence[float]]: ...
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.util.generator")``.

    PropertyGenerator: typing.Type[PropertyGenerator]
