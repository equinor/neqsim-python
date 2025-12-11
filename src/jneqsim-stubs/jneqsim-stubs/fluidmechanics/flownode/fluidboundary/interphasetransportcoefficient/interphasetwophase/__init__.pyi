
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.interphasepipeflow
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.interphasereactorflow
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.stirredcell
import typing



class InterphaseTwoPhase(jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.InterphaseTransportCoefficientBaseClass):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase")``.

    InterphaseTwoPhase: typing.Type[InterphaseTwoPhase]
    interphasepipeflow: jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.interphasepipeflow.__module_protocol__
    interphasereactorflow: jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.interphasereactorflow.__module_protocol__
    stirredcell: jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphasetwophase.stirredcell.__module_protocol__
