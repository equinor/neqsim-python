import jpype
import jpype.imports
from jpype import JImplements, JOverride
import numpy as np
from neqsim import jNeqSim

@JImplements(jNeqSim.util.NamedInterface) # Use the fully qualified class name directly from the jNeqSim package
class unitop:
    def __init__(self):
        self.name = ""

    @JOverride
    def getName(self):
        return self.name

    @JOverride
    def setName(self, name):
        self.name = name