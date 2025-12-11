import types
import typing


import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import neqsim


@typing.overload
def JPackage(__package_name: Literal['neqsim']) -> neqsim.__module_protocol__: ...


@typing.overload
def JPackage(__package_name: str) -> types.ModuleType: ...


def JPackage(__package_name) -> types.ModuleType: ...

