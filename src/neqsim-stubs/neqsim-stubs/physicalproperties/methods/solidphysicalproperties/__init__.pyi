
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods
import neqsim.physicalproperties.methods.solidphysicalproperties.conductivity
import neqsim.physicalproperties.methods.solidphysicalproperties.density
import neqsim.physicalproperties.methods.solidphysicalproperties.diffusivity
import neqsim.physicalproperties.methods.solidphysicalproperties.viscosity
import neqsim.physicalproperties.system
import typing



class SolidPhysicalPropertyMethod(neqsim.physicalproperties.methods.PhysicalPropertyMethod):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def setPhase(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.solidphysicalproperties")``.

    SolidPhysicalPropertyMethod: typing.Type[SolidPhysicalPropertyMethod]
    conductivity: neqsim.physicalproperties.methods.solidphysicalproperties.conductivity.__module_protocol__
    density: neqsim.physicalproperties.methods.solidphysicalproperties.density.__module_protocol__
    diffusivity: neqsim.physicalproperties.methods.solidphysicalproperties.diffusivity.__module_protocol__
    viscosity: neqsim.physicalproperties.methods.solidphysicalproperties.viscosity.__module_protocol__
