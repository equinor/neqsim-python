import jpype

if not(jpype.isJVMStarted()):
    jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=True)

jNeqSim = jpype.JPackage('neqsim')
