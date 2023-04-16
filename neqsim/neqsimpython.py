import jpype

if not jpype.isJVMStarted():
    jvmVersion = jpype.getJVMVersion()[0]
    if jvmVersion <= 8:
        jpype.addClassPath('./lib/libj8/*')
    else:
        jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=False)

jNeqSim = jpype.JPackage('neqsim')
