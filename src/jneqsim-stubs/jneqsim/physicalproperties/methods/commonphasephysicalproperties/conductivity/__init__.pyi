
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.commonphasephysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.system
import jneqsim.thermo.system
import typing



class Conductivity(jneqsim.physicalproperties.methods.commonphasephysicalproperties.CommonPhysicalPropertyMethod, jneqsim.physicalproperties.methods.methodinterface.ConductivityInterface):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def clone(self) -> 'Conductivity': ...

class CO2ConductivityMethod(Conductivity):
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcConductivity(self) -> float: ...

class PFCTConductivityMethodMod86(Conductivity):
    referenceSystem: typing.ClassVar[jneqsim.thermo.system.SystemInterface] = ...
    def __init__(self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties): ...
    def calcConductivity(self) -> float: ...
    def calcMixLPViscosity(self) -> float: ...
    def getRefComponentConductivity(self, double: float, double2: float) -> float: ...
    def getRefComponentViscosity(self, double: float, double2: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.commonphasephysicalproperties.conductivity")``.

    CO2ConductivityMethod: typing.Type[CO2ConductivityMethod]
    Conductivity: typing.Type[Conductivity]
    PFCTConductivityMethodMod86: typing.Type[PFCTConductivityMethodMod86]
