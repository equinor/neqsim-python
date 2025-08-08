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


def save_neqsim(javaobject, filename):
    """
    Save a NEQSim Java object as a compressed ZIP file with any filename and extension.
    Inside, the XML will be stored as 'process.xml'.
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

        # Setup XStream
        xstream = XStream()
        xstream.allowTypesByWildcard(["neqsim.**"])

        # Prepare file output
        file = File(filename)
        fout = BufferedOutputStream(FileOutputStream(file))
        zout = ZipOutputStream(fout)

        # Fixed entry name inside ZIP
        entry = ZipEntry("process.xml")
        zout.putNextEntry(entry)

        # Stream XML directly into ZIP
        writer = OutputStreamWriter(zout, "UTF-8")
        xstream.toXML(javaobject, writer)
        writer.flush()

        zout.closeEntry()
        writer.close()
        zout.close()

        return True

    except Exception as e:
        print(f"[save_neqsim] Error saving file: {e}")
        return False


def open_neqsim(filename):
    """
    Load a NEQSim Java object from a ZIP file, regardless of file extension.
    The ZIP must contain a 'process.xml' file.
    Suitable for large files.
    """
    if not jpype.isJVMStarted():
        raise RuntimeError(
            "JVM is not started. Please start the JVM with the correct classpath and enough heap size (e.g., -Xmx2g)."
        )

    # Java imports
    XStream = jpype.JClass("com.thoughtworks.xstream.XStream")
    FileInputStream = jpype.JClass("java.io.FileInputStream")
    BufferedInputStream = jpype.JClass("java.io.BufferedInputStream")
    ZipInputStream = jpype.JClass("java.util.zip.ZipInputStream")
    InputStreamReader = jpype.JClass("java.io.InputStreamReader")
    File = jpype.JClass("java.io.File")
    AnyTypePermission = jpype.JClass(
        "com.thoughtworks.xstream.security.AnyTypePermission"
    )

    zin = None
    reader = None

    try:
        file = File(filename)
        fin = BufferedInputStream(FileInputStream(file))
        zin = ZipInputStream(fin)

        entry = zin.getNextEntry()
        if entry is None:
            raise ValueError("ZIP does not contain a valid XML entry.")

        reader = InputStreamReader(zin, "UTF-8")

        xstream = XStream()
        xstream.addPermission(AnyTypePermission.ANY)

        javaobject = xstream.fromXML(reader)
        return javaobject

    except Exception as e:
        print(f"[load_neqsim] Failed to deserialize object: {e}")
        return None

    finally:
        # Ensure streams are closed properly
        try:
            if reader:
                reader.close()
            if zin:
                zin.close()
        except Exception as cleanup_error:
            print(f"[load_neqsim] Cleanup warning: {cleanup_error}")


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
