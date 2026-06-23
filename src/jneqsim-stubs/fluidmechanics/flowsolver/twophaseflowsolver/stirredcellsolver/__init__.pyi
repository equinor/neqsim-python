import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver
import jneqsim.fluidmechanics.flowsystem
import jneqsim.thermo
import typing

class StirredCellSolver(
    jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver.TwoPhasePipeFlowSolver,
    jneqsim.thermo.ThermodynamicConstantsInterface,
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self,
        flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface,
        double: float,
        int: int,
    ): ...
    @typing.overload
    def __init__(
        self,
        flowSystemInterface: jneqsim.fluidmechanics.flowsystem.FlowSystemInterface,
        double: float,
        int: int,
        boolean: bool,
    ): ...
    def calcFluxes(self) -> None: ...
    def clone(
        self,
    ) -> (
        jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.twophasepipeflowsolver.TwoPhaseFixedStaggeredGridSolver
    ): ...
    def initComposition(self, int: int, int2: int) -> None: ...
    def initFinalResults(self, int: int) -> None: ...
    def initMatrix(self) -> None: ...
    def initNodes(self) -> None: ...
    def initPhaseFraction(self, int: int) -> None: ...
    def initPressure(self, int: int) -> None: ...
    def initProfiles(self) -> None: ...
    def initTemperature(self, int: int) -> None: ...
    def initVelocity(self, int: int) -> None: ...
    def solveTDMA(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flowsolver.twophaseflowsolver.stirredcellsolver")``.

    StirredCellSolver: typing.Type[StirredCellSolver]
