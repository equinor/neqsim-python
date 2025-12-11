
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods.gasphysicalproperties
import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.system
import typing



class Density(neqsim.physicalproperties.methods.gasphysicalproperties.GasPhysicalPropertyMethod, neqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.gasphysicalproperties.density")``.

    Density: typing.Type[Density]
