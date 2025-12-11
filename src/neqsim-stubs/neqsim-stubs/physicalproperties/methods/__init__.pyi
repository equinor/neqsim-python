
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import neqsim.physicalproperties.methods.commonphasephysicalproperties
import neqsim.physicalproperties.methods.gasphysicalproperties
import neqsim.physicalproperties.methods.liquidphysicalproperties
import neqsim.physicalproperties.methods.methodinterface
import neqsim.physicalproperties.methods.solidphysicalproperties
import neqsim.physicalproperties.system
import typing



class PhysicalPropertyMethodInterface(java.lang.Cloneable, java.io.Serializable):
    def clone(self) -> 'PhysicalPropertyMethodInterface': ...
    def setPhase(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties) -> None: ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...

class PhysicalPropertyMethod(PhysicalPropertyMethodInterface):
    def __init__(self, physicalProperties: neqsim.physicalproperties.system.PhysicalProperties): ...
    def clone(self) -> 'PhysicalPropertyMethod': ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.methods")``.

    PhysicalPropertyMethod: typing.Type[PhysicalPropertyMethod]
    PhysicalPropertyMethodInterface: typing.Type[PhysicalPropertyMethodInterface]
    commonphasephysicalproperties: neqsim.physicalproperties.methods.commonphasephysicalproperties.__module_protocol__
    gasphysicalproperties: neqsim.physicalproperties.methods.gasphysicalproperties.__module_protocol__
    liquidphysicalproperties: neqsim.physicalproperties.methods.liquidphysicalproperties.__module_protocol__
    methodinterface: neqsim.physicalproperties.methods.methodinterface.__module_protocol__
    solidphysicalproperties: neqsim.physicalproperties.methods.solidphysicalproperties.__module_protocol__
