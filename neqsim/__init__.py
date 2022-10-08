"""
NeqSim is a library for estimation of behaviour and properties of fluids. 
This module is a Python interface to the NeqSim Java library. 
It uses the Jpype module for bridging python and Java.
"""

from .neqsimpython import *

def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())


def has_matplotlib():
    from importlib.util import find_spec
    return find_spec("matplotlib")


def has_tabulate():
    from importlib.util import find_spec
    return find_spec("tabulate")


def setDatabase(connectionString):
    from neqsim.neqsimpython import jNeqSim
    jNeqSim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    jNeqSim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
