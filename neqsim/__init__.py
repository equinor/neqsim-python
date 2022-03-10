name = "neqsim"

from neqsim.neqsimpython import neqsim

def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())
            
def setDatabase(connectionString):
    neqsim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    neqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)