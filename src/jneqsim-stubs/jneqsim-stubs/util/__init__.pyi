import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.lang.annotation
import java.util.concurrent
import jneqsim.util.annotation
import jneqsim.util.database
import jneqsim.util.exception
import jneqsim.util.generator
import jneqsim.util.serialization
import jneqsim.util.unit
import jneqsim.util.util
import jneqsim.util.validation
import typing

class ExcludeFromJacocoGeneratedReport(java.lang.annotation.Annotation):
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> java.lang.String: ...

class NamedInterface:
    def getName(self) -> java.lang.String: ...
    def getTagName(self) -> java.lang.String: ...
    def setName(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setTagName(self, string: typing.Union[java.lang.String, str]) -> None: ...

class NeqSimLogging:
    def __init__(self): ...
    @staticmethod
    def resetAllLoggers() -> None: ...
    @staticmethod
    def setGlobalLogging(string: typing.Union[java.lang.String, str]) -> None: ...

class NeqSimThreadPool:
    @staticmethod
    def execute(
        runnable: typing.Union[java.lang.Runnable, typing.Callable]
    ) -> None: ...
    @staticmethod
    def getDefaultPoolSize() -> int: ...
    @staticmethod
    def getKeepAliveTimeSeconds() -> int: ...
    @staticmethod
    def getMaxQueueCapacity() -> int: ...
    @staticmethod
    def getPool() -> java.util.concurrent.ExecutorService: ...
    @staticmethod
    def getPoolSize() -> int: ...
    @staticmethod
    def isAllowCoreThreadTimeout() -> bool: ...
    @staticmethod
    def isShutdown() -> bool: ...
    @staticmethod
    def isTerminated() -> bool: ...
    _newCompletionService__T = typing.TypeVar("_newCompletionService__T")  # <T>
    @staticmethod
    def newCompletionService() -> (
        java.util.concurrent.CompletionService[_newCompletionService__T]
    ): ...
    @staticmethod
    def resetPoolSize() -> None: ...
    @staticmethod
    def setAllowCoreThreadTimeout(boolean: bool) -> None: ...
    @staticmethod
    def setKeepAliveTimeSeconds(long: int) -> None: ...
    @staticmethod
    def setMaxQueueCapacity(int: int) -> None: ...
    @staticmethod
    def setPoolSize(int: int) -> None: ...
    @staticmethod
    def shutdown() -> None: ...
    @staticmethod
    def shutdownAndAwait(
        long: int, timeUnit: java.util.concurrent.TimeUnit
    ) -> bool: ...
    @staticmethod
    def shutdownNow() -> None: ...
    _submit_1__T = typing.TypeVar("_submit_1__T")  # <T>
    @typing.overload
    @staticmethod
    def submit(
        runnable: typing.Union[java.lang.Runnable, typing.Callable]
    ) -> java.util.concurrent.Future[typing.Any]: ...
    @typing.overload
    @staticmethod
    def submit(
        callable: typing.Union[
            java.util.concurrent.Callable[_submit_1__T],
            typing.Callable[[], _submit_1__T],
        ]
    ) -> java.util.concurrent.Future[_submit_1__T]: ...

class NamedBaseClass(NamedInterface, java.io.Serializable):
    name: java.lang.String = ...
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    def getName(self) -> java.lang.String: ...
    def getTagName(self) -> java.lang.String: ...
    def setName(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setTagName(self, string: typing.Union[java.lang.String, str]) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.util")``.

    ExcludeFromJacocoGeneratedReport: typing.Type[ExcludeFromJacocoGeneratedReport]
    NamedBaseClass: typing.Type[NamedBaseClass]
    NamedInterface: typing.Type[NamedInterface]
    NeqSimLogging: typing.Type[NeqSimLogging]
    NeqSimThreadPool: typing.Type[NeqSimThreadPool]
    annotation: jneqsim.util.annotation.__module_protocol__
    database: jneqsim.util.database.__module_protocol__
    exception: jneqsim.util.exception.__module_protocol__
    generator: jneqsim.util.generator.__module_protocol__
    serialization: jneqsim.util.serialization.__module_protocol__
    unit: jneqsim.util.unit.__module_protocol__
    util: jneqsim.util.util.__module_protocol__
    validation: jneqsim.util.validation.__module_protocol__
