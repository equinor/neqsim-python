
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.api
import neqsim.blackoil
import neqsim.chemicalreactions
import neqsim.datapresentation
import neqsim.fluidmechanics
import neqsim.mathlib
import neqsim.physicalproperties
import neqsim.process
import neqsim.pvtsimulation
import neqsim.standards
import neqsim.statistics
import neqsim.thermo
import neqsim.thermodynamicoperations
import neqsim.util
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim")``.

    api: neqsim.api.__module_protocol__
    blackoil: neqsim.blackoil.__module_protocol__
    chemicalreactions: neqsim.chemicalreactions.__module_protocol__
    datapresentation: neqsim.datapresentation.__module_protocol__
    fluidmechanics: neqsim.fluidmechanics.__module_protocol__
    mathlib: neqsim.mathlib.__module_protocol__
    physicalproperties: neqsim.physicalproperties.__module_protocol__
    process: neqsim.process.__module_protocol__
    pvtsimulation: neqsim.pvtsimulation.__module_protocol__
    standards: neqsim.standards.__module_protocol__
    statistics: neqsim.statistics.__module_protocol__
    thermo: neqsim.thermo.__module_protocol__
    thermodynamicoperations: neqsim.thermodynamicoperations.__module_protocol__
    util: neqsim.util.__module_protocol__
