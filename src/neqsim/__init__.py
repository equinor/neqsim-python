name = "neqsim"

from neqsim import javaGateway

java_gateway = javaGateway.start_server()

def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())
            
