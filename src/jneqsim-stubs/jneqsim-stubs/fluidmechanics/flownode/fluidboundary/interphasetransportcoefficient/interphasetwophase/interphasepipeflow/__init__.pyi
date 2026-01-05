import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase
import jneqsim.thermo
import typing

class InterphaseTwoPhasePipeFlow(
    jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.InterphaseTwoPhase
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    def calcHeatTransferCoefficientFromNusselt(
        self, double: float, double2: float, double3: float
    ) -> float: ...
    def calcMassTransferCoefficientFromSherwood(
        self, double: float, double2: float, double3: float
    ) -> float: ...
    def calcNusseltNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcWallSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...

class InterphaseDropletFlow(
    InterphaseTwoPhasePipeFlow, jneqsim.thermo.ThermodynamicConstantsInterface
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    def calcInterPhaseFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcNusseltNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcWallMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...

class InterphaseSlugFlow(
    InterphaseTwoPhasePipeFlow, jneqsim.thermo.ThermodynamicConstantsInterface
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    def calcInterPhaseFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcWallMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def getLiquidHoldupInSlug(self) -> float: ...
    def getSlugLengthToDiameterRatio(self) -> float: ...
    def setLiquidHoldupInSlug(self, double: float) -> None: ...
    def setSlugLengthToDiameterRatio(self, double: float) -> None: ...

class InterphaseStratifiedFlow(
    InterphaseTwoPhasePipeFlow, jneqsim.thermo.ThermodynamicConstantsInterface
):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    def calcInterPhaseFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcInterphaseMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ) -> float: ...
    @typing.overload
    def calcWallFrictionFactor(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    @typing.overload
    def calcWallHeatTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...
    def calcWallMassTransferCoefficient(
        self,
        int: int,
        double: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...

class InterphaseAnnularFlow(InterphaseStratifiedFlow):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(
        self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface
    ): ...
    def calcSherwoodNumber(
        self,
        int: int,
        double: float,
        double2: float,
        flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface,
    ) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.interphasepipeflow")``.

    InterphaseAnnularFlow: typing.Type[InterphaseAnnularFlow]
    InterphaseDropletFlow: typing.Type[InterphaseDropletFlow]
    InterphaseSlugFlow: typing.Type[InterphaseSlugFlow]
    InterphaseStratifiedFlow: typing.Type[InterphaseStratifiedFlow]
    InterphaseTwoPhasePipeFlow: typing.Type[InterphaseTwoPhasePipeFlow]
