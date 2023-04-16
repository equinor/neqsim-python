import jpype

if not jpype.isJVMStarted():
    jpype.startJVM(convertStrings=False)
    jvmVersion = jpype.getJVMVersion()[0]
    if jvmVersion <= 8:
        jpype.addClassPath('./lib/libj8/*')
    else:
        jpype.addClassPath('./lib/*')

jNeqSim = jpype.JPackage('neqsim')
