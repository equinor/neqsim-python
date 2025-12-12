import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.process.util.example
import jneqsim.process.util.fielddevelopment
import jneqsim.process.util.fire
import jneqsim.process.util.monitor
import jneqsim.process.util.optimization
import jneqsim.process.util.report
import jneqsim.process.util.scenario
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.process.util")``.

    example: jneqsim.process.util.example.__module_protocol__
    fielddevelopment: jneqsim.process.util.fielddevelopment.__module_protocol__
    fire: jneqsim.process.util.fire.__module_protocol__
    monitor: jneqsim.process.util.monitor.__module_protocol__
    optimization: jneqsim.process.util.optimization.__module_protocol__
    report: jneqsim.process.util.report.__module_protocol__
    scenario: jneqsim.process.util.scenario.__module_protocol__
