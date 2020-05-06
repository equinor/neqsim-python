from neqsim.thermo import *
import matplotlib.pyplot as plt

fluid1 = createfluid('black oil')
TPflash(fluid1)

print("Phase envelope...................")
phaseenvelope(fluid1,True)

pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 10.0, 1.01325]
temperature = [301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0]

print("Viscosity...................")
gasviscosity = []
oilviscosity = []
viscositysim(fluid1,pressure,temperature,gasviscosity,oilviscosity)
plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, gasviscosity, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('gasviscosity [kg/msec]')
plt.subplot(132)
plt.plot(pressure, oilviscosity, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('oilviscosity [kg/msec]')
plt.show()

#saturation pressure calc
satpress= saturationpressure(fluid1, 340.0)
print("saturation pressure ", satpress)

print("CME...............")
pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 10.0]
temperature = [301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0]

relativevolume = []
liquidrelativevolume = []
Zgas =  []
Yfactor = []
isothermalcompressibility = []
saturationpressure = None
CME(fluid1,pressure,temperature,saturationpressure, relativevolume, liquidrelativevolume,Zgas,Yfactor,isothermalcompressibility)

plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, relativevolume, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('relative volume [-]')
plt.subplot(132)
plt.plot(pressure, Yfactor, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('Yfactor [-]')
plt.subplot(133)
plt.plot(pressure, isothermalcompressibility, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('isothermalcompressibility [1/bar]')
plt.show()

print("GOR")
pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 10.0, 1.01325]
temperature = [301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0, 301.0]

GORdata = []
Bo = []
GOR(fluid1, pressure, temperature, GORdata, Bo)

plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, GORdata, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('GORdata [Sm3 gas/Sm3 oil]')
plt.subplot(132)
plt.plot(pressure, Bo, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('Bo[m3/Sm3]')
plt.show()

print("CVD...............")
pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 10.0]
temperature = 301.0

relativevolume = []
liquidrelativevolume = []
Zgas =  []
Zmix = []
cummulativemolepercdepleted = []

CVD(fluid1,pressure,temperature,relativevolume, liquidrelativevolume,Zgas,Zmix,cummulativemolepercdepleted)

plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, relativevolume, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('relative volume [-]')
plt.subplot(132)
plt.plot(pressure, cummulativemolepercdepleted, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('cummulative depleted [-]')
plt.show()



print("differential liberation...............")
pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 10.0, 1.01325]
temperature = 301.0
printFrame(fluid1)
Bo = []
Bg = []
relativegravity = []
Zgas =  []
gasstandardvolume = []
Rs = []
oildensity = []
relativegravity = []
relativevolume = []

difflib(fluid1.clone(),pressure,temperature,relativevolume,Bo, Bg,relativegravity,Zgas,gasstandardvolume,Rs, oildensity, relativegravity)


plt.figure(figsize=(20, 5))
plt.subplot(131)
plt.plot(pressure, Bo, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('Bo [m3/Sm3]')
plt.subplot(132)
plt.plot(pressure, Rs, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('Rs [m3/Sm3]')
plt.subplot(133)
plt.plot(pressure, oildensity, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('oil density [kg/m3]')
plt.show()




print("swelling test...............")
injectiongas = createfluid('CO2')
relativeoilvolume = []
pressure = []
fluid1.setPressure(100.0)
TPflash(fluid1)
temperature = 301.0
molPercentInjected = [0.0, 1.0, 5.0, 8.0, 10.0, 15.0, 20.0]
swellingtest(fluid1,injectiongas,temperature, molPercentInjected, pressure,relativeoilvolume)

plt.figure()
plt.plot(pressure, relativeoilvolume, "o")
plt.xlabel('Pressure [bara]')
plt.ylabel('swollen volume/initial volume [-]')
plt.show()


