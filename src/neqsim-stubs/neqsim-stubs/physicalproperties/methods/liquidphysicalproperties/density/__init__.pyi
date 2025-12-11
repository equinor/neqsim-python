
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods.liquidphysicalproperties
import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.system
import typing



class Costald(neqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Costald': ...

class Density(neqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...

class Water(neqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    @staticmethod
    def calculatePureWaterDensity(double: float, double2: float) -> float: ...
    def clone(self) -> 'Water': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.liquidphysicalproperties.density")``.

    Costald: typing.Type[Costald]
    Density: typing.Type[Density]
    Water: typing.Type[Water]
