
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.fluidmechanics.flownode
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient
import jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphaseonephase.interphasepipeflow
import typing



class InterphaseOnePhase(jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.InterphaseTransportCoefficientBaseClass):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, flowNodeInterface: jneqsim.fluidmechanics.flownode.FlowNodeInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphaseonephase")``.

    InterphaseOnePhase: typing.Type[InterphaseOnePhase]
    interphasepipeflow: jneqsim.fluidmechanics.flownode.fluidboundary.interphasetransportcoefficient.interphaseonephase.interphasepipeflow.__module_protocol__
