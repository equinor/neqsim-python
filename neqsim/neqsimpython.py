import jpype

if not jpype.isJVMStarted():
    jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=False)
    jvmVersion = jpype.getJVMVersion()[0]
    
jNeqSim = jpype.JPackage('neqsim')
