def methods(checkClass):
    methods = checkClass.getClass().getMethods()
    for method in methods:
        print(method.getName())


def has_matplotlib():
    from importlib.util import find_spec
    return find_spec("matplotlib")


def setDatabase(connectionString):
    from neqsim.neqsimpython import jNeqSim

    jNeqSim.util.database.NeqSimDataBase.setConnectionString(connectionString)
    jNeqSim.util.database.NeqSimDataBase.setCreateTemporaryTables(True)
