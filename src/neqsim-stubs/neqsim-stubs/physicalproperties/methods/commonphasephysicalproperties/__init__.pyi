
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods
import neqsim.physicalproperties.methods.commonphasephysicalproperties.conductivity
import neqsim.physicalproperties.methods.commonphasephysicalproperties.diffusivity
import neqsim.physicalproperties.methods.commonphasephysicalproperties.viscosity
import neqsim.physicalproperties.system
import typing



class CommonPhysicalPropertyMethod(neqsim.physicalproperties.methods.PhysicalPropertyMethod):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def setPhase(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.commonphasephysicalproperties")``.

    CommonPhysicalPropertyMethod: typing.Type[CommonPhysicalPropertyMethod]
    conductivity: neqsim.physicalproperties.methods.commonphasephysicalproperties.conductivity.__module_protocol__
    diffusivity: neqsim.physicalproperties.methods.commonphasephysicalproperties.diffusivity.__module_protocol__
    viscosity: neqsim.physicalproperties.methods.commonphasephysicalproperties.viscosity.__module_protocol__
