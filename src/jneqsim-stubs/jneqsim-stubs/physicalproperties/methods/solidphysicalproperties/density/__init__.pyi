
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.methods.solidphysicalproperties
import jneqsim.physicalproperties.system
import typing



class Density(jneqsim.physicalproperties.methods.solidphysicalproperties.SolidPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.DensityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.solidphysicalproperties.density")``.

    Density: typing.Type[Density]
