
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import typing



class TPflash_benchmark:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...

class TPflash_benchmark_UMR:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...

class TPflash_benchmark_fullcomp:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.benchmark")``.

    TPflash_benchmark: typing.Type[TPflash_benchmark]
    TPflash_benchmark_UMR: typing.Type[TPflash_benchmark_UMR]
    TPflash_benchmark_fullcomp: typing.Type[TPflash_benchmark_fullcomp]
