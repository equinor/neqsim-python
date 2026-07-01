
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.thermodynamicoperations.phaseenvelopeops.multicomponentenvelopeops
import jneqsim.thermodynamicoperations.phaseenvelopeops.reactivecurves
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermodynamicoperations.phaseenvelopeops")``.

    multicomponentenvelopeops: jneqsim.thermodynamicoperations.phaseenvelopeops.multicomponentenvelopeops.__module_protocol__
    reactivecurves: jneqsim.thermodynamicoperations.phaseenvelopeops.reactivecurves.__module_protocol__
