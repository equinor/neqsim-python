
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.statistics.dataanalysis
import neqsim.statistics.experimentalequipmentdata
import neqsim.statistics.experimentalsamplecreation
import neqsim.statistics.montecarlosimulation
import neqsim.statistics.parameterfitting
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.statistics")``.

    dataanalysis: neqsim.statistics.dataanalysis.__module_protocol__
    experimentalequipmentdata: neqsim.statistics.experimentalequipmentdata.__module_protocol__
    experimentalsamplecreation: neqsim.statistics.experimentalsamplecreation.__module_protocol__
    montecarlosimulation: neqsim.statistics.montecarlosimulation.__module_protocol__
    parameterfitting: neqsim.statistics.parameterfitting.__module_protocol__
