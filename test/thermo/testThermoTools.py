# import the package
import neqsim
import unittest
from neqsim.thermo import fluid, TPflash, phaseenvelope, fluidComposition

class TestStringMethods(unittest.TestCase):

    def testTPflash1(self):
        fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
        fluid1.setTemperature(28.15, "C")
        fluid1.setPressure(100.0, "bara")
        fluid1.addComponent("nitrogen", 1.0, "mol/sec")
        fluid1.addComponent("CO2", 2.3, "mol/sec")
        fluid1.addComponent("methane", 80.0, "mol/sec")
        fluid1.addComponent("ethane", 6.0, "mol/sec")
        fluid1.addComponent("propane", 3.0, "mol/sec")
        fluid1.addComponent("i-butane", 1.0, "mol/sec")
        fluid1.addComponent("n-butane", 1.0, "mol/sec")
        fluid1.addComponent("i-pentane", 0.4, "mol/sec")
        fluid1.addComponent("n-pentane", 0.2, "mol/sec")
        fluid1.addComponent("n-hexane", 0.1, "mol/sec")
        fluid1.setMixingRule("classic") # classic will use binary kij 
        fluid1.setMultiPhaseCheck(True) #True if more than two phases could be present
        fluidcomposition = [0.01, 0.02, 0.9, 0.1, 0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
        fluidComposition(fluid1, fluidcomposition)
        fluid1.setPressure(101.0, "bara")
        fluid1.setTemperature(22.3, "C")
        TPflash(fluid1)
        fluid1.initThermoProperties()
        fluid1.initPhysicalProperties()
        self.assertEqual(fluid1.getViscosity('kg/msec'), 1.574354015664789e-05)
        self.assertEqual(fluid1.getZ(), 0.7262354356389622)

    def testTPflash2(self):
        fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
        fluid1.setTemperature(28.15, "C")
        fluid1.setPressure(100.0, "bara")
        fluid1.addComponent("nitrogen", 1.0, "mol/sec")
        fluid1.addComponent("CO2", 2.3, "mol/sec")
        fluid1.addComponent("methane", 80.0, "mol/sec")
        fluid1.addComponent("ethane", 6.0, "mol/sec")
        fluid1.addComponent("propane", 3.0, "mol/sec")
        fluid1.addComponent("i-butane", 1.0, "mol/sec")
        fluid1.addComponent("n-butane", 1.0, "mol/sec")
        fluid1.addComponent("i-pentane", 0.4, "mol/sec")
        fluid1.addComponent("n-pentane", 0.2, "mol/sec")
        fluid1.addComponent("n-heptane", 10.1, "mol/sec")
        fluid1.setMixingRule("classic") # classic will use binary kij 
        fluid1.setMultiPhaseCheck(True) #True if more than two phases could be present
        fluidcomposition = [0.01, 0.02, 0.9, 0.1, 0.03, 0.02, 0.01, 0.01, 0.01, 0.003]
        fluidComposition(fluid1, fluidcomposition)
        fluid1.setPressure(101.0, "bara")
        fluid1.setTemperature(22.3, "C")
        TPflash(fluid1)
        fluid1.initProperties()
        self.assertEqual(fluid1.getNumberOfPhases(), 2)

if __name__ == '__main__':
    unittest.main()