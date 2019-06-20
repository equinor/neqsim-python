from py4j.java_gateway import JavaGateway
from neqsim import java_gateway

neqsim = java_gateway.jvm.neqsim


def ISO6976(thermoSystem):
    standard2 = neqsim.standards.gasQuality.Standard_ISO6976(thermoSystem)
    standard2.calculate()
    return standard2
