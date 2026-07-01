import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.nio.file
import java.util
import jpype
import jpype.protocol
import jneqsim.blackoil
import jneqsim.thermo.system
import typing

class CMGEOSExporter:
    @typing.overload
    @staticmethod
    def toFile(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        exportConfig: "CMGEOSExporter.ExportConfig",
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        exportConfig: "CMGEOSExporter.ExportConfig",
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        simulator: "CMGEOSExporter.Simulator",
    ) -> None: ...
    @typing.overload
    def toString(self) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        exportConfig: "CMGEOSExporter.ExportConfig",
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        systemInterface: jneqsim.thermo.system.SystemInterface,
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        exportConfig: "CMGEOSExporter.ExportConfig",
    ) -> java.lang.String: ...

    class ExportConfig:
        def __init__(self): ...
        def setComment(
            self, string: typing.Union[java.lang.String, str]
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setIncludeHeader(self, boolean: bool) -> "CMGEOSExporter.ExportConfig": ...
        def setModelName(
            self, string: typing.Union[java.lang.String, str]
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setPressureGrid(
            self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setReferenceTemperature(
            self, double: float
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setSimulator(
            self, simulator: "CMGEOSExporter.Simulator"
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setStandardConditions(
            self, double: float, double2: float
        ) -> "CMGEOSExporter.ExportConfig": ...
        def setUnits(
            self, units: "CMGEOSExporter.Units"
        ) -> "CMGEOSExporter.ExportConfig": ...

    class Simulator(java.lang.Enum["CMGEOSExporter.Simulator"]):
        IMEX: typing.ClassVar["CMGEOSExporter.Simulator"] = ...
        GEM: typing.ClassVar["CMGEOSExporter.Simulator"] = ...
        STARS: typing.ClassVar["CMGEOSExporter.Simulator"] = ...
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
        ) -> "CMGEOSExporter.Simulator": ...
        @staticmethod
        def values() -> typing.MutableSequence["CMGEOSExporter.Simulator"]: ...

    class Units(java.lang.Enum["CMGEOSExporter.Units"]):
        SI: typing.ClassVar["CMGEOSExporter.Units"] = ...
        FIELD: typing.ClassVar["CMGEOSExporter.Units"] = ...
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
        ) -> "CMGEOSExporter.Units": ...
        @staticmethod
        def values() -> typing.MutableSequence["CMGEOSExporter.Units"]: ...

class EclipseBlackOilImporter:
    def __init__(self): ...
    @staticmethod
    def fromFile(
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]
    ) -> "EclipseBlackOilImporter.Result": ...
    @staticmethod
    def fromReader(reader: java.io.Reader) -> "EclipseBlackOilImporter.Result": ...

    class Result:
        pvt: jneqsim.blackoil.BlackOilPVTTable = ...
        system: jneqsim.blackoil.SystemBlackOil = ...
        rho_o_sc: float = ...
        rho_w_sc: float = ...
        rho_g_sc: float = ...
        bubblePoint: float = ...
        log: java.util.List = ...
        def __init__(self): ...

    class Units(java.lang.Enum["EclipseBlackOilImporter.Units"]):
        METRIC: typing.ClassVar["EclipseBlackOilImporter.Units"] = ...
        FIELD: typing.ClassVar["EclipseBlackOilImporter.Units"] = ...
        LAB: typing.ClassVar["EclipseBlackOilImporter.Units"] = ...
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
        ) -> "EclipseBlackOilImporter.Units": ...
        @staticmethod
        def values() -> typing.MutableSequence["EclipseBlackOilImporter.Units"]: ...

class EclipseEOSExporter:
    @typing.overload
    @staticmethod
    def toFile(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        exportConfig: "EclipseEOSExporter.ExportConfig",
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
    ) -> None: ...
    @typing.overload
    @staticmethod
    def toFile(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath],
        exportConfig: "EclipseEOSExporter.ExportConfig",
    ) -> None: ...
    @typing.overload
    def toString(self) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        blackOilPVTTable: jneqsim.blackoil.BlackOilPVTTable,
        double: float,
        double2: float,
        double3: float,
        exportConfig: "EclipseEOSExporter.ExportConfig",
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        systemInterface: jneqsim.thermo.system.SystemInterface,
    ) -> java.lang.String: ...
    @typing.overload
    @staticmethod
    def toString(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        exportConfig: "EclipseEOSExporter.ExportConfig",
    ) -> java.lang.String: ...

    class ExportConfig:
        def __init__(self): ...
        def setComment(
            self, string: typing.Union[java.lang.String, str]
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setIncludeDensity(
            self, boolean: bool
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setIncludeHeader(
            self, boolean: bool
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setIncludePVTG(
            self, boolean: bool
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setIncludePVTO(
            self, boolean: bool
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setIncludePVTW(
            self, boolean: bool
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setPressureGrid(
            self, doubleArray: typing.Union[typing.List[float], jpype.JArray]
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setReferenceTemperature(
            self, double: float
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setStandardConditions(
            self, double: float, double2: float
        ) -> "EclipseEOSExporter.ExportConfig": ...
        def setUnits(
            self, units: "EclipseEOSExporter.Units"
        ) -> "EclipseEOSExporter.ExportConfig": ...

    class Units(java.lang.Enum["EclipseEOSExporter.Units"]):
        METRIC: typing.ClassVar["EclipseEOSExporter.Units"] = ...
        FIELD: typing.ClassVar["EclipseEOSExporter.Units"] = ...
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
        ) -> "EclipseEOSExporter.Units": ...
        @staticmethod
        def values() -> typing.MutableSequence["EclipseEOSExporter.Units"]: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.blackoil.io")``.

    CMGEOSExporter: typing.Type[CMGEOSExporter]
    EclipseBlackOilImporter: typing.Type[EclipseBlackOilImporter]
    EclipseEOSExporter: typing.Type[EclipseEOSExporter]
