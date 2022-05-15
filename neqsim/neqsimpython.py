import jpype

if not(jpype.isJVMStarted()):
    jpype.addClassPath('./lib/*')
    try:
        jpype.startJVM(convertStrings=False)
    except:
        print('could not start JVM from jpype')
        
jNeqSim = jpype.JPackage('neqsim')
