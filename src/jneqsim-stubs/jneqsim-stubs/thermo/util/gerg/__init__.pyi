import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.thermo.phase
import org.netlib.util
import typing

class DETAIL:
    def __init__(self): ...
    def DensityDetail(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        intW: org.netlib.util.intW,
        stringW: org.netlib.util.StringW,
    ) -> None: ...
    def MolarMassDetail(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
    ) -> None: ...
    def PressureDetail(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
    ) -> None: ...
    def PropertiesDetail(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
        doubleW3: org.netlib.util.doubleW,
        doubleW4: org.netlib.util.doubleW,
        doubleW5: org.netlib.util.doubleW,
        doubleW6: org.netlib.util.doubleW,
        doubleW7: org.netlib.util.doubleW,
        doubleW8: org.netlib.util.doubleW,
        doubleW9: org.netlib.util.doubleW,
        doubleW10: org.netlib.util.doubleW,
        doubleW11: org.netlib.util.doubleW,
        doubleW12: org.netlib.util.doubleW,
        doubleW13: org.netlib.util.doubleW,
        doubleW14: org.netlib.util.doubleW,
        doubleW15: org.netlib.util.doubleW,
    ) -> None: ...
    def SetupDetail(self) -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def sq(self, double: float) -> float: ...

class EOSCG:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, eOSCGCorrelationBackend: "EOSCGCorrelationBackend"): ...
    def alpha0(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleWArray: typing.Union[typing.List[org.netlib.util.doubleW], jpype.JArray],
    ) -> None: ...
    def alphar(
        self,
        int: int,
        int2: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleWArray: typing.Union[
            typing.List[typing.MutableSequence[org.netlib.util.doubleW]], jpype.JArray
        ],
    ) -> None: ...
    def density(
        self,
        int: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        intW: org.netlib.util.intW,
        stringW: org.netlib.util.StringW,
    ) -> None: ...
    def molarMass(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
    ) -> None: ...
    def pressure(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
    ) -> None: ...
    def properties(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
        doubleW3: org.netlib.util.doubleW,
        doubleW4: org.netlib.util.doubleW,
        doubleW5: org.netlib.util.doubleW,
        doubleW6: org.netlib.util.doubleW,
        doubleW7: org.netlib.util.doubleW,
        doubleW8: org.netlib.util.doubleW,
        doubleW9: org.netlib.util.doubleW,
        doubleW10: org.netlib.util.doubleW,
        doubleW11: org.netlib.util.doubleW,
        doubleW12: org.netlib.util.doubleW,
        doubleW13: org.netlib.util.doubleW,
        doubleW14: org.netlib.util.doubleW,
        doubleW15: org.netlib.util.doubleW,
        doubleW16: org.netlib.util.doubleW,
    ) -> None: ...
    def setup(self) -> None: ...

class EOSCGCorrelationBackend:
    def __init__(self): ...
    def alpha0(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleWArray: typing.Union[typing.List[org.netlib.util.doubleW], jpype.JArray],
    ) -> None: ...
    def alphar(
        self,
        int: int,
        int2: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleWArray: typing.Union[
            typing.List[typing.MutableSequence[org.netlib.util.doubleW]], jpype.JArray
        ],
    ) -> None: ...
    def density(
        self,
        int: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        intW: org.netlib.util.intW,
        stringW: org.netlib.util.StringW,
    ) -> None: ...
    def molarMass(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
    ) -> None: ...
    def pressure(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
    ) -> None: ...
    def properties(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
        doubleW3: org.netlib.util.doubleW,
        doubleW4: org.netlib.util.doubleW,
        doubleW5: org.netlib.util.doubleW,
        doubleW6: org.netlib.util.doubleW,
        doubleW7: org.netlib.util.doubleW,
        doubleW8: org.netlib.util.doubleW,
        doubleW9: org.netlib.util.doubleW,
        doubleW10: org.netlib.util.doubleW,
        doubleW11: org.netlib.util.doubleW,
        doubleW12: org.netlib.util.doubleW,
        doubleW13: org.netlib.util.doubleW,
        doubleW14: org.netlib.util.doubleW,
        doubleW15: org.netlib.util.doubleW,
        doubleW16: org.netlib.util.doubleW,
    ) -> None: ...
    def setup(self) -> None: ...

class EOSCGModel:
    def __init__(self): ...
    def DensityEOSCG(
        self,
        int: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        intW: org.netlib.util.intW,
        stringW: org.netlib.util.StringW,
    ) -> None: ...
    def MolarMassEOSCG(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
    ) -> None: ...
    def PressureEOSCG(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
    ) -> None: ...
    def PropertiesEOSCG(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
        doubleW3: org.netlib.util.doubleW,
        doubleW4: org.netlib.util.doubleW,
        doubleW5: org.netlib.util.doubleW,
        doubleW6: org.netlib.util.doubleW,
        doubleW7: org.netlib.util.doubleW,
        doubleW8: org.netlib.util.doubleW,
        doubleW9: org.netlib.util.doubleW,
        doubleW10: org.netlib.util.doubleW,
        doubleW11: org.netlib.util.doubleW,
        doubleW12: org.netlib.util.doubleW,
        doubleW13: org.netlib.util.doubleW,
        doubleW14: org.netlib.util.doubleW,
        doubleW15: org.netlib.util.doubleW,
        doubleW16: org.netlib.util.doubleW,
    ) -> None: ...
    def SetupEOSCG(self) -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class GERG2008:
    def __init__(self): ...
    def DensityGERG(
        self,
        int: int,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        intW: org.netlib.util.intW,
        stringW: org.netlib.util.StringW,
    ) -> None: ...
    def MolarMassGERG(
        self,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
    ) -> None: ...
    def PressureGERG(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
    ) -> None: ...
    def PropertiesGERG(
        self,
        double: float,
        double2: float,
        doubleArray: typing.Union[typing.List[float], jpype.JArray],
        doubleW: org.netlib.util.doubleW,
        doubleW2: org.netlib.util.doubleW,
        doubleW3: org.netlib.util.doubleW,
        doubleW4: org.netlib.util.doubleW,
        doubleW5: org.netlib.util.doubleW,
        doubleW6: org.netlib.util.doubleW,
        doubleW7: org.netlib.util.doubleW,
        doubleW8: org.netlib.util.doubleW,
        doubleW9: org.netlib.util.doubleW,
        doubleW10: org.netlib.util.doubleW,
        doubleW11: org.netlib.util.doubleW,
        doubleW12: org.netlib.util.doubleW,
        doubleW13: org.netlib.util.doubleW,
        doubleW14: org.netlib.util.doubleW,
        doubleW15: org.netlib.util.doubleW,
        doubleW16: org.netlib.util.doubleW,
    ) -> None: ...
    def SetupGERG(self) -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class GERG2008Type(java.lang.Enum["GERG2008Type"]):
    STANDARD: typing.ClassVar["GERG2008Type"] = ...
    HYDROGEN_ENHANCED: typing.ClassVar["GERG2008Type"] = ...
    def getDescription(self) -> java.lang.String: ...
    def getName(self) -> java.lang.String: ...
    def toString(self) -> java.lang.String: ...
    _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(
        class_: typing.Type[_valueOf_0__T], string: typing.Union[java.lang.String, str]
    ) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: typing.Union[java.lang.String, str]) -> "GERG2008Type": ...
    @staticmethod
    def values() -> typing.MutableSequence["GERG2008Type"]: ...

class NeqSimAGA8Detail:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface): ...
    @typing.overload
    def getDensity(self) -> float: ...
    @typing.overload
    def getDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    @typing.overload
    def getMolarDensity(self) -> float: ...
    @typing.overload
    def getMolarDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getMolarMass(self) -> float: ...
    def getPressure(self) -> float: ...
    def getProperties(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def normalizeComposition(self) -> None: ...
    @typing.overload
    def propertiesDetail(self) -> typing.MutableSequence[float]: ...
    @typing.overload
    def propertiesDetail(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> typing.MutableSequence[float]: ...
    def setPhase(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> None: ...

class NeqSimEOSCG:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface): ...
    def getAlpha0_EOSCG(self) -> typing.MutableSequence[org.netlib.util.doubleW]: ...
    def getAlphares_EOSCG(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[org.netlib.util.doubleW]]: ...
    @typing.overload
    def getDensity(self) -> float: ...
    @typing.overload
    def getDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    @typing.overload
    def getMolarDensity(self) -> float: ...
    @typing.overload
    def getMolarDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getMolarMass(self) -> float: ...
    def getPressure(self) -> float: ...
    def getProperties(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...
    def normalizeComposition(self) -> None: ...
    def propertiesEOSCG(self) -> typing.MutableSequence[float]: ...
    def setPhase(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> None: ...

class NeqSimGERG2008:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface): ...
    @typing.overload
    def __init__(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        gERG2008Type: GERG2008Type,
    ): ...
    def getAlpha0_GERG2008(self) -> typing.MutableSequence[org.netlib.util.doubleW]: ...
    def getAlphares_GERG2008(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[org.netlib.util.doubleW]]: ...
    @typing.overload
    def getDensity(self) -> float: ...
    @typing.overload
    def getDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getModelType(self) -> GERG2008Type: ...
    @typing.overload
    def getMolarDensity(self) -> float: ...
    @typing.overload
    def getMolarDensity(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> float: ...
    def getMolarMass(self) -> float: ...
    def getPressure(self) -> float: ...
    def getProperties(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ) -> typing.MutableSequence[float]: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def normalizeComposition(self) -> None: ...
    @typing.overload
    def propertiesGERG(self) -> typing.MutableSequence[float]: ...
    @typing.overload
    def propertiesGERG(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> typing.MutableSequence[float]: ...
    def setModelType(self, gERG2008Type: GERG2008Type) -> None: ...
    def setPhase(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> None: ...

class GERG2008H2(GERG2008):
    def __init__(self): ...
    def SetupGERG(self) -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.gerg")``.

    DETAIL: typing.Type[DETAIL]
    EOSCG: typing.Type[EOSCG]
    EOSCGCorrelationBackend: typing.Type[EOSCGCorrelationBackend]
    EOSCGModel: typing.Type[EOSCGModel]
    GERG2008: typing.Type[GERG2008]
    GERG2008H2: typing.Type[GERG2008H2]
    GERG2008Type: typing.Type[GERG2008Type]
    NeqSimAGA8Detail: typing.Type[NeqSimAGA8Detail]
    NeqSimEOSCG: typing.Type[NeqSimEOSCG]
    NeqSimGERG2008: typing.Type[NeqSimGERG2008]
