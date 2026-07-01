
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import typing



class EscalationGraphAnalyzer(java.io.Serializable):
    def __init__(self): ...
    def addExposure(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], double: float) -> 'EscalationGraphAnalyzer': ...
    def addItem(self, string: typing.Union[java.lang.String, str], double: float) -> 'EscalationGraphAnalyzer': ...
    def getItems(self) -> java.util.Set[java.lang.String]: ...
    def propagate(self, string: typing.Union[java.lang.String, str]) -> java.util.Set[java.lang.String]: ...
    def worstCaseEscalation(self) -> java.util.Set[java.lang.String]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.escalation")``.

    EscalationGraphAnalyzer: typing.Type[EscalationGraphAnalyzer]
