
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.liquidphysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.system
import typing



class Costald(jneqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Costald': ...

class Density(jneqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...

class Water(jneqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    @staticmethod
    def calculatePureWaterDensity(double: float, double2: float) -> float: ...
    def clone(self) -> 'Water': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.liquidphysicalproperties.density")``.

    Costald: typing.Type[Costald]
    Density: typing.Type[Density]
    Water: typing.Type[Water]
