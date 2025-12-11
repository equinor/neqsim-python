
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.mathlib.generalmath
import neqsim.mathlib.nonlinearsolver
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.mathlib")``.

    generalmath: neqsim.mathlib.generalmath.__module_protocol__
    nonlinearsolver: neqsim.mathlib.nonlinearsolver.__module_protocol__
