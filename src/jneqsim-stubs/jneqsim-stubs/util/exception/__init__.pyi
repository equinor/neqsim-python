
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import typing



class ThermoException(java.lang.Exception):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...

class InvalidInputException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str], string4: typing.Union[java.lang.String, str]): ...

class InvalidOutputException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str], string4: typing.Union[java.lang.String, str]): ...

class IsNaNException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...

class NotImplementedException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]): ...

class NotInitializedException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], string3: typing.Union[java.lang.String, str], string4: typing.Union[java.lang.String, str]): ...

class TooManyIterationsException(ThermoException):
    @typing.overload
    def __init__(self, object: typing.Any, string: typing.Union[java.lang.String, str], long: int): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str], long: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.util.exception")``.

    InvalidInputException: typing.Type[InvalidInputException]
    InvalidOutputException: typing.Type[InvalidOutputException]
    IsNaNException: typing.Type[IsNaNException]
    NotImplementedException: typing.Type[NotImplementedException]
    NotInitializedException: typing.Type[NotInitializedException]
    ThermoException: typing.Type[ThermoException]
    TooManyIterationsException: typing.Type[TooManyIterationsException]
