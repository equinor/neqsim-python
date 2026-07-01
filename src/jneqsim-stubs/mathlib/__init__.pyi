
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.mathlib.generalmath
import jneqsim.mathlib.nonlinearsolver
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.mathlib")``.

    generalmath: jneqsim.mathlib.generalmath.__module_protocol__
    nonlinearsolver: jneqsim.mathlib.nonlinearsolver.__module_protocol__
