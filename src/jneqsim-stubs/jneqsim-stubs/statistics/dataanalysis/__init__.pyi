import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.statistics.dataanalysis.datasmoothing
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.statistics.dataanalysis")``.

    datasmoothing: jneqsim.statistics.dataanalysis.datasmoothing.__module_protocol__
