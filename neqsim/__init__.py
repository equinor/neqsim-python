def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())


def setDatabase(connectionString):
    from neqsim.neqsimpython import jNeqSim

    jNeqSim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    jNeqSim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
