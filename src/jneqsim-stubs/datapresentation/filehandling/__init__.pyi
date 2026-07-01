
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import typing



class TextFile(java.io.Serializable):
    def __init__(self): ...
    def createFile(self) -> None: ...
    def newFile(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setOutputFileName(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def setValues(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def setValues(self, stringArray: typing.Union[typing.List[typing.MutableSequence[java.lang.String]], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.datapresentation.filehandling")``.

    TextFile: typing.Type[TextFile]
