
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import typing



class BukacekWaterInGas:
    def __init__(self): ...
    @staticmethod
    def getWaterInGas(double: float, double2: float) -> float: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...
    @staticmethod
    def waterDewPointTemperature(double: float, double2: float) -> float: ...

class DuanSun:
    def __init__(self): ...
    def bublePointPressure(self, double: float, double2: float, double3: float) -> float: ...
    def calcCO2solubility(self, double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...

class Water:
    def __init__(self): ...
    def density(self) -> float: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...
    @staticmethod
    def waterDensity(double: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.empiric")``.

    BukacekWaterInGas: typing.Type[BukacekWaterInGas]
    DuanSun: typing.Type[DuanSun]
    Water: typing.Type[Water]
