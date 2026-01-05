import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.process.equipment.stream
import jneqsim.process.measurementdevice
import jneqsim.thermo.system
import typing

class FluidSevereSlug:
    def getGasConstant(self) -> float: ...
    def getLiqDensity(self) -> float: ...
    def getMolecularWeight(self) -> float: ...
    def getliqVisc(self) -> float: ...
    def setLiqDensity(self, double: float) -> None: ...
    def setLiqVisc(self, double: float) -> None: ...
    def setMolecularWeight(self, double: float) -> None: ...

class Pipe:
    def getAngle(self, string: typing.Union[java.lang.String, str]) -> float: ...
    def getArea(self) -> float: ...
    def getInternalDiameter(self) -> float: ...
    def getLeftLength(self) -> float: ...
    def getName(self) -> java.lang.String: ...
    def getRightLength(self) -> float: ...
    def setAngle(self, double: float) -> None: ...
    def setInternalDiameter(self, double: float) -> None: ...
    def setLeftLength(self, double: float) -> None: ...
    def setName(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setRightLength(self, double: float) -> None: ...

class SevereSlugAnalyser(jneqsim.process.measurementdevice.MeasurementDeviceBaseClass):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(
        self, string: typing.Union[java.lang.String, str], double: float, double2: float
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        double2: float,
        double3: float,
        int: int,
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        stream: jneqsim.process.equipment.stream.Stream,
        double: float,
        double2: float,
        double3: float,
        double4: float,
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        stream: jneqsim.process.equipment.stream.Stream,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        double6: float,
        double7: float,
        int: int,
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        stream: jneqsim.process.equipment.stream.Stream,
        double: float,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
        int: int,
    ): ...
    @typing.overload
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        systemInterface: jneqsim.thermo.system.SystemInterface,
        pipe: Pipe,
        double: float,
        double2: float,
        double3: float,
        int: int,
    ): ...
    def checkFlowRegime(
        self,
        fluidSevereSlug: FluidSevereSlug,
        pipe: Pipe,
        severeSlugAnalyser: "SevereSlugAnalyser",
    ) -> java.lang.String: ...
    def gasConst(self, fluidSevereSlug: FluidSevereSlug) -> float: ...
    def getFlowPattern(self) -> java.lang.String: ...
    @typing.overload
    def getMeasuredValue(self) -> float: ...
    @typing.overload
    def getMeasuredValue(
        self, string: typing.Union[java.lang.String, str]
    ) -> float: ...
    @typing.overload
    def getMeasuredValue(
        self,
        fluidSevereSlug: FluidSevereSlug,
        pipe: Pipe,
        severeSlugAnalyser: "SevereSlugAnalyser",
    ) -> float: ...
    def getNumberOfTimeSteps(self) -> int: ...
    def getOutletPressure(self) -> float: ...
    @typing.overload
    def getPredictedFlowRegime(self) -> java.lang.String: ...
    @typing.overload
    def getPredictedFlowRegime(
        self,
        fluidSevereSlug: FluidSevereSlug,
        pipe: Pipe,
        severeSlugAnalyser: "SevereSlugAnalyser",
    ) -> java.lang.String: ...
    def getSimulationTime(self) -> float: ...
    def getSlugValue(self) -> float: ...
    def getSuperficialGasVelocity(self) -> float: ...
    def getSuperficialLiquidVelocity(self) -> float: ...
    def getTemperature(self) -> float: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def runSevereSlug(
        self,
        fluidSevereSlug: FluidSevereSlug,
        pipe: Pipe,
        severeSlugAnalyser: "SevereSlugAnalyser",
    ) -> None: ...
    def setNumberOfTimeSteps(self, int: int) -> None: ...
    def setOutletPressure(self, double: float) -> None: ...
    def setSimulationTime(self, double: float) -> None: ...
    def setSuperficialGasVelocity(self, double: float) -> None: ...
    def setSuperficialLiquidVelocity(self, double: float) -> None: ...
    def setTemperature(self, double: float) -> None: ...
    def slugHoldUp(
        self, pipe: Pipe, severeSlugAnalyser: "SevereSlugAnalyser"
    ) -> float: ...
    def stratifiedHoldUp(
        self,
        fluidSevereSlug: FluidSevereSlug,
        pipe: Pipe,
        severeSlugAnalyser: "SevereSlugAnalyser",
    ) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.measurementdevice.simpleflowregime")``.

    FluidSevereSlug: typing.Type[FluidSevereSlug]
    Pipe: typing.Type[Pipe]
    SevereSlugAnalyser: typing.Type[SevereSlugAnalyser]
