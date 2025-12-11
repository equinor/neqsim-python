
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.process.util.example
import neqsim.process.util.fielddevelopment
import neqsim.process.util.fire
import neqsim.process.util.monitor
import neqsim.process.util.optimization
import neqsim.process.util.report
import neqsim.process.util.scenario
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.process.util")``.

    example: neqsim.process.util.example.__module_protocol__
    fielddevelopment: neqsim.process.util.fielddevelopment.__module_protocol__
    fire: neqsim.process.util.fire.__module_protocol__
    monitor: neqsim.process.util.monitor.__module_protocol__
    optimization: neqsim.process.util.optimization.__module_protocol__
    report: neqsim.process.util.report.__module_protocol__
    scenario: neqsim.process.util.scenario.__module_protocol__
