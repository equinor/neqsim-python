name = "neqsim"

from neqsim import javaGateway

java_gateway = javaGateway.start_server()
neqsim = java_gateway.jvm.neqsim

def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())
            
def setDatabase(connectionString):
    neqsim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    neqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
