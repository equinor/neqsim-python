import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing

class CompositionEstimation:
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def estimateH2Sconcentration(self) -> float: ...
    @typing.overload
    def estimateH2Sconcentration(self, double: float) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.pvtsimulation.reservoirproperties")``.

    CompositionEstimation: typing.Type[CompositionEstimation]
