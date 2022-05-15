import jpype

if not(jpype.isJVMStarted()):
    jpype.addClassPath('./lib/*')
    try:
        jpype.startJVM(convertStrings=True)
    except:
        print('could not start JVM')
        
jNeqSim = jpype.JPackage('neqsim')
