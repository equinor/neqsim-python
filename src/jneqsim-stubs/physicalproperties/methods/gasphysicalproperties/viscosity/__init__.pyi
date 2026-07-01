import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.gasphysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.system
import typing

class Viscosity(
    jneqsim.physicalproperties.methods.gasphysicalproperties.GasPhysicalPropertyMethod,
    jneqsim.physicalproperties.methods.methodinterface.ViscosityInterface,
):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def clone(self) -> "Viscosity": ...

class ChungViscosityMethod(Viscosity):
    pureComponentViscosity: typing.MutableSequence[float] = ...
    relativeViscosity: typing.MutableSequence[float] = ...
    Fc: typing.MutableSequence[float] = ...
    omegaVisc: typing.MutableSequence[float] = ...
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def calcViscosity(self) -> float: ...
    def getPureComponentViscosity(self, int: int) -> float: ...
    def initChungPureComponentViscosity(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.gasphysicalproperties.viscosity")``.

    ChungViscosityMethod: typing.Type[ChungViscosityMethod]
    Viscosity: typing.Type[Viscosity]
