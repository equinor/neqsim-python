import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.api
import jneqsim.blackoil
import jneqsim.chemicalreactions
import jneqsim.datapresentation
import jneqsim.fluidmechanics
import jneqsim.mathlib
import jneqsim.physicalproperties
import jneqsim.process
import jneqsim.pvtsimulation
import jneqsim.standards
import jneqsim.statistics
import jneqsim.thermo
import jneqsim.thermodynamicoperations
import jneqsim.util
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim")``.

    api: jneqsim.api.__module_protocol__
    blackoil: jneqsim.blackoil.__module_protocol__
    chemicalreactions: jneqsim.chemicalreactions.__module_protocol__
    datapresentation: jneqsim.datapresentation.__module_protocol__
    fluidmechanics: jneqsim.fluidmechanics.__module_protocol__
    mathlib: jneqsim.mathlib.__module_protocol__
    physicalproperties: jneqsim.physicalproperties.__module_protocol__
    process: jneqsim.process.__module_protocol__
    pvtsimulation: jneqsim.pvtsimulation.__module_protocol__
    standards: jneqsim.standards.__module_protocol__
    statistics: jneqsim.statistics.__module_protocol__
    thermo: jneqsim.thermo.__module_protocol__
    thermodynamicoperations: jneqsim.thermodynamicoperations.__module_protocol__
    util: jneqsim.util.__module_protocol__
