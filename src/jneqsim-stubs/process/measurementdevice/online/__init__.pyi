import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import typing

class OnlineSignal(java.io.Serializable):
    def __init__(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ): ...
    def connect(self) -> bool: ...
    def getTimeStamp(self) -> java.util.Date: ...
    def getUnit(self) -> java.lang.String: ...
    def getValue(self) -> float: ...
    def setUnit(self, string: typing.Union[java.lang.String, str]) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.measurementdevice.online")``.

    OnlineSignal: typing.Type[OnlineSignal]
