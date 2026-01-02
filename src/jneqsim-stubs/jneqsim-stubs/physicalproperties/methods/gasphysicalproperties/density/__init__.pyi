
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.gasphysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.system
import typing



class Density(jneqsim.physicalproperties.methods.gasphysicalproperties.GasPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.gasphysicalproperties.density")``.

    Density: typing.Type[Density]
