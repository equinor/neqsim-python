from neqsim.neqsimpython import jNeqSim


def ISO6976(thermoSystem):
    standard2 = jNeqSim.standards.gasQuality.Standard_ISO6976(thermoSystem)
    standard2.calculate()
    return standard2
