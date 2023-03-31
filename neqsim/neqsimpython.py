import jpype

if not jpype.isJVMStarted():
    jvmVersion = jpype.getJVMVersion()[0]
    jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=False)

jNeqSim = jpype.JPackage('neqsim')
