def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())


def setDatabase(connectionString):
    from neqsim.neqsimpython import neqsim

    neqsim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    neqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
