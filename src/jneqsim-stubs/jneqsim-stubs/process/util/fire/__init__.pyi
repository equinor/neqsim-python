import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.process.equipment.flare
import jneqsim.process.equipment.separator
import typing

class FireHeatLoadCalculator:
    STEFAN_BOLTZMANN: typing.ClassVar[float] = ...
    @staticmethod
    def api521PoolFireHeatLoad(double: float, double2: float) -> float: ...
    @staticmethod
    def generalizedStefanBoltzmannHeatFlux(
        double: float, double2: float, double3: float, double4: float
    ) -> float: ...

class FireHeatTransferCalculator:
    @staticmethod
    def calculateWallTemperatures(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
    ) -> "FireHeatTransferCalculator.SurfaceTemperatureResult": ...

    class SurfaceTemperatureResult:
        def __init__(self, double: float, double2: float, double3: float): ...
        def heatFlux(self) -> float: ...
        def innerWallTemperatureK(self) -> float: ...
        def outerWallTemperatureK(self) -> float: ...

class ReliefValveSizing:
    R_GAS: typing.ClassVar[float] = ...
    STANDARD_ORIFICE_AREAS_IN2: typing.ClassVar[typing.MutableSequence[float]] = ...
    STANDARD_ORIFICE_LETTERS: typing.ClassVar[
        typing.MutableSequence[java.lang.String]
    ] = ...
    @staticmethod
    def calculateBlowdownPressure(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateCv(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateMassFlowCapacity(
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
    @staticmethod
    def calculateMaxHeatAbsorption(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateRequiredArea(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        boolean: bool,
        boolean2: bool,
    ) -> "ReliefValveSizing.PSVSizingResult": ...
    @staticmethod
    def dynamicFireSizing(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
        double10: float,
        double11: float,
    ) -> "ReliefValveSizing.PSVSizingResult": ...
    @staticmethod
    def getNextLargerOrifice(
        string: typing.Union[java.lang.String, str]
    ) -> java.lang.String: ...
    @staticmethod
    def getStandardOrificeArea(
        string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @staticmethod
    def validateSizing(
        pSVSizingResult: "ReliefValveSizing.PSVSizingResult", boolean: bool
    ) -> java.lang.String: ...

    class PSVSizingResult:
        def __init__(
            self,
            double: float,
            double2: float,
            double3: float,
            string: typing.Union[java.lang.String, str],
            double4: float,
            double5: float,
            double6: float,
            double7: float,
            double8: float,
            double9: float,
            double10: float,
        ): ...
        def getBackPressureCorrectionFactor(self) -> float: ...
        def getBackPressureFraction(self) -> float: ...
        def getCombinationCorrectionFactor(self) -> float: ...
        def getDischargeCoefficient(self) -> float: ...
        def getMassFlowCapacity(self) -> float: ...
        def getOverpressureFraction(self) -> float: ...
        def getRecommendedOrifice(self) -> java.lang.String: ...
        def getRequiredArea(self) -> float: ...
        def getRequiredAreaIn2(self) -> float: ...
        def getSelectedArea(self) -> float: ...
        def getSelectedAreaIn2(self) -> float: ...

class SeparatorFireExposure:
    @staticmethod
    def applyFireHeating(
        separator: jneqsim.process.equipment.separator.Separator,
        fireExposureResult: "SeparatorFireExposure.FireExposureResult",
        double: float,
    ) -> float: ...
    @typing.overload
    @staticmethod
    def evaluate(
        separator: jneqsim.process.equipment.separator.Separator,
        fireScenarioConfig: "SeparatorFireExposure.FireScenarioConfig",
    ) -> "SeparatorFireExposure.FireExposureResult": ...
    @typing.overload
    @staticmethod
    def evaluate(
        separator: jneqsim.process.equipment.separator.Separator,
        fireScenarioConfig: "SeparatorFireExposure.FireScenarioConfig",
        flare: jneqsim.process.equipment.flare.Flare,
        double: float,
    ) -> "SeparatorFireExposure.FireExposureResult": ...

    class FireExposureResult:
        def __init__(
            self,
            double: float,
            double2: float,
            double3: float,
            double4: float,
            double5: float,
            double6: float,
            double7: float,
            double8: float,
            surfaceTemperatureResult: FireHeatTransferCalculator.SurfaceTemperatureResult,
            surfaceTemperatureResult2: FireHeatTransferCalculator.SurfaceTemperatureResult,
            double9: float,
            double10: float,
            boolean: bool,
        ): ...
        def flareRadiativeFlux(self) -> float: ...
        def flareRadiativeHeat(self) -> float: ...
        def isRuptureLikely(self) -> bool: ...
        def poolFireHeatLoad(self) -> float: ...
        def radiativeHeatFlux(self) -> float: ...
        def ruptureMarginPa(self) -> float: ...
        def totalFireHeat(self) -> float: ...
        def unwettedArea(self) -> float: ...
        def unwettedRadiativeHeat(self) -> float: ...
        def unwettedWall(
            self,
        ) -> FireHeatTransferCalculator.SurfaceTemperatureResult: ...
        def vonMisesStressPa(self) -> float: ...
        def wettedArea(self) -> float: ...
        def wettedWall(self) -> FireHeatTransferCalculator.SurfaceTemperatureResult: ...

    class FireScenarioConfig:
        def __init__(self): ...
        def allowableTensileStrengthPa(self) -> float: ...
        def emissivity(self) -> float: ...
        def environmentalFactor(self) -> float: ...
        def externalFilmCoefficientWPerM2K(self) -> float: ...
        def fireTemperatureK(self) -> float: ...
        def setAllowableTensileStrengthPa(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setEmissivity(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setEnvironmentalFactor(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setExternalFilmCoefficientWPerM2K(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setFireTemperatureK(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setThermalConductivityWPerMPerK(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setUnwettedInternalFilmCoefficientWPerM2K(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setViewFactor(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setWallThicknessM(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def setWettedInternalFilmCoefficientWPerM2K(
            self, double: float
        ) -> "SeparatorFireExposure.FireScenarioConfig": ...
        def thermalConductivityWPerMPerK(self) -> float: ...
        def unwettedInternalFilmCoefficientWPerM2K(self) -> float: ...
        def viewFactor(self) -> float: ...
        def wallThicknessM(self) -> float: ...
        def wettedInternalFilmCoefficientWPerM2K(self) -> float: ...

class TransientWallHeatTransfer:
    @typing.overload
    def __init__(
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
        int: int,
    ): ...
    @typing.overload
    def __init__(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        int: int,
    ): ...
    def advanceTimeStep(
        self,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
    ) -> None: ...
    def getHeatAbsorbed(self, double: float, double2: float) -> float: ...
    def getHeatFlux(self) -> float: ...
    def getInnerWallTemperature(self) -> float: ...
    def getMaxStableTimeStep(self) -> float: ...
    def getMeanWallTemperature(self) -> float: ...
    def getNodeSpacing(self) -> float: ...
    def getNumNodes(self) -> int: ...
    def getOuterWallTemperature(self) -> float: ...
    def getPositionArray(self) -> typing.MutableSequence[float]: ...
    def getTemperatureProfile(self) -> typing.MutableSequence[float]: ...
    def getTotalThickness(self) -> float: ...
    def resetTemperature(self, double: float) -> None: ...

class VesselHeatTransferCalculator:
    GRAVITY: typing.ClassVar[float] = ...
    @staticmethod
    def calculateCompleteHeatTransfer(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        boolean: bool,
    ) -> "VesselHeatTransferCalculator.HeatTransferResult": ...
    @staticmethod
    def calculateGrashofNumber(
        double: float, double2: float, double3: float, double4: float, double5: float
    ) -> float: ...
    @staticmethod
    def calculateInternalFilmCoefficient(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        boolean: bool,
    ) -> float: ...
    @staticmethod
    def calculateMixedConvectionCoefficient(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        double9: float,
        boolean: bool,
    ) -> float: ...
    @staticmethod
    def calculateNucleateBoilingHeatFlux(
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
    @staticmethod
    def calculateNusseltForcedConvection(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateNusseltHorizontalCylinder(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateNusseltVerticalSurface(double: float, double2: float) -> float: ...
    @staticmethod
    def calculatePrandtlNumber(
        double: float, double2: float, double3: float
    ) -> float: ...
    @staticmethod
    def calculateRayleighNumber(double: float, double2: float) -> float: ...
    @staticmethod
    def calculateReynoldsNumber(
        double: float, double2: float, double3: float, double4: float
    ) -> float: ...
    @staticmethod
    def calculateWettedWallFilmCoefficient(
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        double8: float,
        boolean: bool,
    ) -> float: ...

    class HeatTransferResult:
        def __init__(
            self,
            double: float,
            double2: float,
            double3: float,
            double4: float,
            double5: float,
            double6: float,
        ): ...
        def getFilmCoefficient(self) -> float: ...
        def getGrashofNumber(self) -> float: ...
        def getHeatFlux(self) -> float: ...
        def getNusseltNumber(self) -> float: ...
        def getPrandtlNumber(self) -> float: ...
        def getRayleighNumber(self) -> float: ...

class VesselRuptureCalculator:
    @staticmethod
    def isRuptureLikely(double: float, double2: float) -> bool: ...
    @staticmethod
    def ruptureMargin(double: float, double2: float) -> float: ...
    @staticmethod
    def vonMisesStress(double: float, double2: float, double3: float) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.util.fire")``.

    FireHeatLoadCalculator: typing.Type[FireHeatLoadCalculator]
    FireHeatTransferCalculator: typing.Type[FireHeatTransferCalculator]
    ReliefValveSizing: typing.Type[ReliefValveSizing]
    SeparatorFireExposure: typing.Type[SeparatorFireExposure]
    TransientWallHeatTransfer: typing.Type[TransientWallHeatTransfer]
    VesselHeatTransferCalculator: typing.Type[VesselHeatTransferCalculator]
    VesselRuptureCalculator: typing.Type[VesselRuptureCalculator]
