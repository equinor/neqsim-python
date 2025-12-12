import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import jneqsim.physicalproperties.interfaceproperties.solidadsorption
import jneqsim.physicalproperties.interfaceproperties.surfacetension
import jneqsim.thermo.system
import typing

class InterphasePropertiesInterface(java.lang.Cloneable):
    def calcAdsorption(self) -> None: ...
    def clone(self) -> "InterphasePropertiesInterface": ...
    @typing.overload
    def getAdsorptionCalc(
        self, string: typing.Union[java.lang.String, str]
    ) -> (
        jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
    ): ...
    @typing.overload
    def getAdsorptionCalc(
        self,
    ) -> typing.MutableSequence[
        jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
    ]: ...
    def getInterfacialTensionModel(self) -> int: ...
    @typing.overload
    def getSurfaceTension(self, int: int, int2: int) -> float: ...
    @typing.overload
    def getSurfaceTension(
        self, int: int, int2: int, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    def getSurfaceTensionModel(
        self, int: int
    ) -> (
        jneqsim.physicalproperties.interfaceproperties.surfacetension.SurfaceTensionInterface
    ): ...
    @typing.overload
    def init(self) -> None: ...
    @typing.overload
    def init(self, systemInterface: jneqsim.thermo.system.SystemInterface) -> None: ...
    def initAdsorption(self) -> None: ...
    def setAdsorptionCalc(
        self,
        adsorptionInterfaceArray: typing.Union[
            typing.List[
                jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
            ],
            jpype.JArray,
        ],
    ) -> None: ...
    @typing.overload
    def setInterfacialTensionModel(self, int: int) -> None: ...
    @typing.overload
    def setInterfacialTensionModel(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> None: ...
    def setSolidAdsorbentMaterial(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...

class InterfaceProperties(InterphasePropertiesInterface, java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def calcAdsorption(self) -> None: ...
    def clone(self) -> "InterfaceProperties": ...
    @typing.overload
    def getAdsorptionCalc(
        self, string: typing.Union[java.lang.String, str]
    ) -> (
        jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
    ): ...
    @typing.overload
    def getAdsorptionCalc(
        self,
    ) -> typing.MutableSequence[
        jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
    ]: ...
    def getInterfacialTensionModel(self) -> int: ...
    @typing.overload
    def getSurfaceTension(self, int: int, int2: int) -> float: ...
    @typing.overload
    def getSurfaceTension(
        self, int: int, int2: int, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    def getSurfaceTensionModel(
        self, int: int
    ) -> (
        jneqsim.physicalproperties.interfaceproperties.surfacetension.SurfaceTensionInterface
    ): ...
    @typing.overload
    def init(self) -> None: ...
    @typing.overload
    def init(self, systemInterface: jneqsim.thermo.system.SystemInterface) -> None: ...
    def initAdsorption(self) -> None: ...
    def setAdsorptionCalc(
        self,
        adsorptionInterfaceArray: typing.Union[
            typing.List[
                jneqsim.physicalproperties.interfaceproperties.solidadsorption.AdsorptionInterface
            ],
            jpype.JArray,
        ],
    ) -> None: ...
    @typing.overload
    def setInterfacialTensionModel(self, int: int) -> None: ...
    @typing.overload
    def setInterfacialTensionModel(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> None: ...
    def setSolidAdsorbentMaterial(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.interfaceproperties")``.

    InterfaceProperties: typing.Type[InterfaceProperties]
    InterphasePropertiesInterface: typing.Type[InterphasePropertiesInterface]
    solidadsorption: (
        jneqsim.physicalproperties.interfaceproperties.solidadsorption.__module_protocol__
    )
    surfacetension: (
        jneqsim.physicalproperties.interfaceproperties.surfacetension.__module_protocol__
    )
