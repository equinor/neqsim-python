
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.process.processmodel
import typing



class ConditionMonitor(java.io.Serializable, java.lang.Runnable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, processSystem: jneqsim.process.processmodel.ProcessSystem): ...
    @typing.overload
    def conditionAnalysis(self) -> None: ...
    @typing.overload
    def conditionAnalysis(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def getProcess(self) -> jneqsim.process.processmodel.ProcessSystem: ...
    def getReport(self) -> java.lang.String: ...
    def run(self) -> None: ...

class ConditionMonitorSpecifications(java.io.Serializable):
    HXmaxDeltaT: typing.ClassVar[float] = ...
    HXmaxDeltaT_ErrorMsg: typing.ClassVar[java.lang.String] = ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.conditionmonitor")``.

    ConditionMonitor: typing.Type[ConditionMonitor]
    ConditionMonitorSpecifications: typing.Type[ConditionMonitorSpecifications]
