import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import jneqsim.thermo.system
import typing

class EclipseFluidReadWrite:
    pseudoName: typing.ClassVar[java.lang.String] = ...
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def read(
        string: typing.Union[java.lang.String, str]
    ) -> jneqsim.thermo.system.SystemInterface: ...
    @typing.overload
    @staticmethod
    def read(
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> jneqsim.thermo.system.SystemInterface: ...
    @typing.overload
    @staticmethod
    def read(
        string: typing.Union[java.lang.String, str],
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray],
    ) -> jneqsim.thermo.system.SystemInterface: ...
    @staticmethod
    def readE300File(
        string: typing.Union[java.lang.String, str]
    ) -> jneqsim.thermo.system.SystemInterface: ...
    @typing.overload
    @staticmethod
    def setComposition(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        string: typing.Union[java.lang.String, str],
    ) -> None: ...
    @typing.overload
    @staticmethod
    def setComposition(
        systemInterface: jneqsim.thermo.system.SystemInterface,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> None: ...

class TablePrinter(java.io.Serializable):
    def __init__(self): ...
    @staticmethod
    def convertDoubleToString(
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ]
    ) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    @typing.overload
    @staticmethod
    def printTable(
        doubleArray: typing.Union[
            typing.List[typing.MutableSequence[float]], jpype.JArray
        ]
    ) -> None: ...
    @typing.overload
    @staticmethod
    def printTable(
        stringArray: typing.Union[
            typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray
        ]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.readwrite")``.

    EclipseFluidReadWrite: typing.Type[EclipseFluidReadWrite]
    TablePrinter: typing.Type[TablePrinter]
