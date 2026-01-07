
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.fielddevelopment.concept
import jneqsim.process.fielddevelopment.evaluation
import jneqsim.process.fielddevelopment.facility
import jneqsim.process.fielddevelopment.screening
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.fielddevelopment")``.

    concept: jneqsim.process.fielddevelopment.concept.__module_protocol__
    evaluation: jneqsim.process.fielddevelopment.evaluation.__module_protocol__
    facility: jneqsim.process.fielddevelopment.facility.__module_protocol__
    screening: jneqsim.process.fielddevelopment.screening.__module_protocol__
