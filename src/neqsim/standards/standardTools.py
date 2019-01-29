from py4j.java_gateway import JavaGateway
neqsim =  JavaGateway().jvm.neqsim
 
def ISO6976(thermoSystem):
    standard2 = neqsim.standards.gasQuality.Standard_ISO6976(thermoSystem)
    standard2.calculate()
    return standard2

