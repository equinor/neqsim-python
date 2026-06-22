
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.process.fielddevelopment.concept
import jneqsim.process.fielddevelopment.economics
import jneqsim.process.fielddevelopment.evaluation
import jneqsim.process.fielddevelopment.tieback
import typing



class FieldDevelopmentReportExporter:
    def __init__(self): ...
    def exportConceptKpisMarkdown(self, list: java.util.List[jneqsim.process.fielddevelopment.evaluation.ConceptKPIs]) -> java.lang.String: ...
    def exportTemplateComparisonMarkdown(self, list: java.util.List[jneqsim.process.fielddevelopment.concept.DevelopmentCaseTemplate]) -> java.lang.String: ...
    def exportTemplateNpvFigureData(self, list: java.util.List[jneqsim.process.fielddevelopment.concept.DevelopmentCaseTemplate]) -> java.util.List[typing.MutableSequence[java.lang.String]]: ...
    def exportTiebackOptionsMarkdown(self, tiebackReport: jneqsim.process.fielddevelopment.tieback.TiebackReport) -> java.lang.String: ...
    def exportTornadoMarkdown(self, tornadoResult: jneqsim.process.fielddevelopment.economics.SensitivityAnalyzer.TornadoResult) -> java.lang.String: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.fielddevelopment.reporting")``.

    FieldDevelopmentReportExporter: typing.Type[FieldDevelopmentReportExporter]
