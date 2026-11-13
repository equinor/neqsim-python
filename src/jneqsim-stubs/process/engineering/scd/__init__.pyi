
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.nio.file
import java.util
import jpype.protocol
import jneqsim.process.engineering
import jneqsim.process.engineering.pid
import jneqsim.process.processmodel.dexpi
import typing



class ScdDesignModel(java.io.Serializable):
    def __init__(self, engineeringProject: jneqsim.process.engineering.EngineeringProject, pidDesignModel: jneqsim.process.engineering.pid.PidDesignModel, pidSimulationBindings: jneqsim.process.engineering.pid.PidSimulationBindings, string: typing.Union[java.lang.String, str], engineeringStandard: jneqsim.process.engineering.EngineeringStandard): ...
    def assertCurrent(self, engineeringProject: jneqsim.process.engineering.EngineeringProject, pidDesignModel: jneqsim.process.engineering.pid.PidDesignModel, pidSimulationBindings: jneqsim.process.engineering.pid.PidSimulationBindings) -> None: ...
    @staticmethod
    def attribute(pidElement: jneqsim.process.engineering.pid.PidElement, string: typing.Union[java.lang.String, str]) -> java.lang.String: ...
    def getBlocks(self) -> java.util.List[jneqsim.process.engineering.pid.PidElement]: ...
    def getDrawingNumber(self) -> java.lang.String: ...
    def getRevision(self) -> java.lang.String: ...
    def getSignals(self) -> java.util.List[java.util.Map[java.lang.String, java.lang.String]]: ...
    def getStandard(self) -> jneqsim.process.engineering.EngineeringStandard: ...
    @staticmethod
    def template(pidElement: jneqsim.process.engineering.pid.PidElement) -> java.lang.String: ...
    def toJson(self) -> java.lang.String: ...
    def toMap(self) -> java.util.Map[java.lang.String, typing.Any]: ...

class ScdPackageExporter:
    @staticmethod
    def export(engineeringProject: jneqsim.process.engineering.EngineeringProject, pidDesignModel: jneqsim.process.engineering.pid.PidDesignModel, pidSimulationBindings: jneqsim.process.engineering.pid.PidSimulationBindings, scdDesignModel: ScdDesignModel, dexpi20PlantExportMetadata: jneqsim.process.processmodel.dexpi.Dexpi20PlantExportMetadata, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> java.nio.file.Path: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.engineering.scd")``.

    ScdDesignModel: typing.Type[ScdDesignModel]
    ScdPackageExporter: typing.Type[ScdPackageExporter]
