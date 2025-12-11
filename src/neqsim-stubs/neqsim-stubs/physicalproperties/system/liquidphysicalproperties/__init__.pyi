
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.system
import neqsim.thermo.phase
import typing



class CO2waterPhysicalProperties(neqsim.physicalproperties.system.PhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...
    def clone(self) -> 'CO2waterPhysicalProperties': ...

class LiquidPhysicalProperties(neqsim.physicalproperties.system.PhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...
    def clone(self) -> 'LiquidPhysicalProperties': ...

class AminePhysicalProperties(LiquidPhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...

class GlycolPhysicalProperties(LiquidPhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...

class WaterPhysicalProperties(LiquidPhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...

class SaltWaterPhysicalProperties(WaterPhysicalProperties):
    def __init__(self, phaseInterface: neqsim.thermo.phase.PhaseInterface, int: int, int2: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.system.liquidphysicalproperties")``.

    AminePhysicalProperties: typing.Type[AminePhysicalProperties]
    CO2waterPhysicalProperties: typing.Type[CO2waterPhysicalProperties]
    GlycolPhysicalProperties: typing.Type[GlycolPhysicalProperties]
    LiquidPhysicalProperties: typing.Type[LiquidPhysicalProperties]
    SaltWaterPhysicalProperties: typing.Type[SaltWaterPhysicalProperties]
    WaterPhysicalProperties: typing.Type[WaterPhysicalProperties]
