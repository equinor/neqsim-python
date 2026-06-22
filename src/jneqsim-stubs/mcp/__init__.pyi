
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.mcp.catalog
import jneqsim.mcp.model
import jneqsim.mcp.runners
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.mcp")``.

    catalog: jneqsim.mcp.catalog.__module_protocol__
    model: jneqsim.mcp.model.__module_protocol__
    runners: jneqsim.mcp.runners.__module_protocol__
