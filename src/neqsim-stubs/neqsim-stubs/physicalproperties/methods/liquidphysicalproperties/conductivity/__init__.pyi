
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods.liquidphysicalproperties
import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.system
import typing



class Conductivity(neqsim.physicalproperties.methods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.ConductivityInterface):
    pureComponentConductivity: typing.MutableSequence[float] = ...
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcConductivity(self) -> float: ...
    def calcPureComponentConductivity(self) -> None: ...
    def clone(self) -> 'Conductivity': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.liquidphysicalproperties.conductivity")``.

    Conductivity: typing.Type[Conductivity]
