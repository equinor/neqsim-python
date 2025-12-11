
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.thermo.util.Vega
import neqsim.thermo.util.benchmark
import neqsim.thermo.util.constants
import neqsim.thermo.util.empiric
import neqsim.thermo.util.gerg
import neqsim.thermo.util.humidair
import neqsim.thermo.util.jni
import neqsim.thermo.util.leachman
import neqsim.thermo.util.readwrite
import neqsim.thermo.util.referenceequations
import neqsim.thermo.util.spanwagner
import neqsim.thermo.util.steam
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.thermo.util")``.

    Vega: neqsim.thermo.util.Vega.__module_protocol__
    benchmark: neqsim.thermo.util.benchmark.__module_protocol__
    constants: neqsim.thermo.util.constants.__module_protocol__
    empiric: neqsim.thermo.util.empiric.__module_protocol__
    gerg: neqsim.thermo.util.gerg.__module_protocol__
    humidair: neqsim.thermo.util.humidair.__module_protocol__
    jni: neqsim.thermo.util.jni.__module_protocol__
    leachman: neqsim.thermo.util.leachman.__module_protocol__
    readwrite: neqsim.thermo.util.readwrite.__module_protocol__
    referenceequations: neqsim.thermo.util.referenceequations.__module_protocol__
    spanwagner: neqsim.thermo.util.spanwagner.__module_protocol__
    steam: neqsim.thermo.util.steam.__module_protocol__
