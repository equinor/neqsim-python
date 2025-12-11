
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.blackoil
import typing



class BlackOilSeparator:
    def __init__(self, string: typing.Union[java.lang.String, str], systemBlackOil: neqsim.blackoil.SystemBlackOil, double: float, double2: float): ...
    def getGasOut(self) -> neqsim.blackoil.SystemBlackOil: ...
    def getInlet(self) -> neqsim.blackoil.SystemBlackOil: ...
    def getName(self) -> java.lang.String: ...
    def getOilOut(self) -> neqsim.blackoil.SystemBlackOil: ...
    def getWaterOut(self) -> neqsim.blackoil.SystemBlackOil: ...
    def run(self) -> None: ...
    def setInlet(self, systemBlackOil: neqsim.blackoil.SystemBlackOil) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.equipment.blackoil")``.

    BlackOilSeparator: typing.Type[BlackOilSeparator]
