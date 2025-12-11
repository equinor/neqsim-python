
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.thermodynamicoperations.phaseenvelopeops.multicomponentenvelopeops
import neqsim.thermodynamicoperations.phaseenvelopeops.reactivecurves
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.thermodynamicoperations.phaseenvelopeops")``.

    multicomponentenvelopeops: neqsim.thermodynamicoperations.phaseenvelopeops.multicomponentenvelopeops.__module_protocol__
    reactivecurves: neqsim.thermodynamicoperations.phaseenvelopeops.reactivecurves.__module_protocol__
