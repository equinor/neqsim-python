
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.fielddevelopment.concept
import jneqsim.process.fielddevelopment.economics
import jneqsim.process.fielddevelopment.evaluation
import jneqsim.process.fielddevelopment.facility
import jneqsim.process.fielddevelopment.integrated
import jneqsim.process.fielddevelopment.network
import jneqsim.process.fielddevelopment.reporting
import jneqsim.process.fielddevelopment.reservoir
import jneqsim.process.fielddevelopment.screening
import jneqsim.process.fielddevelopment.subsea
import jneqsim.process.fielddevelopment.tieback
import jneqsim.process.fielddevelopment.workflow
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.fielddevelopment")``.

    concept: jneqsim.process.fielddevelopment.concept.__module_protocol__
    economics: jneqsim.process.fielddevelopment.economics.__module_protocol__
    evaluation: jneqsim.process.fielddevelopment.evaluation.__module_protocol__
    facility: jneqsim.process.fielddevelopment.facility.__module_protocol__
    integrated: jneqsim.process.fielddevelopment.integrated.__module_protocol__
    network: jneqsim.process.fielddevelopment.network.__module_protocol__
    reporting: jneqsim.process.fielddevelopment.reporting.__module_protocol__
    reservoir: jneqsim.process.fielddevelopment.reservoir.__module_protocol__
    screening: jneqsim.process.fielddevelopment.screening.__module_protocol__
    subsea: jneqsim.process.fielddevelopment.subsea.__module_protocol__
    tieback: jneqsim.process.fielddevelopment.tieback.__module_protocol__
    workflow: jneqsim.process.fielddevelopment.workflow.__module_protocol__
