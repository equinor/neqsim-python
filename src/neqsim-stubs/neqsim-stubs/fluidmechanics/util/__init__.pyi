
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import neqsim.fluidmechanics.util.fluidmechanicsvisualization
import neqsim.fluidmechanics.util.timeseries
import typing



class FrictionFactorCalculator:
    RE_LAMINAR_LIMIT: typing.ClassVar[float] = ...
    RE_TURBULENT_LIMIT: typing.ClassVar[float] = ...
    @staticmethod
    def calcDarcyFrictionFactor(double: float, double2: float) -> float: ...
    @staticmethod
    def calcFanningFrictionFactor(double: float, double2: float) -> float: ...
    @staticmethod
    def calcHaalandFrictionFactor(double: float, double2: float) -> float: ...
    @staticmethod
    def calcPressureDropPerLength(double: float, double2: float, double3: float, double4: float) -> float: ...
    @staticmethod
    def getFlowRegime(double: float) -> java.lang.String: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.util")``.

    FrictionFactorCalculator: typing.Type[FrictionFactorCalculator]
    fluidmechanicsvisualization: neqsim.fluidmechanics.util.fluidmechanicsvisualization.__module_protocol__
    timeseries: neqsim.fluidmechanics.util.timeseries.__module_protocol__
