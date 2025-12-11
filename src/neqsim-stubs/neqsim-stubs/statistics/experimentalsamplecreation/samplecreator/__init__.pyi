
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.statistics.experimentalequipmentdata
import neqsim.statistics.experimentalsamplecreation.samplecreator.wettedwallcolumnsamplecreator
import neqsim.thermo.system
import neqsim.thermodynamicoperations
import typing



class SampleCreator:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: neqsim.thermo.system.SystemInterface, thermodynamicOperations: neqsim.thermodynamicoperations.ThermodynamicOperations): ...
    def setExperimentalEquipment(self, experimentalEquipmentData: neqsim.statistics.experimentalequipmentdata.ExperimentalEquipmentData) -> None: ...
    def setThermoSystem(self, systemInterface: neqsim.thermo.system.SystemInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.statistics.experimentalsamplecreation.samplecreator")``.

    SampleCreator: typing.Type[SampleCreator]
    wettedwallcolumnsamplecreator: neqsim.statistics.experimentalsamplecreation.samplecreator.wettedwallcolumnsamplecreator.__module_protocol__
