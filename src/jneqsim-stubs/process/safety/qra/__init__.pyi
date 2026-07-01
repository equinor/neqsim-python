import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jneqsim.process.safety.dispersion
import jneqsim.process.safety.fire
import jneqsim.process.safety.risk.eta
import typing

class ConsequenceAnalysisEngine(java.io.Serializable):
    def __init__(self, string: typing.Union[java.lang.String, str], double: float): ...
    def addJetFire(
        self,
        double: float,
        jetFireModel: jneqsim.process.safety.fire.JetFireModel,
        probitModel: jneqsim.process.safety.dispersion.ProbitModel,
        double2: float,
    ) -> "ConsequenceAnalysisEngine": ...
    def addOutcome(
        self,
        string: typing.Union[java.lang.String, str],
        double: float,
        consequence: typing.Union[
            "ConsequenceAnalysisEngine.Consequence", typing.Callable
        ],
    ) -> "ConsequenceAnalysisEngine": ...
    def addPoolFire(
        self,
        double: float,
        poolFireModel: jneqsim.process.safety.fire.PoolFireModel,
        probitModel: jneqsim.process.safety.dispersion.ProbitModel,
        double2: float,
    ) -> "ConsequenceAnalysisEngine": ...
    def addToxicDispersion(
        self,
        double: float,
        gaussianPlume: jneqsim.process.safety.dispersion.GaussianPlume,
        probitModel: jneqsim.process.safety.dispersion.ProbitModel,
        double2: float,
        double3: float,
        double4: float,
        double5: float,
    ) -> "ConsequenceAnalysisEngine": ...
    def addVCE(
        self,
        double: float,
        vCEModel: jneqsim.process.safety.fire.VCEModel,
        probitModel: jneqsim.process.safety.dispersion.ProbitModel,
    ) -> "ConsequenceAnalysisEngine": ...
    def evaluate(
        self, double: float
    ) -> java.util.List["ConsequenceAnalysisEngine.OutcomeResult"]: ...
    def individualFatalityRiskPerYear(self, double: float) -> float: ...
    def report(self, double: float) -> java.lang.String: ...
    def toEventTree(self) -> jneqsim.process.safety.risk.eta.EventTreeAnalyzer: ...

    class Consequence(java.io.Serializable):
        def fatalityProbabilityAt(self, double: float) -> float: ...

    class OutcomeResult(java.io.Serializable):
        outcomeName: java.lang.String = ...
        outcomeFrequencyPerYear: float = ...
        fatalityProbability: float = ...
        fatalityFrequencyPerYear: float = ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.qra")``.

    ConsequenceAnalysisEngine: typing.Type[ConsequenceAnalysisEngine]
