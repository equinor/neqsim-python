# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:54:21 2020

@author: esol
"""


from neqsim.thermo import *
from neqsim import java_gateway
neqsim = java_gateway.jvm.neqsim
neqsim.util.database.NeqSimDataBase.setConnectionString("jdbc:derby:C:/Users/esol/OneDrive - Equinor/temp/neqsimthermodatabase");
neqsim.util.database.NeqSimDataBase.setCreateTemporaryTables(True);
    	

        
# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS

fluid1.addComponent("nitrogen", 1.0, "mol/sec")
fluid1.addComponent("CO2", 2.3, "mol/sec")
fluid1.addComponent("methane", 80.0, "mol/sec")
fluid1.addComponent("ethane", 6.0, "mol/sec")
fluid1.addComponent("propane", 3.0, "mol/sec")
fluid1.addComponent("i-butane", 1.0, "mol/sec")
fluid1.addComponent("n-butane", 1.0, "mol/sec")
fluid1.addPlusFraction("C11", 2.95, 217.0 / 1000.0, 0.8331);
fluid1.getCharacterization().characterisePlusFraction();
fluid1.getWaxModel().addTBPWax();
fluid1.createDatabase(True);
fluid1.setMixingRule(2);
fluid1.addSolidComplexPhase("wax");
fluid1.setMultiphaseWaxCheck(True);

fluid1.setTemperature(10.112, "C")
fluid1.setPressure(10.0, "bara")

TPflash(fluid1)
printFrame(fluid1)

fluid1.setTemperature(40.112, "C")
fluid1.setPressure(10.0, "bara")
waxTemp = WAT(fluid1)-273.15
#printFrame(fluid1)
print("WAT ", waxTemp, " °C")
