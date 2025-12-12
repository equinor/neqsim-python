import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.statistics.experimentalsamplecreation.readdatafromfile
import jneqsim.statistics.experimentalsamplecreation.samplecreator
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.statistics.experimentalsamplecreation")``.

    readdatafromfile: (
        jneqsim.statistics.experimentalsamplecreation.readdatafromfile.__module_protocol__
    )
    samplecreator: (
        jneqsim.statistics.experimentalsamplecreation.samplecreator.__module_protocol__
    )
