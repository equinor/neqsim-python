import jpype

if not jpype.isJVMStarted():
    #jpype.addClassPath('./lib/*')
    try:
        jpype.startJVM(convertStrings=False)
        jvmVersion = jpype.getJVMVersion()[0]
    except:
        print('could not start JVM from jpype')
    if jvmVersion <= 8:
        jpype.addClassPath('./lib/libj8/*')  
    else:
        jpype.addClassPath('./lib/*') 

jNeqSim = jpype.JPackage('neqsim')
