import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.methods.solidphysicalproperties
import jneqsim.physicalproperties.system
import typing

class Conductivity(
    jneqsim.physicalproperties.methods.solidphysicalproperties.SolidPhysicalPropertyMethod,
    jneqsim.physicalproperties.methods.methodinterface.ConductivityInterface,
):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def calcConductivity(self) -> float: ...
    def clone(self) -> "Conductivity": ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods.solidphysicalproperties.conductivity")``.

    Conductivity: typing.Type[Conductivity]
