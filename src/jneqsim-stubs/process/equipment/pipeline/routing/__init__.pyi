import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jneqsim.process.equipment.pipeline
import jneqsim.process.equipment.stream
import jneqsim.process.processmodel
import typing

class PipingRouteBuilder(java.io.Serializable):
    def __init__(self): ...
    def addMinorLoss(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        double: float,
    ) -> "PipingRouteBuilder": ...
    @typing.overload
    def addSegment(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        double: float,
        string3: typing.Union[java.lang.String, str],
        double2: float,
        string4: typing.Union[java.lang.String, str],
    ) -> "PipingRouteBuilder": ...
    @typing.overload
    def addSegment(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
        double: float,
        string4: typing.Union[java.lang.String, str],
        double2: float,
        string5: typing.Union[java.lang.String, str],
    ) -> "PipingRouteBuilder": ...
    @typing.overload
    def addToProcessSystem(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    @typing.overload
    def addToProcessSystem(
        self,
        processSystem: jneqsim.process.processmodel.ProcessSystem,
        streamInterface: jneqsim.process.equipment.stream.StreamInterface,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> jneqsim.process.equipment.stream.StreamInterface: ...
    def build(
        self, streamInterface: jneqsim.process.equipment.stream.StreamInterface
    ) -> jneqsim.process.processmodel.ProcessSystem: ...
    def getSegment(
        self, string: typing.Union[java.lang.String, str]
    ) -> "PipingRouteBuilder.RouteSegment": ...
    def getSegments(self) -> java.util.List["PipingRouteBuilder.RouteSegment"]: ...
    def setDefaultHeatTransferMode(
        self,
        heatTransferMode: jneqsim.process.equipment.pipeline.PipeBeggsAndBrills.HeatTransferMode,
    ) -> "PipingRouteBuilder": ...
    def setDefaultNumberOfIncrements(self, int: int) -> "PipingRouteBuilder": ...
    def setDefaultPipeWallRoughness(
        self, double: float, string: typing.Union[java.lang.String, str]
    ) -> "PipingRouteBuilder": ...
    def setMinorLossFrictionFactor(self, double: float) -> "PipingRouteBuilder": ...
    def setSegmentElevationChange(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        string2: typing.Union[java.lang.String, str],
    ) -> "PipingRouteBuilder": ...
    def setSegmentPipeWallRoughness(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        string2: typing.Union[java.lang.String, str],
    ) -> "PipingRouteBuilder": ...
    def setSegmentWallThickness(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        string2: typing.Union[java.lang.String, str],
    ) -> "PipingRouteBuilder": ...
    def toJson(self) -> java.lang.String: ...

    class MinorLoss(java.io.Serializable):
        def getEquivalentLengthRatio(self) -> float: ...
        def getFittingType(self) -> java.lang.String: ...
        def getKValue(self) -> float: ...

    class RouteSegment(java.io.Serializable):
        def getElevationChangeMeters(self) -> float: ...
        def getFromNode(self) -> java.lang.String: ...
        def getLengthMeters(self) -> float: ...
        def getMinorLosses(self) -> java.util.List["PipingRouteBuilder.MinorLoss"]: ...
        def getNominalDiameterMeters(self) -> float: ...
        def getPipeName(self) -> java.lang.String: ...
        def getPipeWallRoughnessMeters(self) -> float: ...
        def getSegmentId(self) -> java.lang.String: ...
        def getToNode(self) -> java.lang.String: ...
        def getTotalEquivalentLengthRatio(self) -> float: ...
        def getTotalKValue(self) -> float: ...
        def getWallThicknessMeters(self) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.pipeline.routing")``.

    PipingRouteBuilder: typing.Type[PipingRouteBuilder]
