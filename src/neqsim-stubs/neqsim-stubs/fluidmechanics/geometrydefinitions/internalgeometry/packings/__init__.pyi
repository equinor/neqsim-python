
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.util
import typing



class PackingInterface:
    def getSize(self) -> float: ...
    def getSurfaceAreaPrVolume(self) -> float: ...
    def getVoidFractionPacking(self) -> float: ...
    def setVoidFractionPacking(self, double: float) -> None: ...

class Packing(neqsim.util.NamedBaseClass, PackingInterface):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], int: int): ...
    def getSize(self) -> float: ...
    def getSurfaceAreaPrVolume(self) -> float: ...
    def getVoidFractionPacking(self) -> float: ...
    def setSize(self, double: float) -> None: ...
    def setVoidFractionPacking(self, double: float) -> None: ...

class BerlSaddlePacking(Packing):
    def __init__(self): ...

class PallRingPacking(Packing):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], int: int): ...

class RachigRingPacking(Packing):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], int: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.geometrydefinitions.internalgeometry.packings")``.

    BerlSaddlePacking: typing.Type[BerlSaddlePacking]
    Packing: typing.Type[Packing]
    PackingInterface: typing.Type[PackingInterface]
    PallRingPacking: typing.Type[PallRingPacking]
    RachigRingPacking: typing.Type[RachigRingPacking]
