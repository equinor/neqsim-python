
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods
import jneqsim.physicalproperties.methods.liquidphysicalproperties.conductivity
import jneqsim.physicalproperties.methods.liquidphysicalproperties.density
import jneqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity
import jneqsim.physicalproperties.methods.liquidphysicalproperties.viscosity
import jneqsim.physicalproperties.system
import typing



class LiquidPhysicalPropertyMethod(jneqsim.physicalproperties.methods.PhysicalPropertyMethod):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def setPhase(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.liquidphysicalproperties")``.

    LiquidPhysicalPropertyMethod: typing.Type[LiquidPhysicalPropertyMethod]
    conductivity: jneqsim.physicalproperties.methods.liquidphysicalproperties.conductivity.__module_protocol__
    density: jneqsim.physicalproperties.methods.liquidphysicalproperties.density.__module_protocol__
    diffusivity: jneqsim.physicalproperties.methods.liquidphysicalproperties.diffusivity.__module_protocol__
    viscosity: jneqsim.physicalproperties.methods.liquidphysicalproperties.viscosity.__module_protocol__
