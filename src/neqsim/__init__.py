name = "neqsim"
from neqsim import javaGateway
javaGateway.startServer()
from neqsim.thermoTools import *
neqsim =  JavaGateway().jvm.neqsim