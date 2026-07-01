import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import typing

class RiskFrameworkQuickStart:
    def __init__(self): ...
    @staticmethod
    def exampleBowTieAnalysis() -> None: ...
    @staticmethod
    def exampleConditionBasedReliability() -> None: ...
    @staticmethod
    def exampleDynamicSimulation() -> None: ...
    @staticmethod
    def exampleMLIntegration() -> None: ...
    @staticmethod
    def exampleOperationalRiskSimulation() -> None: ...
    @staticmethod
    def examplePortfolioRisk() -> None: ...
    @staticmethod
    def exampleRealTimeMonitoring() -> None: ...
    @staticmethod
    def exampleSISIntegration() -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.safety.risk.examples")``.

    RiskFrameworkQuickStart: typing.Type[RiskFrameworkQuickStart]
