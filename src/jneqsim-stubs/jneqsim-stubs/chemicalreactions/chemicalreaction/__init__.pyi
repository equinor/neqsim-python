import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import Jama
import java.lang
import java.util
import jpype
import jneqsim.thermo
import jneqsim.thermo.component
import jneqsim.thermo.phase
import jneqsim.thermo.system
import jneqsim.util
import typing

class ChemicalReaction(
    jneqsim.util.NamedBaseClass, jneqsim.thermo.ThermodynamicConstantsInterface
):
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
        double3: float,
        double4: float,
        double5: float,
    ): ...
    def calcK(
        self, systemInterface: jneqsim.thermo.system.SystemInterface, int: int
    ) -> float: ...
    def calcKgamma(
        self, systemInterface: jneqsim.thermo.system.SystemInterface, int: int
    ) -> float: ...
    def calcKx(
        self, systemInterface: jneqsim.thermo.system.SystemInterface, int: int
    ) -> float: ...
    def checkK(
        self, systemInterface: jneqsim.thermo.system.SystemInterface
    ) -> None: ...
    def getActivationEnergy(self) -> float: ...
    @typing.overload
    def getK(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> float: ...
    @typing.overload
    def getK(self) -> typing.MutableSequence[float]: ...
    def getNames(self) -> typing.MutableSequence[java.lang.String]: ...
    def getProductNames(self) -> typing.MutableSequence[java.lang.String]: ...
    @typing.overload
    def getRateFactor(self) -> float: ...
    @typing.overload
    def getRateFactor(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getReactantNames(self) -> typing.MutableSequence[java.lang.String]: ...
    def getReactionHeat(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getSaturationRatio(
        self, systemInterface: jneqsim.thermo.system.SystemInterface, int: int
    ) -> float: ...
    def getStocCoefs(self) -> typing.MutableSequence[float]: ...
    def init(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> None: ...
    def initMoleNumbers(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        componentInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.component.ComponentInterface], jpype.JArray
        ],
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
    ) -> None: ...
    def reactantsContains(
        self, stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> bool: ...
    def setActivationEnergy(self, double: float) -> None: ...
    @typing.overload
    def setK(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...
    @typing.overload
    def setK(self, int: int, double: float) -> None: ...
    def setRateFactor(self, double: float) -> None: ...

class ChemicalReactionFactory:
    @staticmethod
    def getChemicalReaction(
        string: typing.Union[java.lang.String, str]
    ) -> ChemicalReaction: ...
    @staticmethod
    def getChemicalReactionNames() -> typing.MutableSequence[java.lang.String]: ...

class ChemicalReactionList(jneqsim.thermo.ThermodynamicConstantsInterface):
    def __init__(self): ...
    def calcReacMatrix(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> None: ...
    def calcReacRates(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        componentInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.component.ComponentInterface], jpype.JArray
        ],
    ) -> Jama.Matrix: ...
    def calcReferencePotentials(self) -> typing.MutableSequence[float]: ...
    def checkReactions(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> None: ...
    def createReactionMatrix(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        componentInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.component.ComponentInterface], jpype.JArray
        ],
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAllComponents(self) -> typing.MutableSequence[java.lang.String]: ...
    def getChemicalReactionList(self) -> java.util.ArrayList[ChemicalReaction]: ...
    def getReacMatrix(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getReaction(self, int: int) -> ChemicalReaction: ...
    @typing.overload
    def getReaction(
        self, string: typing.Union[java.lang.String, str]
    ) -> ChemicalReaction: ...
    def getReactionGMatrix(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getReactionMatrix(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getStocMatrix(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def initMoleNumbers(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        componentInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.component.ComponentInterface], jpype.JArray
        ],
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ],
        doubleArray2: typing.Union[typing.List[float], jpype.JArray],
    ) -> None: ...
    def reacHeat(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        string: typing.Union[java.lang.String, str],
    ) -> float: ...
    def readReactions(
        self, systemInterface: jneqsim.thermo.system.SystemInterface
    ) -> None: ...
    def removeJunkReactions(
        self, stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def setChemicalReactionList(
        self, arrayList: java.util.ArrayList[ChemicalReaction]
    ) -> None: ...
    def updateReferencePotentials(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        componentInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.component.ComponentInterface], jpype.JArray
        ],
    ) -> typing.MutableSequence[float]: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.chemicalreactions.chemicalreaction")``.

    ChemicalReaction: typing.Type[ChemicalReaction]
    ChemicalReactionFactory: typing.Type[ChemicalReactionFactory]
    ChemicalReactionList: typing.Type[ChemicalReactionList]
