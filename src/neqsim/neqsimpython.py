import jpype
import atexit

if not jpype.isJVMStarted():
    # Start the JVM with your specific options and classpath settings
    jpype.startJVM("-Xms512m", "-Xmx2g", convertStrings=False)
    jvm_version = jpype.getJVMVersion()[0]
    if jvm_version == 1 and jpype.getJVMVersion()[1] >= 8:
        jpype.addClassPath("./lib/java8/*")
    elif jvm_version >= 11:
        jpype.addClassPath("./lib/java11/*")
    else:
        print(
            "Your version of Java is not supported. "
            "Please upgrade to Java version 8 or higher."
        )
        print("See: https://github.com/equinor/neqsimpython#prerequisites")

# Register the shutdown function to be called at interpreter exit
atexit.register(lambda: jpype.shutdownJVM() if jpype.isJVMStarted() else None)

jneqsim = jpype.JPackage("neqsim")
