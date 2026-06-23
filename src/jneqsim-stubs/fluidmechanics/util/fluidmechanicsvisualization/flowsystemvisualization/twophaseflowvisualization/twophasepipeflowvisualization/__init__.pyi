import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization
import typing

class TwoPhasePipeFlowVisualization(
    jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization.TwoPhaseFlowVisualization
):
    bulkComposition: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    interfaceComposition: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    effectiveMassTransferCoefficient: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    molarFlux: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    schmidtNumber: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    totalMolarMassTransferRate: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    totalVolumetricMassTransferRate: typing.MutableSequence[
        typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]
    ] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def displayResult(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def setPoints(self) -> None: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.util.fluidmechanicsvisualization.flowsystemvisualization.twophaseflowvisualization.twophasepipeflowvisualization")``.

    TwoPhasePipeFlowVisualization: typing.Type[TwoPhasePipeFlowVisualization]
