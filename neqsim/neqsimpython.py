import jpype

if not jpype.isJVMStarted():
    #jpype.addClassPath('./lib/*')
    try:
        jpype.startJVM(convertStrings=False)
        jvmVersion = jpype.getJVMVersion()[0]
        if jvmVersion <= 8:
            jpype.addClassPath('./lib/libj8/*')  
        else:
            jpype.addClassPath('./lib/*') 
    except:
        print('Java could not be started. Please check that Java is installed on your computer. Java can be downloaded from https://adoptium.net/')

jNeqSim = jpype.JPackage('neqsim')
