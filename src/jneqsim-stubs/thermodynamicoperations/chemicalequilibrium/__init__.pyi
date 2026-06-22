
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.thermo.system
import jneqsim.thermodynamicoperations
import org.jfree.chart
import typing



class ChemicalEquilibrium(jneqsim.thermodynamicoperations.BaseOperation):
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface): ...
    def displayResult(self) -> None: ...
    def getJFreeChart(self, string: typing.Union[java.lang.String, str]) -> org.jfree.chart.JFreeChart: ...
    def getPoints(self, int: int) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getResultTable(self) -> typing.MutableSequence[typing.MutableSequence[java.lang.String]]: ...
    def printToFile(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def run(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermodynamicoperations.chemicalequilibrium")``.

    ChemicalEquilibrium: typing.Type[ChemicalEquilibrium]
