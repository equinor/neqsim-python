
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.methods.solidphysicalproperties
import neqsim.physicalproperties.system
import typing



class Viscosity(neqsim.physicalproperties.methods.solidphysicalproperties.SolidPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.ViscosityInterface):
    pureComponentViscosity: typing.MutableSequence[float] = ...
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcPureComponentViscosity(self) -> None: ...
    def calcViscosity(self) -> float: ...
    def clone(self) -> 'Viscosity': ...
    def getPureComponentViscosity(self, int: int) -> float: ...
    def getViscosityPressureCorrection(self, int: int) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.solidphysicalproperties.viscosity")``.

    Viscosity: typing.Type[Viscosity]
