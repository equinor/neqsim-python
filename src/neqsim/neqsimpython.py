import jpype
jpype.addClassPath('./lib/NeqSim.jar')
if not(jpype.isJVMStarted()):
    jpype.startJVM(convertStrings =True)

neqsim = jpype.JPackage('neqsim')