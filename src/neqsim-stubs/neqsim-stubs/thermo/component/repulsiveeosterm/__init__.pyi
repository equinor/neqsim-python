
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing



class RepulsiveTermInterface: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("neqsim.thermo.component.repulsiveeosterm")``.

    RepulsiveTermInterface: typing.Type[RepulsiveTermInterface]
