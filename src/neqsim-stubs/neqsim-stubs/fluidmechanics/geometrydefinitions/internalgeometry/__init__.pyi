
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.fluidmechanics.geometrydefinitions.internalgeometry.packings
import neqsim.fluidmechanics.geometrydefinitions.internalgeometry.wall
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.fluidmechanics.geometrydefinitions.internalgeometry")``.

    packings: neqsim.fluidmechanics.geometrydefinitions.internalgeometry.packings.__module_protocol__
    wall: neqsim.fluidmechanics.geometrydefinitions.internalgeometry.wall.__module_protocol__
