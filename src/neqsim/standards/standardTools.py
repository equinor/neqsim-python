from neqsim.neqsimpython import neqsim

def ISO6976(thermoSystem):
    standard2 = neqsim.standards.gasQuality.Standard_ISO6976(thermoSystem)
    standard2.calculate()
    return standard2
