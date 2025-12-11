
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.awt.image
import java.lang
import javax.swing
import jpype
import org.jfree.chart
import org.jfree.data.category
import typing



class Graph2b(javax.swing.JFrame):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str], string4: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str], string4: typing.Union[java.lang.String, str]): ...
    def createCategoryDataSource(self) -> org.jfree.data.category.CategoryDataset: ...
    def getBufferedImage(self) -> java.awt.image.BufferedImage: ...
    def getChart(self) -> org.jfree.chart.JFreeChart: ...
    def getChartPanel(self) -> org.jfree.chart.ChartPanel: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...
    def saveFigure(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setChart(self, jFreeChart: org.jfree.chart.JFreeChart) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.datapresentation.jfreechart")``.

    Graph2b: typing.Type[Graph2b]
