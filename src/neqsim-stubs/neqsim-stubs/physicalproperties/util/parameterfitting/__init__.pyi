
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.physicalproperties.util.parameterfitting")``.

    purecomponentparameterfitting: neqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.__module_protocol__
