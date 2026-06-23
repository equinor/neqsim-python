import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods
import jneqsim.physicalproperties.methods.commonphasephysicalproperties.conductivity
import jneqsim.physicalproperties.methods.commonphasephysicalproperties.diffusivity
import jneqsim.physicalproperties.methods.commonphasephysicalproperties.viscosity
import jneqsim.physicalproperties.system
import typing

class CommonPhysicalPropertyMethod(
    jneqsim.physicalproperties.methods.PhysicalPropertyMethod
):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def setPhase(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.commonphasephysicalproperties")``.

    CommonPhysicalPropertyMethod: typing.Type[CommonPhysicalPropertyMethod]
    conductivity: (
        jneqsim.physicalproperties.methods.commonphasephysicalproperties.conductivity.__module_protocol__
    )
    diffusivity: (
        jneqsim.physicalproperties.methods.commonphasephysicalproperties.diffusivity.__module_protocol__
    )
    viscosity: (
        jneqsim.physicalproperties.methods.commonphasephysicalproperties.viscosity.__module_protocol__
    )
