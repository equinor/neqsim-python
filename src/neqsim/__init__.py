"""
NeqSim is a library for estimation of behaviour and properties of fluids.
This module is a Python interface to the NeqSim Java library.
It uses the Jpype module for bridging python and Java.
"""

from neqsim.neqsimpython import jneqsim, jpype
import gzip


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


def save_neqsim(javaobject, filename):
    """
    Serialize a Java object (such as a NEQSim ProcessSystem) to XML
    using XStream, then compress and save it as a .gz file.

    Args:
        javaobject: A Java object that XStream can serialize (e.g., neqsim.process.processmodel.ProcessSystem).
        filename (str): The path (including filename) to write the compressed XML file.
            For clarity, you can use a .xml.gz extension, for example "myProcess.xml.gz".

    Returns:
        bool: True if the file is successfully written.

    Raises:
        Any exception raised by XStream serialization, file I/O, or gzip operations
        will propagate unless caught by the caller.

    Usage Example:
        # 1. Ensure JPype has started the JVM and XStream is on the classpath:
        #    if not jpype.isJVMStarted():
        #        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", f"-Djava.class.path=path/to/xstream.jar")

        # 2. Acquire or build the NEQSim process object (javaobject).
        #    process = ... # your neqsim.process.processmodel.ProcessSystem

        # 3. Call save_neqsim:
        #    save_neqsim(process, "myProcess.xml.gz")
    """
    # Instantiate XStream from the Java packages
    xstream = jpype.JPackage("com.thoughtworks.xstream").XStream()

    # Convert the Java object to an XML string (java.lang.String)
    xml_java_string = xstream.toXML(javaobject)

    # Convert java.lang.String to a native Python string
    xml_python_string = str(xml_java_string)

    # Compress and save the string as UTF-8 bytes in a .gz file
    with gzip.open(filename, "wb") as f:
        f.write(xml_python_string.encode("utf-8"))

    return True


def open_neqsim(filename, allow_all=True, wildcard_permission=None):
    """
    Decompress and deserialize a Java object (e.g., a NEQSim ProcessSystem)
    from a gzipped XStream XML file.

    Args:
        filename (str): Path to the gzipped file (e.g. 'process.neqsim').
        allow_all (bool): If True, uses AnyTypePermission to allow all classes
            during deserialization. This is simple but not recommended for
            production security.
        wildcard_permission (list of str, optional):
            A list of wildcard patterns for XStream to allow. For example,
            ['neqsim.**'] would allow classes under 'neqsim'.

    Returns:
        object: The deserialized Java object (e.g., a NEQSim ProcessSystem),
                or None if an error occurs.

    Raises:
        Any exceptions raised by file I/O, gzip, XStream, or JPype will
        propagate unless caught by the caller.

    Usage Example:
        # Ensure the JVM is started and the XStream JAR is on the classpath.
        # jpype.startJVM(..., classpath=[...])

        # open_neqsim("myProcess.neqsim", allow_all=True)
    """
    # 1. Create an XStream instance
    xstream_cls = jpype.JPackage("com.thoughtworks.xstream").XStream
    xstream = xstream_cls()

    # 2. Configure security permissions
    security_pkg = jpype.JPackage("com.thoughtworks.xstream.security")
    if allow_all:
        # Allow everything (not recommended in production)
        anyTypePermission_cls = security_pkg.AnyTypePermission
        xstream.addPermission(anyTypePermission_cls.ANY)
    elif wildcard_permission is not None:
        # e.g. wildcard_permission = ["neqsim.**"]
        wildcard_cls = security_pkg.WildcardTypePermission
        xstream.addPermission(wildcard_cls(wildcard_permission))
    else:
        # By default, XStream might reject many classes.
        # The user can add more specific permissions here.
        pass

    # 3. Read and decompress the file
    try:
        with gzip.open(filename, "rb") as f:
            xml_bytes = f.read()
        xml_str = xml_bytes.decode("utf-8")
    except Exception as e:
        print(f"[open_neqsim] Failed to read/decompress file: {e}")
        return None

    # 4. Deserialize using XStream
    try:
        java_object = xstream.fromXML(xml_str)
        return java_object
    except Exception as e:
        print(f"[open_neqsim] Failed to deserialize object: {e}")
        return None


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
