import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.statistics.experimentalsamplecreation.samplecreator
import typing

class WettedWallColumnSampleCreator(
    jneqsim.statistics.experimentalsamplecreation.samplecreator.SampleCreator
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    def calcdPdt(self) -> None: ...
    @staticmethod
    def main(
        stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]
    ) -> None: ...
    def setSampleValues(self) -> None: ...
    def smoothData(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.statistics.experimentalsamplecreation.samplecreator.wettedwallcolumnsamplecreator")``.

    WettedWallColumnSampleCreator: typing.Type[WettedWallColumnSampleCreator]
