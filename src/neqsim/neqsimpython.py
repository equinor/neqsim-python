import jpype
jpype.addClassPath('./lib/*')
if not(jpype.isJVMStarted()):
    jpype.startJVM(convertStrings =True)

neqsim = jpype.JPackage('neqsim')