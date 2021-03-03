import jpype
jpype.addClassPath('./lib/NeqSim.jar')
if not(jpype.isJVMStarted()):
    jpype.startJVM()

neqsim = jpype.JPackage('neqsim')