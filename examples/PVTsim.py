import matplotlib.pyplot as plt
from neqsim.thermo import (
    CVD,
    TPflash,
    addOilFractions,
    createfluid,
    createfluid2,
    dataFrame,
    fluid,
    fluidcreator,
    phaseenvelope,
    printFrame,
    separatortest,
)

# Calculate and display the phase envelope of various fluid types
fluid1 = createfluid("black oil")
print("phase envelope for black oil")
# phaseenvelope(fluid1, True)

TPflash(fluid1)


pressure = [300.0, 250.0, 200.0, 150.0, 100.0, 50.0, 20.0, 1.01325]
temperature = [345.0, 345.0, 345.0, 345.0, 345.0, 345.0, 345.0, 345.0]

GOR = []
Bo = []
separatortest(fluid1, pressure, temperature, GOR, Bo, display=False)

plt.figure()
plt.plot(pressure, Bo, "o")
plt.xlabel("Pressure [bara]")
plt.ylabel("Bo [m3/Sm3]")
plt.figure()
plt.plot(pressure, GOR, "o")
plt.xlabel("Pressure [bara]")
plt.ylabel("GOR [Sm3/Sm3]")
plt.show()
relativeVolume = []
Zgas = []
temperature = 313.15
CVD(fluid1, pressure, temperature, relativeVolume, Zgas, display=False)
print("rel vol")
print(relativeVolume)
