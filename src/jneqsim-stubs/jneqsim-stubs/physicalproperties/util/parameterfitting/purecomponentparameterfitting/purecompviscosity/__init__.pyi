
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.chungmethod
import jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.linearliquidmodel
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity")``.

    chungmethod: jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.chungmethod.__module_protocol__
    linearliquidmodel: jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.linearliquidmodel.__module_protocol__
