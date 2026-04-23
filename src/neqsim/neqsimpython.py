import jpype


class NeqSimJVMError(Exception):
    """Exception raised when JVM initialization fails."""

    pass


def _get_jvm_error_message() -> str:
    """Return helpful error message for JVM issues."""
    return (
        "Failed to start Java Virtual Machine (JVM).\n\n"
        "Common solutions:\n"
        "1. Install Java JDK 11+ from https://adoptium.net/\n"
        "2. Ensure JAVA_HOME environment variable is set\n"
        "3. Ensure 64-bit Python matches 64-bit Java (or 32-bit with 32-bit)\n\n"
        "See: https://github.com/equinor/neqsim-python#prerequisites"
    )


try:
    if not jpype.isJVMStarted():
        # Could call jpype.getDefaultJVMPath() to get default JVM,
        # but not able to get the orders to force loading a specific JVM
        #
        # Pass "-Xrs" to reduce the JVM's use of OS signals. Without this,
        # the JVM installs signal handlers (SIGINT/SIGTERM/SIGSEGV) that can
        # crash embedded Python kernels in IDEs such as Spyder 6 and some
        # Jupyter setups, producing "The kernel died, restarting..." errors
        # immediately on `import neqsim`. "-Xrs" is safe for normal use.
        #
        # In addition, JPype >= 1.5 installs its own Python-level signal
        # handler chain for SIGINT to forward Ctrl+C into Java. In embedded
        # kernels (Spyder 6, QtConsole, some Jupyter setups) this conflicts
        # with the host's signal handling and can still kill the kernel on
        # `import neqsim` even with "-Xrs". Passing `interrupt=False` tells
        # JPype to leave signal handling to the host process, which resolves
        # the "kernel died, restarting" error in Spyder.
        start_kwargs = {"convertStrings": False}
        try:
            # `interrupt` kwarg was added in JPype 1.5.0. Guard with a
            # fallback for older versions just in case.
            jpype.startJVM("-Xrs", interrupt=False, **start_kwargs)
        except TypeError:
            jpype.startJVM("-Xrs", **start_kwargs)
        jvm_version = jpype.getJVMVersion()[0]
        if jvm_version == 1 and jpype.getJVMVersion()[1] >= 8:
            jpype.addClassPath("./lib/java8/*")
        # elif jvm_version >= 21:
        #    jpype.addClassPath("./lib/java21/*")
        elif jvm_version >= 11:
            jpype.addClassPath("./lib/java11/*")
        else:
            print(
                "Your version of Java is not supported. Please upgrade to Java version 8 or higher."
            )
            print("See: https://github.com/equinor/neqsim-python#prerequisites")
except Exception as e:
    raise NeqSimJVMError(_get_jvm_error_message()) from e

jneqsim = jpype.JPackage("neqsim")
