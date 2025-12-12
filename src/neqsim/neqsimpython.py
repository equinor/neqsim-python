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
        jpype.startJVM(convertStrings=False)
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
