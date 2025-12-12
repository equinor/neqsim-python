import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.liquidphysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.system
import typing

class Viscosity(
    jneqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod,
    jneqsim.physicalproperties.methods.methodinterface.ViscosityInterface,
):
    pureComponentViscosity: typing.MutableSequence[float] = ...
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def calcPureComponentViscosity(self) -> None: ...
    def calcViscosity(self) -> float: ...
    def clone(self) -> "Viscosity": ...
    def getPureComponentViscosity(self, int: int) -> float: ...
    def getViscosityPressureCorrection(self, int: int) -> float: ...

class AmineViscosity(Viscosity):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def calcViscosity(self) -> float: ...

class Water(Viscosity):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def calcViscosity(self) -> float: ...
    def clone(self) -> "Water": ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.liquidphysicalproperties.viscosity")``.

    AmineViscosity: typing.Type[AmineViscosity]
    Viscosity: typing.Type[Viscosity]
    Water: typing.Type[Water]
