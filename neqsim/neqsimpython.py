import jpype

if not jpype.isJVMStarted():
    jpype.addClassPath('./lib/*')
    jpype.startJVM(convertStrings=False)
    jvmVersion = jpype.getJVMVersion()[0]
    if jvmVersion<=8:
        print('Your version of Java is not supported. Please upgrade to Java version 11 or higher.')
        print('See: https://github.com/equinor/neqsimpython#prerequisites')

jNeqSim = jpype.JPackage('neqsim')
