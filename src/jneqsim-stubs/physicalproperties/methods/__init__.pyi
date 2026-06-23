import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.physicalproperties.methods.commonphasephysicalproperties
import jneqsim.physicalproperties.methods.gasphysicalproperties
import jneqsim.physicalproperties.methods.liquidphysicalproperties
import jneqsim.physicalproperties.methods.methodinterface
import jneqsim.physicalproperties.methods.solidphysicalproperties
import jneqsim.physicalproperties.system
import typing

class PhysicalPropertyMethodInterface(java.lang.Cloneable, java.io.Serializable):
    def clone(self) -> "PhysicalPropertyMethodInterface": ...
    def setPhase(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ) -> None: ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...

class PhysicalPropertyMethod(PhysicalPropertyMethodInterface):
    def __init__(
        self, physicalProperties: jneqsim.physicalproperties.system.PhysicalProperties
    ): ...
    def clone(self) -> "PhysicalPropertyMethod": ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.methods")``.

    PhysicalPropertyMethod: typing.Type[PhysicalPropertyMethod]
    PhysicalPropertyMethodInterface: typing.Type[PhysicalPropertyMethodInterface]
    commonphasephysicalproperties: (
        jneqsim.physicalproperties.methods.commonphasephysicalproperties.__module_protocol__
    )
    gasphysicalproperties: (
        jneqsim.physicalproperties.methods.gasphysicalproperties.__module_protocol__
    )
    liquidphysicalproperties: (
        jneqsim.physicalproperties.methods.liquidphysicalproperties.__module_protocol__
    )
    methodinterface: (
        jneqsim.physicalproperties.methods.methodinterface.__module_protocol__
    )
    solidphysicalproperties: (
        jneqsim.physicalproperties.methods.solidphysicalproperties.__module_protocol__
    )
