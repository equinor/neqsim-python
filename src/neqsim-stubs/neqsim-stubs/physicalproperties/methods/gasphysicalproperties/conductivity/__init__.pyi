
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods.gasphysicalproperties
import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.system
import typing



class Conductivity(neqsim.physicalproperties.methods.gasphysicalproperties.GasPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.ConductivityInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def clone(self) -> 'Conductivity': ...

class ChungConductivityMethod(Conductivity):
    pureComponentConductivity: typing.MutableSequence[float] = ...
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcConductivity(self) -> float: ...
    def calcPureComponentConductivity(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.gasphysicalproperties.conductivity")``.

    ChungConductivityMethod: typing.Type[ChungConductivityMethod]
    Conductivity: typing.Type[Conductivity]
