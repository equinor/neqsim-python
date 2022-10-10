# import the package
from neqsim.process.processTools import (compsplitter, waterDewPointAnalyser, clearProcess, runProcess, stream, runProcessAsThread)
from neqsim.thermo import (TPflash, fluid, printFrame)
from numpy import isnan
from pytest import approx

def test_compsplitter():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("CO2", 2.3, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream(fluid1)
    splittcomp = compsplitter(stream1, [1.0, 0.0])
    runProcess()
    TPflash(splittcomp.getSplitStream(0).getFluid())
    printFrame(splittcomp.getSplitStream(0).getFluid())
    assert splittcomp.getSplitStream(0).getFluid().getViscosity('kg/msec') > 1e-19

def test_waterDewPointAnalyser():
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("water", 50e-6, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream(fluid1)
    waterDewPoint = waterDewPointAnalyser(stream1)
    runProcess()
    assert waterDewPoint.getMeasuredValue('C') == approx(-11.828217379989212, rel= 0.001)

def test_runProcessAsThread():
    """
    In the test_runProcessAsThread() we set up a process and run it as a thread. 
    We will start the thread and check that the calculated value is diferent from the final results. 
    Then we set maximum calculation time to 10 sec and finish the calculation and check the results is ok.
    """
    fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
    fluid1.setTemperature(28.15, "C")
    fluid1.setPressure(100.0, "bara")
    fluid1.addComponent("nitrogen", 1.0, "mol/sec")
    fluid1.addComponent("water", 50e-6, "mol/sec")
    fluid1.setMixingRule(2)
    clearProcess()
    stream1 = stream(fluid1)
    waterDewPoint = waterDewPointAnalyser(stream1)
    stream2 = stream(fluid1)
    waterDewPoint2 = waterDewPointAnalyser(stream2)
    stream3 = stream(fluid1)
    waterDewPoint3 = waterDewPointAnalyser(stream3)
    processThread = runProcessAsThread()
    assert waterDewPoint2.getMeasuredValue('C') != approx(-11.828217379989212, rel= 0.001)
    processThread.join(10000) #max 10 sec calculation time
    assert waterDewPoint2.getMeasuredValue('C') == approx(-11.828217379989212, rel= 0.001)