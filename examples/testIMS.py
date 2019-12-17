"""
Read data for Gran using pyIMS
"""
import pyims
c = pyims.IMSClient('GRA','Aspen')
c.connect() 
tags = ['GRA-PT  -21-0111.PV','GRA-TIC -21-0113X.PV','GRA-PZT -21-0112.PV']
df = c.read_tags(tags,'26-May-19 13:00:00','03-Jun-19 13:00:00',3600) 




"""
Creating a Grane oil using NeqSim
"""
components = ["water", "nitrogen", "CO2", "methane", "ethane", "propane", "i-butane","n-butane","i-pentane", "n-pentane", "CHCmp_1", "CHCmp_2", "CHCmp_3", "CHCmp_4" ,"CHCmp_5","CHCmp_6","CHCmp_7"]
fractions1 = [0.0386243104934692, 1.08263303991407E-05, 0.00019008457660675, 0.00305547803640366, 0.00200786963105202, 0.00389420658349991,0.00179276615381241 ,  0.00255768150091171, 0.00205287128686905, 0.00117853358387947, 0.000867870151996613, 0.048198757171630900,0.097208471298217800,0.165174083709717000, 0.279571933746338000, 0.240494251251221000, 0.113120021820068000]
molarmass = [0, 0, 0.0, 0, 0, 0,0, 0, 0, 0, 0.081, 0.098, 0.141, 0.185, 0.2410, 0.404,0.906]
density = [0, 0, 0.0, 0, 0, 0,0, 0, 0, 0, 0.72,0.75, 0.81, 0.861, 0.902, 0.9552, 1.0074]


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


"""
Define a function to flash the fluid and calculate thermal conductivity
"""
def TPthermalCond(frame):
        fluid1.setPressure(frame['GRA-PT  -21-0111.PV']+1.01325)
        fluid1.setTemperature(frame['GRA-TIC -21-0113X.PV']+273.15)
        TPflash(fluid1)
        fluid1.initPhysicalProperties()
        return fluid1.getConductivity()


"""
Add thermal conductivity to the data frame
"""
dataTest = df[['GRA-PT  -21-0111.PV','GRA-TIC -21-0113X.PV','GRA-PZT -21-0112.PV']]
dataTest["ThermCond1"] = dataTest.apply(TPthermalCond, axis=1)
dataTest.plot(y='ThermCond1')