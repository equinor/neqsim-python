import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.standards
import jneqsim.thermo.system
import typing

class Standard_ASTM_D6377(jneqsim.standards.Standard):
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def calculate(self) -> None: ...
    def getMethodRVP(self) -> java.lang.String: ...
    def getUnit(
        self, string: typing.Union[java.lang.String, str]
    ) -> java.lang.String: ...
    @typing.overload
    def getValue(self, string: typing.Union[java.lang.String, str]) -> float: ...
    @typing.overload
    def getValue(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> float: ...
    def isOnSpec(self) -> bool: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def setMethodRVP(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setReferenceTemperature(
        self, double: float, string: typing.Union[java.lang.String, str]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.standards.oilquality")``.

    Standard_ASTM_D6377: typing.Type[Standard_ASTM_D6377]
