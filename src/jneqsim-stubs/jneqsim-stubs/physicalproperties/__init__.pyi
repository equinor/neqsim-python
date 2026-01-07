
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.physicalproperties.interfaceproperties
import jneqsim.physicalproperties.methods
import jneqsim.physicalproperties.mixingrule
import jneqsim.physicalproperties.system
import jneqsim.physicalproperties.util
import jneqsim.thermo.phase
import typing



class PhysicalPropertyHandler(java.lang.Cloneable, java.io.Serializable):
    def __init__(self): ...
    def clone(self) -> 'PhysicalPropertyHandler': ...
    def getPhysicalProperties(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> jneqsim.physicalproperties.system.PhysicalProperties: ...
    def setPhysicalProperties(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface, physicalPropertyModel: jneqsim.physicalproperties.system.PhysicalPropertyModel) -> None: ...

class PhysicalPropertyType(java.lang.Enum['PhysicalPropertyType']):
    MASS_DENSITY: typing.ClassVar['PhysicalPropertyType'] = ...
    DYNAMIC_VISCOSITY: typing.ClassVar['PhysicalPropertyType'] = ...
    THERMAL_CONDUCTIVITY: typing.ClassVar['PhysicalPropertyType'] = ...
    @staticmethod
    def byName(string: typing.Union[java.lang.String, str]) -> 'PhysicalPropertyType': ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: typing.Union[java.lang.String, str]) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: typing.Union[java.lang.String, str]) -> 'PhysicalPropertyType': ...
    @staticmethod
    def values() -> typing.MutableSequence['PhysicalPropertyType']: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties")``.

    PhysicalPropertyHandler: typing.Type[PhysicalPropertyHandler]
    PhysicalPropertyType: typing.Type[PhysicalPropertyType]
    interfaceproperties: jneqsim.physicalproperties.interfaceproperties.__module_protocol__
    methods: jneqsim.physicalproperties.methods.__module_protocol__
    mixingrule: jneqsim.physicalproperties.mixingrule.__module_protocol__
    system: jneqsim.physicalproperties.system.__module_protocol__
    util: jneqsim.physicalproperties.util.__module_protocol__
