
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.methods
import neqsim.physicalproperties.methods.gasphysicalproperties.conductivity
import neqsim.physicalproperties.methods.gasphysicalproperties.density
import neqsim.physicalproperties.methods.gasphysicalproperties.diffusivity
import neqsim.physicalproperties.methods.gasphysicalproperties.viscosity
import neqsim.physicalproperties.system
import typing



class GasPhysicalPropertyMethod(neqsim.physicalproperties.methods.PhysicalPropertyMethod):
    binaryMolecularDiameter: typing.MutableSequence[typing.MutableSequence[float]] = ...
    binaryEnergyParameter: typing.MutableSequence[typing.MutableSequence[float]] = ...
    binaryMolecularMass: typing.MutableSequence[typing.MutableSequence[float]] = ...
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def setPhase(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods.gasphysicalproperties")``.

    GasPhysicalPropertyMethod: typing.Type[GasPhysicalPropertyMethod]
    conductivity: neqsim.physicalproperties.methods.gasphysicalproperties.conductivity.__module_protocol__
    density: neqsim.physicalproperties.methods.gasphysicalproperties.density.__module_protocol__
    diffusivity: neqsim.physicalproperties.methods.gasphysicalproperties.diffusivity.__module_protocol__
    viscosity: neqsim.physicalproperties.methods.gasphysicalproperties.viscosity.__module_protocol__
