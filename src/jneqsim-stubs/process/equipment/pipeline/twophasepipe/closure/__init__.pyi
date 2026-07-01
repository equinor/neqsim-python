import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.process.equipment.pipeline.twophasepipe
import typing

class GeometryCalculator(java.io.Serializable):
    def __init__(self): ...
    def approximateLiquidLevel(self, double: float, double2: float) -> float: ...
    def calcAnnularFilmThickness(self, double: float, double2: float) -> float: ...
    def calcAnnularGasPerimeter(self, double: float, double2: float) -> float: ...
    def calcAreaDerivative(self, double: float, double2: float) -> float: ...
    def calculateFromHoldup(
        self, double: float, double2: float
    ) -> "GeometryCalculator.StratifiedGeometry": ...
    def calculateFromLiquidLevel(
        self, double: float, double2: float
    ) -> "GeometryCalculator.StratifiedGeometry": ...
    def isStratifiedStable(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
    ) -> bool: ...

    class StratifiedGeometry(java.io.Serializable):
        liquidArea: float = ...
        gasArea: float = ...
        liquidWettedPerimeter: float = ...
        gasWettedPerimeter: float = ...
        interfacialWidth: float = ...
        liquidHydraulicDiameter: float = ...
        gasHydraulicDiameter: float = ...
        liquidAngle: float = ...
        liquidLevel: float = ...
        liquidHoldup: float = ...
        def __init__(self): ...

class InterfacialFriction(java.io.Serializable):
    def __init__(self): ...
    def calcAndreussiPersenCorrelation(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
    ) -> "InterfacialFriction.InterfacialFrictionResult": ...
    def calcHartCorrelation(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
    ) -> "InterfacialFriction.InterfacialFrictionResult": ...
    def calcInterfacialForce(
        self,
        flowRegime: jneqsim.process.equipment.pipeline.twophasepipe.PipeSection.FlowRegime,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
    ) -> float: ...
    def calculate(
        self,
        flowRegime: jneqsim.process.equipment.pipeline.twophasepipe.PipeSection.FlowRegime,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
    ) -> "InterfacialFriction.InterfacialFrictionResult": ...

    class InterfacialFrictionResult(java.io.Serializable):
        interfacialShear: float = ...
        frictionFactor: float = ...
        slipVelocity: float = ...
        interfacialAreaPerLength: float = ...
        def __init__(self): ...

class OilWaterFlowRegimeDetector(java.io.Serializable):
    def __init__(self): ...
    def calcCriticalDispersionVelocity(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
    ) -> float: ...
    def calcEffectiveViscosity(
        self, double: float, double2: float, double3: float, boolean: bool
    ) -> float: ...
    def calcInversionWaterFraction(
        self, double: float, double2: float, double3: float
    ) -> float: ...
    def calcMaxDropletDiameter(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
    ) -> float: ...
    def detect(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
    ) -> "OilWaterFlowRegimeDetector.OilWaterResult": ...
    def getCriticalWeber(self) -> float: ...
    def getInversionConstant(self) -> float: ...
    def isWaterDropoutLikely(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
    ) -> bool: ...
    def setCriticalWeber(self, double: float) -> None: ...
    def setInversionConstant(self, double: float) -> None: ...

    class OilWaterFlowRegime(
        java.lang.Enum["OilWaterFlowRegimeDetector.OilWaterFlowRegime"]
    ):
        STRATIFIED: typing.ClassVar["OilWaterFlowRegimeDetector.OilWaterFlowRegime"] = (
            ...
        )
        STRATIFIED_WITH_MIXING: typing.ClassVar[
            "OilWaterFlowRegimeDetector.OilWaterFlowRegime"
        ] = ...
        DISPERSED_OIL_IN_WATER: typing.ClassVar[
            "OilWaterFlowRegimeDetector.OilWaterFlowRegime"
        ] = ...
        DISPERSED_WATER_IN_OIL: typing.ClassVar[
            "OilWaterFlowRegimeDetector.OilWaterFlowRegime"
        ] = ...
        DUAL_DISPERSION: typing.ClassVar[
            "OilWaterFlowRegimeDetector.OilWaterFlowRegime"
        ] = ...
        ANNULAR: typing.ClassVar["OilWaterFlowRegimeDetector.OilWaterFlowRegime"] = ...
        SINGLE_PHASE: typing.ClassVar[
            "OilWaterFlowRegimeDetector.OilWaterFlowRegime"
        ] = ...
        _valueOf_0__T = typing.TypeVar("_valueOf_0__T", bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(
            class_: typing.Type[_valueOf_0__T],
            string: typing.Union[java.lang.String, str],
        ) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(
            string: typing.Union[java.lang.String, str]
        ) -> "OilWaterFlowRegimeDetector.OilWaterFlowRegime": ...
        @staticmethod
        def values() -> (
            typing.MutableSequence["OilWaterFlowRegimeDetector.OilWaterFlowRegime"]
        ): ...

    class OilWaterResult:
        regime: "OilWaterFlowRegimeDetector.OilWaterFlowRegime" = ...
        waterWetting: bool = ...
        effectiveViscosity: float = ...
        inversionWaterFraction: float = ...
        criticalDispersionVelocity: float = ...
        maxDropletDiameter: float = ...
        oilContinuous: bool = ...
        waterDropoutRisk: bool = ...
        def __init__(
            self,
            oilWaterFlowRegime: "OilWaterFlowRegimeDetector.OilWaterFlowRegime",
            boolean: bool,
            double: float,
            double2: float,
            double3: float,
            double4: float,
            boolean2: bool,
            boolean3: bool,
        ): ...

class WallFriction(java.io.Serializable):
    def __init__(self): ...
    def calcColebrookFanning(
        self, double: float, double2: float, double3: float
    ) -> float: ...
    def calcFanningFrictionFactor(
        self, double: float, double2: float, double3: float
    ) -> float: ...
    def calculate(
        self,
        flowRegime: jneqsim.process.equipment.pipeline.twophasepipe.PipeSection.FlowRegime,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
    ) -> "WallFriction.WallFrictionResult": ...
    def getDefaultRoughness(self) -> float: ...
    def setDefaultRoughness(self, double: float) -> None: ...

    class WallFrictionResult(java.io.Serializable):
        gasWallShear: float = ...
        liquidWallShear: float = ...
        gasFrictionFactor: float = ...
        liquidFrictionFactor: float = ...
        gasReynolds: float = ...
        liquidReynolds: float = ...
        def __init__(self): ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.pipeline.twophasepipe.closure")``.

    GeometryCalculator: typing.Type[GeometryCalculator]
    InterfacialFriction: typing.Type[InterfacialFriction]
    OilWaterFlowRegimeDetector: typing.Type[OilWaterFlowRegimeDetector]
    WallFriction: typing.Type[WallFriction]
