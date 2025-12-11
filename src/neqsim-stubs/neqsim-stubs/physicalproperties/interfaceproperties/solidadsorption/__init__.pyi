
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.thermo
import neqsim.thermo.system
import typing



class AdsorptionInterface(neqsim.thermo.ThermodynamicConstantsInterface):
    def calcAdsorption(self, int: int) -> None: ...
    @typing.overload
    def getSurfaceExcess(self, int: int) -> float: ...
    @typing.overload
    def getSurfaceExcess(self, string: typing.Union[java.lang.String, str]) -> float: ...
    def setSolidMaterial(self, string: typing.Union[java.lang.String, str]) -> None: ...

class PotentialTheoryAdsorption(AdsorptionInterface):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface): ...
    def calcAdsorption(self, int: int) -> None: ...
    @typing.overload
    def getSurfaceExcess(self, int: int) -> float: ...
    @typing.overload
    def getSurfaceExcess(self, string: typing.Union[java.lang.String, str]) -> float: ...
    def readDBParameters(self) -> None: ...
    def setSolidMaterial(self, string: typing.Union[java.lang.String, str]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.interfaceproperties.solidadsorption")``.

    AdsorptionInterface: typing.Type[AdsorptionInterface]
    PotentialTheoryAdsorption: typing.Type[PotentialTheoryAdsorption]
