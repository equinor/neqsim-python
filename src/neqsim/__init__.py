name = "neqsim"

from neqsim import javaGateway

try:
    java_gateway
except:
    java_gateway = javaGateway.start_server()

def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())
            
def setDatabase(connectionString):
    neqsim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    neqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
