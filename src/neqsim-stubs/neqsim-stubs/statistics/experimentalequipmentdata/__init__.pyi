
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.statistics.experimentalequipmentdata.wettedwallcolumndata
import typing



class ExperimentalEquipmentData:
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.statistics.experimentalequipmentdata")``.

    ExperimentalEquipmentData: typing.Type[ExperimentalEquipmentData]
    wettedwallcolumndata: neqsim.statistics.experimentalequipmentdata.wettedwallcolumndata.__module_protocol__
