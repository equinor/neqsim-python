# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:43:53 2019

@author: esol
"""

import pyims

#https://git.equinor.com/ProcessControl/pyIMS
 
print(pyims.list_aspen_servers())
#print(pyims.list_pi_servers())
c = pyims.IMSClient('GRA','Aspen')
#c = pyims.IMSClient('GRA','Aspen')
c.connect() 
tags = ['GRA-PT  -21-0111.PV','GRA-TIC -21-0113X.PV','GRA-PZT -21-0112.PV']
df = c.read_tags(tags,'26-May-19 13:00:00','03-Jun-19 13:00:00',3600) 
df.describe()
print(df.head(5))

print(c.search_tag('*GFA*TT*'))





components = ["water", "nitrogen", "CO2", "methane", "ethane", "propane", "i-butane","n-butane","i-pentane", "n-pentane", "CHCmp_1", "CHCmp_2", "CHCmp_3", "CHCmp_4" ,"CHCmp_5","CHCmp_6","CHCmp_7"]
fractions1 = [0.0386243104934692, 1.08263303991407E-05, 0.00019008457660675, 0.00305547803640366, 0.00200786963105202, 0.00389420658349991,0.00179276615381241 ,  0.00255768150091171, 0.00205287128686905, 0.00117853358387947, 0.000867870151996613, 0.048198757171630900,0.097208471298217800,0.165174083709717000, 0.279571933746338000, 0.240494251251221000, 0.113120021820068000]

molarmass = [0.0386243104934692, 1.08263303991407E-05, 0.00019008457660675, 0.00305547803640366, 0.00200786963105202, 0.00389420658349991,0.00179276615381241 ,  0.00255768150091171, 0.00205287128686905, 0.00117853358387947 , 0.0810000000000000, 0.0987799987792969, 0.1412200012207030, 0.1857899932861330, 0.2410899963378910, 0.4045100097656250,0.9069699707031250]
density = [0.0386243104934692, 1.08263303991407E-05, 0.00019008457660675, 0.00305547803640366, 0.00200786963105202, 0.00389420658349991,0.00179276615381241 ,  0.00255768150091171, 0.00205287128686905, 0.00117853358387947, 0.72122997045517,0.754330039024353, 0.81659996509552, 0.861050009727478, 0.902539968490601, 0.955269992351531, 1.0074599981308]



from neqsim.thermo import fluid, TPflash

# Start by creating a fluid in neqsim
fluid1 = fluid("srk")  # create a fluid using the SRK-EoS
fluid1.setTemperature(28.15, "C")
fluid1.setPressure(10.0, "bara")

for c in range(1,len(components)):
    if(components[c].startswith("CH")):
        fluid1.addTBPfraction(components[c],fractions1[c], molarmass[c], density[c])
    else:
        fluid1.addComponent(components[c],fractions1[c])

fluid1.setMixingRule(2)
fluid1.setMultiPhaseCheck(True)
TPflash(fluid1)

def TPenthalpy(frame):
        fluid1.setPressure(frame['GRA-PT  -21-0111.PV']+1.01325)
        fluid1.setTemperature(frame['GRA-TIC -21-0113X.PV']+273.15)
        TPflash(fluid1)
        fluid1.init(2)
        return fluid1.getEnthalpy("J/mol")
    
def TPthermalCond(frame):
        fluid1.setPressure(frame['GRA-PT  -21-0111.PV']+1.01325)
        fluid1.setTemperature(frame['GRA-TIC -21-0113X.PV']+273.15)
        TPflash(fluid1)
        fluid1.initPhysicalProperties()
        return fluid1.getConductivity()

from neqsim import java_gateway


def PHentropy(frame):
        fluid1.setPressure(frame['GRA-PZT -21-0112.PV']+1.01325)
        neqsim = java_gateway.jvm.neqsim
        ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations
        testFlash = ThermodynamicOperations(fluid1)
        #TPflash(fluid1)
        testFlash.PHflash(frame["enthalpy"], "J/mol")
        fluid1.init(3)
        if(fluid1.getEntropy("J/molK")>0.0):
            #testFlash.PHflash(frame["enthalpy"]+0.01, "J/mol")
            errorConditions = str(frame["enthalpy"])
            file = "C:/temp/neqsimfluids/"  +errorConditions + ".neqsim"
            print(file)
            fluid1.saveObjectToFile(file,"")
            fluid1.display()
        return fluid1.getEntropy("J/molK")

def PSentropy(frame):
        fluid1.setPressure(frame['GRA-PZT -21-0112.PV']+1.01325)
        neqsim = java_gateway.jvm.neqsim
        ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations
        testFlash = ThermodynamicOperations(fluid1)
        #TPflash(fluid1)
        testFlash.PSflash(frame["entropy"], "J/molK")
        fluid1.init(3)
        return fluid1.getEntropy("J/molK")


def thermalConductivity(frame):
        fluid1.setPressure(frame['GRA-PZT -21-0112.PV']+1.01325)
        neqsim = java_gateway.jvm.neqsim
        ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations
        testFlash = ThermodynamicOperations(fluid1)
        #TPflash(fluid1)
        testFlash.PHflash(frame["enthalpy"], "J/mol")
        fluid1.init(3)
        fluid1.initPhysicalProperties()
        return fluid1.getConductivity()
   

dataTest = df[['GRA-PT  -21-0111.PV','GRA-TIC -21-0113X.PV','GRA-PZT -21-0112.PV']]
dataTest["enthalpy"] = dataTest.apply(TPenthalpy, axis=1)
dataTest["ThermCond1"] = dataTest.apply(TPthermalCond, axis=1)
dataTest["entropy"] = dataTest.apply(PHentropy, axis=1)
dataTest["entropy2"] = dataTest.apply(PSentropy, axis=1)
dataTest["thermalCond"] = dataTest.apply(thermalConductivity, axis=1)

dataTest.plot(y='GRA-PT  -21-0111.PV')
dataTest.plot(y='GRA-TIC -21-0113X.PV')
dataTest.plot(y='GRA-PZT -21-0112.PV')
dataTest.plot(y='enthalpy')
dataTest.plot(y='entropy')
dataTest.plot(x='entropy2',y='entropy')
dataTest.plot(y='thermalCond')
dataTest.plot(y='ThermCond1')

