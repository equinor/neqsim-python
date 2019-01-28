from py4j.java_gateway import JavaGateway
neqsim =  JavaGateway().jvm.neqsim
ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations

def fluid(name='srk', temperature=298.15, pressure=1.01325):
       if name=='srk':
                system = neqsim.thermo.system.SystemSrkEos(temperature, pressure)
       elif name=='SRK-EoS':
                system = neqsim.thermo.system.SystemSrkEos(temperature, pressure)
       elif name=='Psrk-EoS':
                system = neqsim.thermo.system.SystemPsrkEos(temperature, pressure)
       elif name=='PSRK-EoS':
                system = neqsim.thermo.system.SystemPsrkEos(temperature, pressure)
       elif name=='RK-EoS':
                system = neqsim.thermo.system.SystemRKEos(temperature, pressure)
       elif name=='pr':
                system = neqsim.thermo.system.SystemPrEos(temperature, pressure)
       elif name=='PR-EoS':
                system = neqsim.thermo.system.SystemPrEos(temperature, pressure)
       elif name=='srk-s':
                system = neqsim.thermo.system.SystemSrkSchwartzentruberEos(temperature, pressure)
       elif name=='GERG-water':
                system = neqsim.thermo.system.SystemGERGwaterEos(temperature, pressure)
       elif name=='SRK-MC':
                system = neqsim.thermo.system.SystemSrkMathiasCopeman(temperature, pressure)
       elif name=='PR-MC':
                system = neqsim.thermo.system.SystemPrMathiasCopeman(temperature, pressure)
       elif name=='scrk':
                system = neqsim.thermo.system.SystemSrkSchwartzentruberEos(temperature, pressure)
       elif name=='ScRK-EoS':
                system = neqsim.thermo.system.SystemSrkSchwartzentruberEos(temperature, pressure)
       elif name=='nrtl':
                system = neqsim.thermo.system.SystemNRTL(temperature, pressure)
       elif name=='unifac':
                system = neqsim.thermo.system.SystemUNIFAC(temperature, pressure)
       elif name=='electrolyte':
                system = neqsim.thermo.system.SystemFurstElectrolyteEos(temperature, pressure)
       elif name=='Electrolyte-ScRK-EoS':
                system = neqsim.thermo.system.SystemFurstElectrolyteEos(temperature, pressure)
       elif name=='Electrolyte-CPA-EoS':
                system = neqsim.thermo.system.SystemElectrolyteCPA(temperature, pressure)
       elif name=='cpa-el':
                system = neqsim.thermo.system.SystemElectrolyteCPA(temperature, pressure)
       elif name=='cpa-s':
                system = neqsim.thermo.system.SystemSrkCPAs(temperature, pressure)
       elif name=='cpa-statoil':
                system = neqsim.thermo.system.SystemSrkCPAstatoil(temperature, pressure)
       elif name=='CPA-SRK-EoS':
                system = neqsim.thermo.system.SystemSrkCPA(temperature, pressure)
       elif name=='cpa-srk':
                system = neqsim.thermo.system.SystemSrkCPA(temperature, pressure)
       elif name=='srk-twoCoon':
                system = neqsim.thermo.system.SystemSrkTwuCoonParamEos(temperature, pressure)
       elif name=='cpa-pr':
                system = neqsim.thermo.system.SystemPrCPA(temperature, pressure)
       elif name=='CPA-PR-EoS':
                system = neqsim.thermo.system.SystemPrCPA(temperature, pressure)
       else:
                print('thermo method: ',name,' not defined . Continue with default method SRK-EOS')
                system = neqsim.thermo.system.SystemSrkEos(temperature, pressure)
       return system

def newdatabase(system):
        system.createDatabase(1)

def volumecorrection(system, use=1):
        system.useVolumeCorrection(use)

def write(system, filename, newfile=0):
        system.write(filename,filename,newfile)

def appenddatabase(system):
        system.createDatabase(0)        
       
def show(system):
        system.display()

def showPDF(system):
        system.generatePDF()
        system.displayPDF()
       
def addComponent(thermoSystem, name, moles, unit="no", phase=-10):
        if phase==-10 and unit=="no":
                thermoSystem.addComponent(name, moles)
        elif phase==-10:
                thermoSystem.addComponent(name, moles, unit)
        elif unit=="no":
                thermoSystem.addComponent(name, moles, phase)
        else:
                thermoSystem.addComponent(name, moles, unit, phase)
        
def temperature(thermoSystem, temp, phase=-1):
         if phase==-1:
                thermoSystem.setTemperature(temp)
         else:
                thermoSystem.getPhase(phase).setTemperature(temp)
                
def pressure(thermoSystem, pres, phase=-1):
        if phase==-1:
                thermoSystem.setPressure(pres)
        else:
                thermoSystem.getPhase(phase).setPressure(pres)

def reactionCheck(thermoSystem):
        thermoSystem.chemicalReactionInit()

def mixingRule(thermoSystem, mixRule='classic', GEmodel=''):
        if GEmodel=='':
                thermoSystem.setMixingRule(mixRule)
        else:
                thermoSystem.setMixingRule(mixRule, GEmodel)
        
def multiphase(testSystem, multiphase=1):
        testSystem.setMultiPhaseCheck(multiphase)

def solidcheck(testSystem, solid=1):
        testSystem.setSolidPhaseCheck(solid)
        
def solid(testSystem, solid=1):
        testSystem.setSolidPhaseCheck(solid)
       
def TPflash(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.TPflash()
        testSystem.init(3)

def TPsolidflash(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.TPSolidflash()
        
def PHflash(testSystem, enthalpy):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.PHflash(enthalpy,0)

def PSflash(testSystem, entropy):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.PSflash(entropy)

def freeze(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.freezingPointTemperatureFlash()

def hydp(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.hydrateFormationPressure()

def hydt(testSystem, type):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.hydrateFormationTemperature(type)
        return testSystem.getTemperature()
             
def bubp(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        try:
                testFlash.bubblePointPressureFlash(0)
        except:
                print('error calculating bublepoint')
        return testSystem.getPressure()
            
        
def bubt(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        try:
                testFlash.bubblePointTemperatureFlash()
        except:
                print('error calculating bublepoint')
        return testSystem.getTemperature()

def dewp(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        try:
                testFlash.dewPointPressureFlash()
        except:
                print('error could not calculate')
        return testSystem.getPressure()
        
def dewt(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        try:
                testFlash.dewPointTemperatureFlash()
        except:
                print('error could not calculate')
        return testSystem.getTemperature()

def waterdewt(testSystem):
        testFlash = ThermodynamicOperations(testSystem)
        try:
                testFlash.waterDewPointTemperatureFlash()
        except:
                print('error could not calculate')
        return testSystem.getTemperature()

def phaseenvelope(testSystem,i=1):
        testFlash = ThermodynamicOperations(testSystem)
        testFlash.calcPTphaseEnvelope(i)
        return testFlash
        
def getExtThermProp(function, thermoSystem, t=0, p=0):
        nargout=[0,0,0,0]
        if t!=0:   
                thermoSystem.setTemperature(t)
                if p!=0:
                        thermoSystem.setPressure(p)
                TPflash(thermoSystem)
        thermoSystem.init(3)
        nargout[0] = function[0]()/thermoSystem.getNumberOfMoles()
        if(thermoSystem.getNumberOfPhases()==1):
                if(thermoSystem.getPhase(0).getPhaseType==1):
                        nargout[1] = function[1]()/thermoSystem.getPhase(0).getNumberOfMolesInPhase()
                        nargout[2] = 0
                else:
                        nargout[2] = function[1]()/thermoSystem.getPhase(0).getNumberOfMolesInPhase()
                        nargout[1] = 0
        else:
                nargout[1] = function[1]()/thermoSystem.getPhase(0).getNumberOfMolesInPhase()
                nargout[2] = function[2]()/thermoSystem.getPhase(1).getNumberOfMolesInPhase()

        nargout[3]=thermoSystem.getNumberOfPhases()
        return nargout


def getIntThermProp(function, thermoSystem, t=0, p=0):
        nargout=[0,0,0,0]
        if t!=0:   
                thermoSystem.setTemperature(t)
                if p!=0:
                        thermoSystem.setPressure(p)
                TPflash(thermoSystem)
        thermoSystem.init(3)
        nargout[0] = function[0]()
        if(thermoSystem.getNumberOfPhases()==1):
                if(thermoSystem.getPhase(0).getPhaseType==1):
                        nargout[1] = function[1]()
                        nargout[2] = 0
                else:
                        nargout[2] = function[1]()
                        nargout[1] = 0
        else:
                nargout[1] = function[1]()
                nargout[2] = function[2]()

        nargout[3]=thermoSystem.getNumberOfPhases()
        return nargout

def getPhysProp(function, thermoSystem, t=0, p=0):
        nargout=[0,0,0,0]
        if t!=0:   
                thermoSystem.setTemperature(t)
                if p!=0:
                        thermoSystem.setPressure(p)
                TPflash(thermoSystem)
        thermoSystem.init(3)
        thermoSystem.initPhysicalProperties()    
        nargout[0] = function[0]()
        if(thermoSystem.getNumberOfPhases()==1):
                if(thermoSystem.getPhase(0).getPhaseType==1):
                        nargout[1] = function[1]()
                        nargout[2] = 0
                else:
                        nargout[2] = function[1]()
                        nargout[1] = 0
        else:
                nargout[1] = function[1]()
                nargout[2] = function[2]()

        nargout[3]=thermoSystem.getNumberOfPhases()
        return nargout
        
 
        
        
def enthalpy(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getEnthalpy)
        func.append(thermoSystem.getPhase(0).getEnthalpy)
        func.append(thermoSystem.getPhase(1).getEnthalpy)
        return getExtThermProp(func,thermoSystem,t,p)
        
        
def entropy(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getEntropy)
        func.append(thermoSystem.getPhase(0).getEntropy)
        func.append(thermoSystem.getPhase(1).getEntropy)
        return getExtThermProp(func,thermoSystem,t,p)
        
def molvol(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getMolarVolume)
        func.append(thermoSystem.getPhase(0).getMolarVolume)
        func.append(thermoSystem.getPhase(1).getMolarVolume)
        return getIntThermProp(func,thermoSystem,t,p)

def energy(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getInternalEnergy)
        func.append(thermoSystem.getPhase(0).getInternalEnergy)
        func.append(thermoSystem.getPhase(1).getInternalEnergy)
        return getExtThermProp(func,thermoSystem,t,p)
        
def gibbsenergy(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getGibbsEnergy)
        func.append(thermoSystem.getPhase(0).getGibbsEnergy)
        func.append(thermoSystem.getPhase(1).getGibbsEnergy)
        return getExtThermProp(func,thermoSystem,t,p)     

def helmholtzenergy(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getHelmholtzEnergy)
        func.append(thermoSystem.getPhase(0).getHelmholtzEnergy)
        func.append(thermoSystem.getPhase(1).getHelmholtzEnergy)
        return getExtThermProp(func,thermoSystem,t,p)   
        
def molefrac(thermoSystem, comp, t=0, p=0):
        func = []
        func.append(thermoSystem.getPhase(0).getComponent(comp).getz)
        func.append(thermoSystem.getPhase(0).getComponent(comp).getx)
        func.append(thermoSystem.getPhase(1).getComponent(comp).getx)
        return getIntThermProp(func,thermoSystem,t,p) 
 
def moles(thermoSystem, phase=0):
        if phase==0: 
                return thermoSystem.getNumberOfMoles() 
        else:
                return thermoSystem.getPhase(phase).getNumberOfMolesInPhase()
        
def beta(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getBeta)
        func.append(thermoSystem.getPhase(0).getBeta)
        func.append(thermoSystem.getPhase(1).getBeta)
        return getIntThermProp(func,thermoSystem,t,p)
        
def molarmass(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getMolarMass)
        func.append(thermoSystem.getPhase(0).getMolarMass)
        func.append(thermoSystem.getPhase(1).getMolarMass)
        return getIntThermProp(func,thermoSystem,t,p) 

def Z(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getZ)
        func.append(thermoSystem.getPhase(0).getZ)
        func.append(thermoSystem.getPhase(1).getZ)
        return getIntThermProp(func,thermoSystem,t,p) 
                
def density(thermoSystem, volcor=1,t=0, p=0):
        func = []
        func.append(thermoSystem.getDensity)
        if volcor==1:
                thermoSystem.initPhysicalProperties()
                func.append(thermoSystem.getPhase(0).getPhysicalProperties().getDensity)
                func.append(thermoSystem.getPhase(1).getPhysicalProperties().getDensity)
        else:
                func.append(thermoSystem.getPhase(0).getDensity)
                func.append(thermoSystem.getPhase(1).getDensity)
        return getPhysProp(func,thermoSystem,t,p)
        
def viscosity(thermoSystem, t=0, p=0):
        func = []
        func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
        func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
        func.append(thermoSystem.getPhase(1).getPhysicalProperties().getViscosity)
        return getPhysProp(func,thermoSystem,t,p)

