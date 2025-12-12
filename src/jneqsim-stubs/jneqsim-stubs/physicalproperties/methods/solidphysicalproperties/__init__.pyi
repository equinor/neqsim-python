import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods
import jneqsim.physicalproperties.methods.solidphysicalproperties.conductivity
import jneqsim.physicalproperties.methods.solidphysicalproperties.density
import jneqsim.physicalproperties.methods.solidphysicalproperties.diffusivity
import jneqsim.physicalproperties.methods.solidphysicalproperties.viscosity
import jneqsim.physicalproperties.system
import typing

class SolidPhysicalPropertyMethod(
    jneqsim.physicalproperties.methods.PhysicalPropertyMethod
):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def setPhase(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.solidphysicalproperties")``.

    SolidPhysicalPropertyMethod: typing.Type[SolidPhysicalPropertyMethod]
    conductivity: (
        jneqsim.physicalproperties.methods.solidphysicalproperties.conductivity.__module_protocol__
    )
    density: (
        jneqsim.physicalproperties.methods.solidphysicalproperties.density.__module_protocol__
    )
    diffusivity: (
        jneqsim.physicalproperties.methods.solidphysicalproperties.diffusivity.__module_protocol__
    )
    viscosity: (
        jneqsim.physicalproperties.methods.solidphysicalproperties.viscosity.__module_protocol__
    )
