"""
NeqSim is a library for estimation of behaviour and properties of fluids.
This module is a Python interface to the NeqSim Java library.
It uses the Jpype module for bridging python and Java.
"""

from neqsim.neqsimpython import jneqsim, jpype


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
    jneqsim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    jneqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)


def save_xml(javaobject, filename):
    xstream = jpype.JPackage("com.thoughtworks.xstream")
    streamer = xstream.XStream()
    xml = streamer.toXML(javaobject)
    print(xml, file=open(filename, "w"))
    return xml


def open_xml(filename):
    xstream = jpype.JPackage("com.thoughtworks.xstream")
    streamer = xstream.XStream()
    streamer.addPermission(xstream.security.AnyTypePermission.ANY)
    str = open(filename, "r").read()
    neqsimobj = streamer.fromXML(str)
    return neqsimobj
