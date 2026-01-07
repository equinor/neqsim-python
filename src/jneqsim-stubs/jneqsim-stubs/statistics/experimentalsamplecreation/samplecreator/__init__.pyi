
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.statistics.experimentalequipmentdata
import jneqsim.statistics.experimentalsamplecreation.samplecreator.wettedwallcolumnsamplecreator
import jneqsim.thermo.system
import jneqsim.thermodynamicoperations
import typing



class SampleCreator:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, systemInterface: jneqsim.thermo.system.SystemInterface, thermodynamicOperations: jneqsim.thermodynamicoperations.ThermodynamicOperations): ...
    def setExperimentalEquipment(self, experimentalEquipmentData: jneqsim.statistics.experimentalequipmentdata.ExperimentalEquipmentData) -> None: ...
    def setThermoSystem(self, systemInterface: jneqsim.thermo.system.SystemInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.statistics.experimentalsamplecreation.samplecreator")``.

    SampleCreator: typing.Type[SampleCreator]
    wettedwallcolumnsamplecreator: jneqsim.statistics.experimentalsamplecreation.samplecreator.wettedwallcolumnsamplecreator.__module_protocol__
