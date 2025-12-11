
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.statistics.experimentalsamplecreation.readdatafromfile
import neqsim.statistics.experimentalsamplecreation.samplecreator
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.statistics.experimentalsamplecreation")``.

    readdatafromfile: neqsim.statistics.experimentalsamplecreation.readdatafromfile.__module_protocol__
    samplecreator: neqsim.statistics.experimentalsamplecreation.samplecreator.__module_protocol__
