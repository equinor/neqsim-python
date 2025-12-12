import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import jpype
import jneqsim.fluidmechanics.flowsystem
import jneqsim.thermo.system
import typing

class TimeSeries(java.io.Serializable):
    def __init__(self): ...
    def getOutletMolarFlowRates(self) -> typing.MutableSequence[float]: ...
    def getThermoSystem(
        self,
    ) -> typing.MutableSequence[jneqsim.thermo.system.SystemInterface]: ...
    @typing.overload
    def getTime(self, int: int) -> float: ...
    @typing.overload
    def getTime(self) -> typing.MutableSequence[float]: ...
    def getTimeStep(self) -> typing.MutableSequence[float]: ...
    def init(
        self, flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface
    ) -> None: ...
    def setInletThermoSystems(
        self,
        systemInterfaceArray: typing.Union[
            typing.List[jneqsim.thermo.system.SystemInterface], jpype.JArray
        ],
    ) -> None: ...
    def setNumberOfTimeStepsInInterval(self, int: int) -> None: ...
    def setOutletMolarFlowRate(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...
    def setTimes(
        self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.util.timeseries")``.

    TimeSeries: typing.Type[TimeSeries]
