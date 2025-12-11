
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.fluidmechanics.geometrydefinitions
import typing



class ReactorData(neqsim.fluidmechanics.geometrydefinitions.GeometryDefinition):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    def clone(self) -> 'ReactorData': ...
    @typing.overload
    def setPackingType(self, int: int) -> None: ...
    @typing.overload
    def setPackingType(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setPackingType(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.geometrydefinitions.reactor")``.

    ReactorData: typing.Type[ReactorData]
