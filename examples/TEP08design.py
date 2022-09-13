# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:25:59 2019

@author: esol
"""

"""
1. make a fluid stream with methane and n-decane
"
set flow rate to 10 MSm3/day

build an inlet separator operating at 50C amd 45 bar, cool the gas to 30C and sen it to a gas scrubber

estimate the needed cooling duty of the heat exchanger, use water as cooling medium. Estimate the water circulation rate (inlet water temperature 10C, outlet temperature 30C)

estimate the internal diameter of the gas scubber with using a gas load factor og 0.1

design a scrubber with only inlet vane and mesh pad - what is the weight/hight
"""
import math

from neqsim.process import (clearProcess, compressor, heater, runProcess,
                            separator, stream, valve, viewProcess)
from neqsim.thermo import TPflash, fluid, phaseenvelope

fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.addComponent("methane", 99.0)
fluid1.addComponent("nC10", 1.0)
fluid1.setMixingRule(2)

fluid1.setTemperature(50.0, "C")
fluid1.setPressure(50.0, "bara")
fluid1.setTotalFlowRate(10.0, "MSm3/day")

clearProcess()
stream1 = stream(fluid1)
separator1 = separator(stream1, "inlet separator")

cooler1 = heater(separator1.getGasOutStream())
cooler1.setOutTemperature(273.15+30.0)

scrubber1 = separator(cooler1.getOutStream(), "inlet separator")

runProcess()


separator1.getMechanicalDesign().calcDesign()
separartorInnerDiameter = separator1.getMechanicalDesign().getInnerDiameter()
Ks = 0.1
Vtmax = Ks * math.sqrt((separator1.getThermoSystem().getPhase('oil').getDensity()-separator1.getThermoSystem(
).getPhase('gas').getDensity())/separator1.getThermoSystem().getPhase('gas').getDensity())
diameter = math.sqrt(
    separator1.getThermoSystem().getFlowRate("m3/sec")/Vtmax/3.14*4.0)
separator1.getMechanicalDesign().displayResults()


coolerDuty = cooler1.getEnergyInput()
print("cooler duty " + str(cooler1.getEnergyInput()/1.0e6) + " MW")
#phaseenvelope(scrubber1.getThermoSystem(), plot=True)


# calulates enthalpy of water between 10 and 30 C
fluid2 = fluid("srk")  # create a fluid using the SRK-EoS
fluid2.addComponent("water", 1.0)
fluid2.setTemperature(10.0, "C")
fluid2.setPressure(30.0, "bara")
TPflash(fluid2)
fluid2.initThermoProperties()
enthalpy1 = fluid2.getEnthalpy("J/mol")
fluid2.setTemperature(30.0, "C")
fluid2.initThermoProperties()
enthalpy2 = fluid2.getEnthalpy("J/mol")

flowratewater = coolerDuty/(enthalpy1-enthalpy2) * \
    fluid2.getMolarMass()*3600/1000.0

print("cooling water rate " + str(flowratewater) + " m3/hr")
