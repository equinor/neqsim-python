
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim
import neqsim.physicalproperties.system
import typing



class AmineDiffusivity(neqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity.SiddiqiLucasMethod):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcBinaryDiffusionCoefficient(self, int: int, int2: int, int3: int) -> float: ...
    def calcDiffusionCoefficients(self, int: int, int2: int) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def calcEffectiveDiffusionCoefficients(self) -> None: ...

class CO2water(neqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity.Diffusivity):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcBinaryDiffusionCoefficient(self, int: int, int2: int, int3: int) -> float: ...

class SiddiqiLucasMethod(neqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity.Diffusivity):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcBinaryDiffusionCoefficient(self, int: int, int2: int, int3: int) -> float: ...
    def calcBinaryDiffusionCoefficient2(self, int: int, int2: int, int3: int) -> float: ...

class Diffusivity: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity")``.

    AmineDiffusivity: typing.Type[AmineDiffusivity]
    CO2water: typing.Type[CO2water]
    Diffusivity: typing.Type[Diffusivity]
    SiddiqiLucasMethod: typing.Type[SiddiqiLucasMethod]
