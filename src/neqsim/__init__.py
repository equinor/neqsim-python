name = "neqsim"
from neqsim import javaGateway
javaGateway.startServer()
import time
time.sleep(2)
from neqsim.thermo.thermoTools import *
from neqsim.process.processTools import *
from neqsim.standards.standardTools import *