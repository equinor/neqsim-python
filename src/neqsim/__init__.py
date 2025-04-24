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


def open_neqsim(filename, allow_all=True, wildcard_permission=None):
    """
    Open and deserialize a NEQSim Java object from either a .gz or .zip XStream-serialized XML file.

    Supports:
        - GZipped XML: .xml.gz
        - Zipped XML: .zip (must contain a file named 'process.xml')

    Returns:
        object: The deserialized Java object.
    """
    import os

    # Instantiate XStream
    XStream = jpype.JClass("com.thoughtworks.xstream.XStream")
    xstream = XStream()

    # Configure security
    security_pkg = jpype.JPackage("com.thoughtworks.xstream.security")
    if allow_all:
        xstream.addPermission(security_pkg.AnyTypePermission.ANY)
    elif wildcard_permission is not None:
        xstream.addPermission(security_pkg.WildcardTypePermission(wildcard_permission))

    # Detect file format by extension
    ext = os.path.splitext(filename)[-1].lower()

    try:
        if ext == ".gz":
            with gzip.open(filename, "rb") as f:
                xml_bytes = f.read()
        elif ext == ".zip":
            import zipfile

            with zipfile.ZipFile(filename, "r") as zf:
                with zf.open("process.xml") as f:
                    xml_bytes = f.read()
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    except Exception as e:
        print(f"[open_neqsim] Failed to read/compress/decompress file: {e}")
        return None

    # Deserialize
    try:
        xml_str = xml_bytes.decode("utf-8")
        java_object = xstream.fromXML(xml_str)
        return java_object
    except Exception as e:
        print(f"[open_neqsim] Failed to deserialize object: {e}")
        return None


def save_neqsim(javaobject, filename):
    """
    Serialize a Java object (e.g., NEQSim ProcessSystem) to XML using XStream,
    and save it as a compressed ZIP file containing one XML file.

    Args:
        javaobject: A Java object that XStream can serialize.
        filename (str): The path to the ZIP file to write (e.g., "myProcess.zip").

    Returns:
        bool: True if the file is successfully written, False otherwise.
    """
    if not jpype.isJVMStarted():
        raise RuntimeError(
            "JVM is not started. Please start the JVM with the correct classpath."
        )

    try:
        # Java imports
        XStream = jpype.JClass("com.thoughtworks.xstream.XStream")
        FileOutputStream = jpype.JClass("java.io.FileOutputStream")
        BufferedOutputStream = jpype.JClass("java.io.BufferedOutputStream")
        ZipOutputStream = jpype.JClass("java.util.zip.ZipOutputStream")
        ZipEntry = jpype.JClass("java.util.zip.ZipEntry")
        OutputStreamWriter = jpype.JClass("java.io.OutputStreamWriter")
        File = jpype.JClass("java.io.File")

        # Create XStream instance and configure security
        xstream = XStream()
        xstream.allowTypesByWildcard(["neqsim.**"])

        # Setup output stream and ZIP structure
        file = File(filename)
        fout = BufferedOutputStream(FileOutputStream(file))
        zout = ZipOutputStream(fout)

        # Use a fixed name for the XML inside the ZIP
        entry = ZipEntry("process.xml")
        zout.putNextEntry(entry)

        writer = OutputStreamWriter(zout, "UTF-8")
        xstream.toXML(javaobject, writer)
        writer.flush()
        zout.closeEntry()
        writer.close()
        zout.close()

        return True
    except Exception as e:
        print(f"Error saving NEQSim object to ZIP: {e}")
        return False


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
