
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.system
import neqsim.thermo.phase
import typing



class SolidPhysicalProperties(neqsim.physicalproperties.system.PhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.system.solidphysicalproperties")``.

    SolidPhysicalProperties: typing.Type[SolidPhysicalProperties]
