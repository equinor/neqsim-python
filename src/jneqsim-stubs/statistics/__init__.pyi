import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.statistics.dataanalysis
import jneqsim.statistics.experimentalequipmentdata
import jneqsim.statistics.experimentalsamplecreation
import jneqsim.statistics.montecarlosimulation
import jneqsim.statistics.parameterfitting
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.statistics")``.

    dataanalysis: jneqsim.statistics.dataanalysis.__module_protocol__
    experimentalequipmentdata: (
        jneqsim.statistics.experimentalequipmentdata.__module_protocol__
    )
    experimentalsamplecreation: (
        jneqsim.statistics.experimentalsamplecreation.__module_protocol__
    )
    montecarlosimulation: jneqsim.statistics.montecarlosimulation.__module_protocol__
    parameterfitting: jneqsim.statistics.parameterfitting.__module_protocol__
