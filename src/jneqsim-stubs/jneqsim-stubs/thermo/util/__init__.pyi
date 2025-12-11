
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.thermo.util.Vega
import jneqsim.thermo.util.benchmark
import jneqsim.thermo.util.constants
import jneqsim.thermo.util.empiric
import jneqsim.thermo.util.gerg
import jneqsim.thermo.util.humidair
import jneqsim.thermo.util.jni
import jneqsim.thermo.util.leachman
import jneqsim.thermo.util.readwrite
import jneqsim.thermo.util.referenceequations
import jneqsim.thermo.util.spanwagner
import jneqsim.thermo.util.steam
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util")``.

    Vega: jneqsim.thermo.util.Vega.__module_protocol__
    benchmark: jneqsim.thermo.util.benchmark.__module_protocol__
    constants: jneqsim.thermo.util.constants.__module_protocol__
    empiric: jneqsim.thermo.util.empiric.__module_protocol__
    gerg: jneqsim.thermo.util.gerg.__module_protocol__
    humidair: jneqsim.thermo.util.humidair.__module_protocol__
    jni: jneqsim.thermo.util.jni.__module_protocol__
    leachman: jneqsim.thermo.util.leachman.__module_protocol__
    readwrite: jneqsim.thermo.util.readwrite.__module_protocol__
    referenceequations: jneqsim.thermo.util.referenceequations.__module_protocol__
    spanwagner: jneqsim.thermo.util.spanwagner.__module_protocol__
    steam: jneqsim.thermo.util.steam.__module_protocol__
