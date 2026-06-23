import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.equipment.well.allocation
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.equipment.well")``.

    allocation: jneqsim.process.equipment.well.allocation.__module_protocol__
