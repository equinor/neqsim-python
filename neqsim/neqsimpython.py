import jpype

jpype.addClassPath('./lib/*')
if not(jpype.isJVMStarted()):
    jpype.startJVM(convertStrings=True)

jNeqSim = jpype.JPackage('neqsim')
