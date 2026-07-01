import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompinterfacetension
import jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity
import typing

class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting")``.

    purecompinterfacetension: (
        jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompinterfacetension.__module_protocol__
    )
    purecompviscosity: (
        jneqsim.physicalproperties.util.parameterfitting.purecomponentparameterfitting.purecompviscosity.__module_protocol__
    )
