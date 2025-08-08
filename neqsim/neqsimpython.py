import jpype

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
        print("See: https://github.com/equinor/neqsimpython#prerequisites")

jneqsim = jpype.JPackage("neqsim")
