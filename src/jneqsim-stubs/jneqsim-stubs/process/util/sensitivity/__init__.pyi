import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.process.processmodel
import jneqsim.process.util.uncertainty
import typing

class ProcessSensitivityAnalyzer(java.io.Serializable):
    def __init__(self, processSystem: jneqsim.process.processmodel.ProcessSystem): ...
    def compute(self) -> jneqsim.process.util.uncertainty.SensitivityMatrix: ...
    def computeFiniteDifferencesOnly(
        self,
    ) -> jneqsim.process.util.uncertainty.SensitivityMatrix: ...
    def generateReport(
        self, sensitivityMatrix: jneqsim.process.util.uncertainty.SensitivityMatrix
    ) -> java.lang.String: ...
    def reset(self) -> "ProcessSensitivityAnalyzer": ...
    def withCentralDifferences(self, boolean: bool) -> "ProcessSensitivityAnalyzer": ...
    @typing.overload
    def withInput(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> "ProcessSensitivityAnalyzer": ...
    @typing.overload
    def withInput(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> "ProcessSensitivityAnalyzer": ...
    @typing.overload
    def withOutput(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
    ) -> "ProcessSensitivityAnalyzer": ...
    @typing.overload
    def withOutput(
        self,
        string: typing.Union[java.lang.String, str],
        string2: typing.Union[java.lang.String, str],
        string3: typing.Union[java.lang.String, str],
    ) -> "ProcessSensitivityAnalyzer": ...
    def withPerturbation(self, double: float) -> "ProcessSensitivityAnalyzer": ...

    class VariableSpec(java.io.Serializable):
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
        ): ...
        @typing.overload
        def __init__(
            self,
            string: typing.Union[java.lang.String, str],
            string2: typing.Union[java.lang.String, str],
            string3: typing.Union[java.lang.String, str],
        ): ...
        def getEquipmentName(self) -> java.lang.String: ...
        def getFullName(self) -> java.lang.String: ...
        def getPropertyName(self) -> java.lang.String: ...
        def getUnit(self) -> java.lang.String: ...
        def toString(self) -> java.lang.String: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.util.sensitivity")``.

    ProcessSensitivityAnalyzer: typing.Type[ProcessSensitivityAnalyzer]
