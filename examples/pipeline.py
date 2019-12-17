# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:27:48 2019

@author: esol
"""
from neqsim import methods
from neqsim.thermo import fluid, TPflash
from neqsim.process import pipe, pipeline, clearProcess, stream, runProcess

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-Eo
fluid1.addComponent("methane", 85.0)
fluid1.addComponent("ethane", 5.0)
fluid1.setMixingRule(2)
fluid1.setTemperature(88.15, "C")
fluid1.setPressure(150.0, "bara")
fluid1.setTotalFlowRate(50.0, "MSm3/day")

TPflash(fluid1)
fluid1.initPhysicalProperties()

diameter = [1.0, 1.0, 1.0]
roughnes = [15.0e-6, 15.0e-6, 15.0e-6]
position = [0.0, 1000.0, 5000.0]
height = [0.0, 0.0, 0.0]
outtemperatures =[278.15, 278.15, 278.15]
outHeatU = [15.0, 15.0, 15.0]
wallHeatU = [15.0, 15.0, 15.0]
clearProcess()
stream1 = stream(fluid1)

deltaElevation = 0.0
pipeLength = 500000.0
#roughness= 15.0e-6
#diameter = 1.1
pipe1 = pipeline(stream1, position, diameter, height, outtemperatures, roughnes,outHeatU,wallHeatU)
#pipeSimple = pipe(stream1, pipeLength, deltaElevation, diameter, roughness)
runProcess()
#pipeSimple.getOutStream().displayResult()
#runProcess()

