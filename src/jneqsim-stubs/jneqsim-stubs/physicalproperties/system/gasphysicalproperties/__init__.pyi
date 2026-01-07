
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.system
import jneqsim.thermo.phase
import typing



class GasPhysicalProperties(jneqsim.physicalproperties.system.PhysicalProperties):
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...
    def clone(self) -> 'GasPhysicalProperties': ...

class AirPhysicalProperties(GasPhysicalProperties):
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...

class NaturalGasPhysicalProperties(GasPhysicalProperties):
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.system.gasphysicalproperties")``.

    AirPhysicalProperties: typing.Type[AirPhysicalProperties]
    GasPhysicalProperties: typing.Type[GasPhysicalProperties]
    NaturalGasPhysicalProperties: typing.Type[NaturalGasPhysicalProperties]
