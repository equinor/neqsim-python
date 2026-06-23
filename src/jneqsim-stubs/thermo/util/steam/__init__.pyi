import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing

class Iapws_if97:
    @staticmethod
    def T4_p(double: float) -> float: ...
    @staticmethod
    def cp_pt(double: float, double2: float) -> float: ...
    @staticmethod
    def h_pt(double: float, double2: float) -> float: ...
    @staticmethod
    def p4_T(double: float) -> float: ...
    @staticmethod
    def psat_t(double: float) -> float: ...
    @staticmethod
    def s_pt(double: float, double2: float) -> float: ...
    @staticmethod
    def tsat_p(double: float) -> float: ...
    @staticmethod
    def v_pt(double: float, double2: float) -> float: ...
    @staticmethod
    def w_pt(double: float, double2: float) -> float: ...

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.thermo.util.steam")``.

    Iapws_if97: typing.Type[Iapws_if97]
