
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.nio.file
import java.util
import jpype.protocol
import neqsim.process.mechanicaldesign
import typing



class MechanicalDesignDataSource:
    def getDesignLimits(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]) -> java.util.Optional[neqsim.process.mechanicaldesign.DesignLimitData]: ...

class CsvMechanicalDesignDataSource(MechanicalDesignDataSource):
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]): ...
    def getDesignLimits(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]) -> java.util.Optional[neqsim.process.mechanicaldesign.DesignLimitData]: ...

class DatabaseMechanicalDesignDataSource(MechanicalDesignDataSource):
    def __init__(self): ...
    def getDesignLimits(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]) -> java.util.Optional[neqsim.process.mechanicaldesign.DesignLimitData]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.mechanicaldesign.data")``.

    CsvMechanicalDesignDataSource: typing.Type[CsvMechanicalDesignDataSource]
    DatabaseMechanicalDesignDataSource: typing.Type[DatabaseMechanicalDesignDataSource]
    MechanicalDesignDataSource: typing.Type[MechanicalDesignDataSource]
