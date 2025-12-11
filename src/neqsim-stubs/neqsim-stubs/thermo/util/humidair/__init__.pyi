
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing



class HumidAir:
    @staticmethod
    def cairSat(double: float) -> float: ...
    @staticmethod
    def dewPointTemperature(double: float, double2: float) -> float: ...
    @staticmethod
    def enthalpy(double: float, double2: float) -> float: ...
    @staticmethod
    def humidityRatioFromRH(double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def relativeHumidity(double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def saturationPressureWater(double: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.thermo.util.humidair")``.

    HumidAir: typing.Type[HumidAir]
