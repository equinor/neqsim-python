
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.blackoil
import typing



class BlackOilSeparator:
    def __init__(self, string: typing.Union[java.lang.String, str], systemBlackOil: jneqsim.blackoil.SystemBlackOil, double: float, double2: float): ...
    def getGasOut(self) -> jneqsim.blackoil.SystemBlackOil: ...
    def getInlet(self) -> jneqsim.blackoil.SystemBlackOil: ...
    def getName(self) -> java.lang.String: ...
    def getOilOut(self) -> jneqsim.blackoil.SystemBlackOil: ...
    def getWaterOut(self) -> jneqsim.blackoil.SystemBlackOil: ...
    def run(self) -> None: ...
    def setInlet(self, systemBlackOil: jneqsim.blackoil.SystemBlackOil) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.blackoil")``.

    BlackOilSeparator: typing.Type[BlackOilSeparator]
