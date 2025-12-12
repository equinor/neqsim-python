import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import neqsim
import jneqsim.thermo
import jneqsim.thermo.component
import jneqsim.thermo.phase
import typing

class MixingRuleHandler(jneqsim.thermo.ThermodynamicConstantsInterface):
    def __init__(self): ...
    def getName(self) -> java.lang.String: ...

class MixingRuleTypeInterface:
    def getValue(self) -> int: ...

class MixingRulesInterface(java.io.Serializable, java.lang.Cloneable):
    def getName(self) -> java.lang.String: ...

class CPAMixingRuleType(java.lang.Enum["CPAMixingRuleType"], MixingRuleTypeInterface):
    CPA_RADOCH: typing.ClassVar["CPAMixingRuleType"] = ...
    PCSAFTA_RADOCH: typing.ClassVar["CPAMixingRuleType"] = ...
    @staticmethod
    def byName(string: typing.Union[java.lang.String, str]) -> "CPAMixingRuleType": ...
    @staticmethod
    def byValue(int: int) -> "CPAMixingRuleType": ...
    def getValue(self) -> int: ...
    _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(
        class_: typing.Type[_valueOf_0__T], string: typing.Union[java.lang.String, str]
    ) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: typing.Union[java.lang.String, str]) -> "CPAMixingRuleType": ...
    @staticmethod
    def values() -> typing.MutableSequence["CPAMixingRuleType"]: ...

class CPAMixingRulesInterface(MixingRulesInterface):
    def calcDelta(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcDeltaNog(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcDeltadN(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        int5: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int6: int,
    ) -> float: ...
    def calcDeltadT(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcDeltadTdT(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcDeltadTdV(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcDeltadV(
        self,
        int: int,
        int2: int,
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...
    def calcXi(
        self,
        intArray: typing.Union[
            typing.List[typing.MutableSequence[typing.MutableSequence[int]]],
            jpype.JArray,
        ],
        intArray2: typing.Union[
            typing.List[
                typing.MutableSequence[
                    typing.MutableSequence[typing.MutableSequence[int]]
                ]
            ],
            jpype.JArray,
        ],
        int3: int,
        int4: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int5: int,
    ) -> float: ...

class ElectrolyteMixingRulesInterface(MixingRulesInterface):
    def calcW(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcWT(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcWTT(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcWi(
        self,
        int: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int2: int,
    ) -> float: ...
    def calcWiT(
        self,
        int: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int2: int,
    ) -> float: ...
    @typing.overload
    def calcWij(
        self,
        int: int,
        int2: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int3: int,
    ) -> float: ...
    @typing.overload
    def calcWij(self, phaseInterface: jneqsim.thermo.phase.PhaseInterface) -> None: ...
    def getWij(self, int: int, int2: int, double: float) -> float: ...
    def getWijParameter(self, int: int, int2: int) -> float: ...
    def getWijT(self, int: int, int2: int, double: float) -> float: ...
    def getWijTT(self, int: int, int2: int, double: float) -> float: ...
    def gettWijT1Parameter(self, int: int, int2: int) -> float: ...
    def gettWijT2Parameter(self, int: int, int2: int) -> float: ...
    def setWijParameter(self, int: int, int2: int, double: float) -> None: ...
    def setWijT1Parameter(self, int: int, int2: int, double: float) -> None: ...
    def setWijT2Parameter(self, int: int, int2: int, double: float) -> None: ...

class EosMixingRuleType(java.lang.Enum["EosMixingRuleType"], MixingRuleTypeInterface):
    NO: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC_HV: typing.ClassVar["EosMixingRuleType"] = ...
    HV: typing.ClassVar["EosMixingRuleType"] = ...
    WS: typing.ClassVar["EosMixingRuleType"] = ...
    CPA_MIX: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC_T: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC_T_CPA: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC_TX_CPA: typing.ClassVar["EosMixingRuleType"] = ...
    SOREIDE_WHITSON: typing.ClassVar["EosMixingRuleType"] = ...
    CLASSIC_T2: typing.ClassVar["EosMixingRuleType"] = ...
    @staticmethod
    def byName(string: typing.Union[java.lang.String, str]) -> "EosMixingRuleType": ...
    @staticmethod
    def byValue(int: int) -> "EosMixingRuleType": ...
    def getValue(self) -> int: ...
    _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(
        class_: typing.Type[_valueOf_0__T], string: typing.Union[java.lang.String, str]
    ) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: typing.Union[java.lang.String, str]) -> "EosMixingRuleType": ...
    @staticmethod
    def values() -> typing.MutableSequence["EosMixingRuleType"]: ...

class EosMixingRulesInterface(MixingRulesInterface):
    def calcA(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcAT(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcATT(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcAi(
        self,
        int: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int2: int,
    ) -> float: ...
    def calcAiT(
        self,
        int: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int2: int,
    ) -> float: ...
    def calcAij(
        self,
        int: int,
        int2: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int3: int,
    ) -> float: ...
    def calcB(
        self,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int: int,
    ) -> float: ...
    def calcBi(
        self,
        int: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int2: int,
    ) -> float: ...
    def calcBij(
        self,
        int: int,
        int2: int,
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        double: float,
        double2: float,
        int3: int,
    ) -> float: ...
    def getBinaryInteractionParameter(self, int: int, int2: int) -> float: ...
    def getBinaryInteractionParameterT1(self, int: int, int2: int) -> float: ...
    def getBinaryInteractionParameters(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getBmixType(self) -> int: ...
    def getGEPhase(self) -> jneqsim.thermo.phase.PhaseInterface: ...
    def setBinaryInteractionParameter(
        self, int: int, int2: int, double: float
    ) -> None: ...
    def setBinaryInteractionParameterT1(
        self, int: int, int2: int, double: float
    ) -> None: ...
    def setBinaryInteractionParameterij(
        self, int: int, int2: int, double: float
    ) -> None: ...
    def setBinaryInteractionParameterji(
        self, int: int, int2: int, double: float
    ) -> None: ...
    def setBmixType(self, int: int) -> None: ...
    def setCalcEOSInteractionParameters(self, boolean: bool) -> None: ...
    def setMixingRuleGEModel(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...
    def setnEOSkij(self, double: float) -> None: ...

class HVMixingRulesInterface(EosMixingRulesInterface):
    def getHVDijParameter(self, int: int, int2: int) -> float: ...
    def getHVDijTParameter(self, int: int, int2: int) -> float: ...
    def getHValphaParameter(self, int: int, int2: int) -> float: ...
    def getKijWongSandler(self, int: int, int2: int) -> float: ...
    def setHVDijParameter(self, int: int, int2: int, double: float) -> None: ...
    def setHVDijTParameter(self, int: int, int2: int, double: float) -> None: ...
    def setHValphaParameter(self, int: int, int2: int, double: float) -> None: ...
    def setKijWongSandler(self, int: int, int2: int, double: float) -> None: ...

class CPAMixingRuleHandler(MixingRuleHandler):
    def __init__(self): ...
    def clone(self) -> "CPAMixingRuleHandler": ...
    def getInteractionMatrix(
        self,
        intArray: typing.Union[typing.List[int], jpype.JArray],
        intArray2: typing.Union[typing.List[int], jpype.JArray],
    ) -> typing.MutableSequence[typing.MutableSequence[int]]: ...
    @typing.overload
    def getMixingRule(self, int: int) -> CPAMixingRulesInterface: ...
    @typing.overload
    def getMixingRule(
        self, int: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> CPAMixingRulesInterface: ...
    @typing.overload
    def getMixingRule(
        self,
        mixingRuleTypeInterface: typing.Union[MixingRuleTypeInterface, typing.Callable],
    ) -> CPAMixingRulesInterface: ...
    def resetMixingRule(
        self, int: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> MixingRulesInterface: ...
    def setAssociationScheme(
        self, int: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> typing.MutableSequence[typing.MutableSequence[int]]: ...
    def setCrossAssociationScheme(
        self, int: int, int2: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> typing.MutableSequence[typing.MutableSequence[int]]: ...

    class CPA_Radoch(jneqsim.thermo.mixingrule.CPAMixingRuleHandler.CPA_Radoch_base):
        def __init__(self, cPAMixingRuleHandler: "CPAMixingRuleHandler"): ...
        @typing.overload
        def calcDelta(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        @typing.overload
        def calcDelta(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def calcDeltaNog(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadN(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            int5: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int6: int,
        ) -> float: ...
        def calcDeltadT(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadTdT(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadTdV(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadV(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def getCrossAssociationEnergy(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def getCrossAssociationVolume(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def getName(self) -> java.lang.String: ...

    class CPA_Radoch_base(CPAMixingRulesInterface):
        def __init__(self, cPAMixingRuleHandler: "CPAMixingRuleHandler"): ...
        def calcDelta(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltaNog(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadN(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            int5: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int6: int,
        ) -> float: ...
        def calcDeltadT(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadTdT(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadTdV(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        def calcDeltadV(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        @typing.overload
        def calcXi(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def calcXi(
            self,
            intArray: typing.Union[
                typing.List[typing.MutableSequence[typing.MutableSequence[int]]],
                jpype.JArray,
            ],
            intArray2: typing.Union[
                typing.List[
                    typing.MutableSequence[
                        typing.MutableSequence[typing.MutableSequence[int]]
                    ]
                ],
                jpype.JArray,
            ],
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...

    class PCSAFTa_Radoch(jneqsim.thermo.mixingrule.CPAMixingRuleHandler.CPA_Radoch):
        def __init__(self, cPAMixingRuleHandler: "CPAMixingRuleHandler"): ...
        @typing.overload
        def calcDelta(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def calcDelta(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        @typing.overload
        def getCrossAssociationEnergy(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def getCrossAssociationEnergy(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...
        @typing.overload
        def getCrossAssociationVolume(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def getCrossAssociationVolume(
            self,
            int: int,
            int2: int,
            int3: int,
            int4: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int5: int,
        ) -> float: ...

class EosMixingRuleHandler(MixingRuleHandler):
    mixingRuleGEModel: java.lang.String = ...
    Atot: float = ...
    Btot: float = ...
    Ai: float = ...
    Bi: float = ...
    A: float = ...
    B: float = ...
    intparam: typing.MutableSequence[typing.MutableSequence[float]] = ...
    intparamT: typing.MutableSequence[typing.MutableSequence[float]] = ...
    WSintparam: typing.MutableSequence[typing.MutableSequence[float]] = ...
    intparamij: typing.MutableSequence[typing.MutableSequence[float]] = ...
    intparamji: typing.MutableSequence[typing.MutableSequence[float]] = ...
    intparamTType: typing.MutableSequence[typing.MutableSequence[int]] = ...
    nEOSkij: float = ...
    calcEOSInteractionParameters: typing.ClassVar[bool] = ...
    def __init__(self): ...
    def clone(self) -> "EosMixingRuleHandler": ...
    def displayInteractionCoefficients(
        self,
        string: typing.Union[java.lang.String, str],
        phaseInterface: jneqsim.thermo.phase.PhaseInterface,
    ) -> None: ...
    def equals(self, object: typing.Any) -> bool: ...
    def getClassicOrHV(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    def getClassicOrWS(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    def getElectrolyteMixingRule(
        self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> ElectrolyteMixingRulesInterface: ...
    def getHVDij(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getHVDijT(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getHValpha(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getMixingRule(self, int: int) -> EosMixingRulesInterface: ...
    @typing.overload
    def getMixingRule(
        self, int: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> EosMixingRulesInterface: ...
    def getMixingRuleName(self) -> java.lang.String: ...
    def getNRTLDij(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getNRTLDijT(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getNRTLalpha(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSRKbinaryInteractionParameters(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getWSintparam(
        self,
    ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def isCalcEOSInteractionParameters(self) -> bool: ...
    def resetMixingRule(
        self, int: int, phaseInterface: jneqsim.thermo.phase.PhaseInterface
    ) -> EosMixingRulesInterface: ...
    def setCalcEOSInteractionParameters(self, boolean: bool) -> None: ...
    def setMixingRuleGEModel(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...
    def setMixingRuleName(
        self, string: typing.Union[java.lang.String, str]
    ) -> None: ...

    class ClassicSRK(jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicVdW):
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def clone(self) -> "EosMixingRuleHandler.ClassicSRK": ...
        def getkij(self, double: float, int: int, int2: int) -> float: ...

    class ClassicSRKT(jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRK):
        @typing.overload
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        @typing.overload
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler", int: int): ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiTT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def clone(self) -> "EosMixingRuleHandler.ClassicSRKT": ...
        def getkij(self, double: float, int: int, int2: int) -> float: ...
        def getkijdT(self, double: float, int: int, int2: int) -> float: ...
        def getkijdTdT(self, double: float, int: int, int2: int) -> float: ...

    class ClassicSRKT2(jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRKT):
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        def clone(self) -> "EosMixingRuleHandler.ClassicSRKT": ...
        def getkij(self, double: float, int: int, int2: int) -> float: ...
        def getkijdT(self, double: float, int: int, int2: int) -> float: ...
        def getkijdTdT(self, double: float, int: int, int2: int) -> float: ...

    class ClassicSRKT2x(jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRKT2):
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def getkij(self, double: float, int: int, int2: int) -> float: ...
        @typing.overload
        def getkij(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            int: int,
            int2: int,
        ) -> float: ...
        def getkijdn(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            int2: int,
            int3: int,
        ) -> float: ...
        def getkijdndn(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            int3: int,
            int4: int,
        ) -> float: ...

    class ClassicVdW(EosMixingRulesInterface):
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def calcB(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcBFull(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcBi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcBi2(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcBiFull(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcBij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def clone(self) -> "EosMixingRuleHandler.ClassicVdW": ...
        def equals(self, object: typing.Any) -> bool: ...
        def getA(self) -> float: ...
        def getB(self) -> float: ...
        def getBinaryInteractionParameter(self, int: int, int2: int) -> float: ...
        def getBinaryInteractionParameterT1(self, int: int, int2: int) -> float: ...
        def getBinaryInteractionParameters(
            self,
        ) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
        def getBmixType(self) -> int: ...
        def getGEPhase(self) -> jneqsim.thermo.phase.PhaseInterface: ...
        def getName(self) -> java.lang.String: ...
        def getbij(
            self,
            componentEosInterface: jneqsim.thermo.component.ComponentEosInterface,
            componentEosInterface2: jneqsim.thermo.component.ComponentEosInterface,
        ) -> float: ...
        def prettyPrintKij(self) -> None: ...
        def setBinaryInteractionParameter(
            self, int: int, int2: int, double: float
        ) -> None: ...
        def setBinaryInteractionParameterT1(
            self, int: int, int2: int, double: float
        ) -> None: ...
        def setBinaryInteractionParameterij(
            self, int: int, int2: int, double: float
        ) -> None: ...
        def setBinaryInteractionParameterji(
            self, int: int, int2: int, double: float
        ) -> None: ...
        def setBmixType(self, int: int) -> None: ...
        def setCalcEOSInteractionParameters(self, boolean: bool) -> None: ...
        def setMixingRuleGEModel(
            self, string: typing.Union[java.lang.String, str]
        ) -> None: ...
        def setnEOSkij(self, double: float) -> None: ...

    class ElectrolyteMixRule(ElectrolyteMixingRulesInterface):
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
        ): ...
        def calcW(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcWT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcWTT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcWi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcWiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        @typing.overload
        def calcWij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        @typing.overload
        def calcWij(
            self, phaseInterface: jneqsim.thermo.phase.PhaseInterface
        ) -> None: ...
        def getName(self) -> java.lang.String: ...
        def getWij(self, int: int, int2: int, double: float) -> float: ...
        def getWijParameter(self, int: int, int2: int) -> float: ...
        def getWijT(self, int: int, int2: int, double: float) -> float: ...
        def getWijTT(self, int: int, int2: int, double: float) -> float: ...
        def gettWijT1Parameter(self, int: int, int2: int) -> float: ...
        def gettWijT2Parameter(self, int: int, int2: int) -> float: ...
        def setWijParameter(self, int: int, int2: int, double: float) -> None: ...
        def setWijT1Parameter(self, int: int, int2: int, double: float) -> None: ...
        def setWijT2Parameter(self, int: int, int2: int, double: float) -> None: ...

    class SRKHuronVidal(
        jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRK,
        HVMixingRulesInterface,
    ):
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray3: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def equals(self, object: typing.Any) -> bool: ...
        def getHVDijParameter(self, int: int, int2: int) -> float: ...
        def getHVDijTParameter(self, int: int, int2: int) -> float: ...
        def getHValphaParameter(self, int: int, int2: int) -> float: ...
        def getKijWongSandler(self, int: int, int2: int) -> float: ...
        def setHVDijParameter(self, int: int, int2: int, double: float) -> None: ...
        def setHVDijTParameter(self, int: int, int2: int, double: float) -> None: ...
        def setHValphaParameter(self, int: int, int2: int, double: float) -> None: ...
        def setKijWongSandler(self, int: int, int2: int, double: float) -> None: ...

    class SRKHuronVidal2(
        jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRK,
        HVMixingRulesInterface,
    ):
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray3: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def getGEPhase(self) -> jneqsim.thermo.phase.PhaseInterface: ...
        def getHVDijParameter(self, int: int, int2: int) -> float: ...
        def getHVDijTParameter(self, int: int, int2: int) -> float: ...
        def getHValphaParameter(self, int: int, int2: int) -> float: ...
        def getKijWongSandler(self, int: int, int2: int) -> float: ...
        def init(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> None: ...
        def setHVDijParameter(self, int: int, int2: int, double: float) -> None: ...
        def setHVDijTParameter(self, int: int, int2: int, double: float) -> None: ...
        def setHValphaParameter(self, int: int, int2: int, double: float) -> None: ...
        def setKijWongSandler(self, int: int, int2: int, double: float) -> None: ...

    class WhitsonSoreideMixingRule(
        jneqsim.thermo.mixingrule.EosMixingRuleHandler.ClassicSRK
    ):
        def __init__(self, eosMixingRuleHandler: "EosMixingRuleHandler"): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def getkijWhitsonSoreideAqueous(
            self,
            componentEosInterfaceArray: typing.Union[
                typing.List[jneqsim.thermo.component.ComponentEosInterface],
                jpype.JArray,
            ],
            double: float,
            double2: float,
            int: int,
            int2: int,
        ) -> float: ...

    class WongSandlerMixingRule(
        jneqsim.thermo.mixingrule.EosMixingRuleHandler.SRKHuronVidal2
    ):
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray3: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        @typing.overload
        def __init__(
            self,
            eosMixingRuleHandler: "EosMixingRuleHandler",
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            doubleArray: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            doubleArray2: typing.Union[
                typing.List[typing.MutableSequence[float]], jpype.JArray
            ],
            stringArray: typing.Union[
                typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
            ],
        ): ...
        def calcA(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcATT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcAi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcAij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def calcB(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcBT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcBTT(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> float: ...
        def calcBi(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcBiT(
            self,
            int: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int2: int,
        ) -> float: ...
        def calcBij(
            self,
            int: int,
            int2: int,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int3: int,
        ) -> float: ...
        def init(
            self,
            phaseInterface: jneqsim.thermo.phase.PhaseInterface,
            double: float,
            double2: float,
            int: int,
        ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.mixingrule")``.

    CPAMixingRuleHandler: typing.Type[CPAMixingRuleHandler]
    CPAMixingRuleType: typing.Type[CPAMixingRuleType]
    CPAMixingRulesInterface: typing.Type[CPAMixingRulesInterface]
    ElectrolyteMixingRulesInterface: typing.Type[ElectrolyteMixingRulesInterface]
    EosMixingRuleHandler: typing.Type[EosMixingRuleHandler]
    EosMixingRuleType: typing.Type[EosMixingRuleType]
    EosMixingRulesInterface: typing.Type[EosMixingRulesInterface]
    HVMixingRulesInterface: typing.Type[HVMixingRulesInterface]
    MixingRuleHandler: typing.Type[MixingRuleHandler]
    MixingRuleTypeInterface: typing.Type[MixingRuleTypeInterface]
    MixingRulesInterface: typing.Type[MixingRulesInterface]
