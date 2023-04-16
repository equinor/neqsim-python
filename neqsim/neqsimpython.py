import jpype

if not jpype.isJVMStarted():
    jvmVersion = jpype.getJVMVersion()[0]
    if jvmVersion<1:
        print('could not detech JVM version. Using version Java 11+ of neqsim library.')
    if jvmVersion <= 8 and jvmVersion>1:
        jpype.addClassPath('./lib/libj8/*')
    else:
        jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=False)

jNeqSim = jpype.JPackage('neqsim')
