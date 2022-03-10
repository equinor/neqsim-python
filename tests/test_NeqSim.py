# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 22:24:08 2019

@author: ESOL
"""
from neqsim.neqsimpython import neqsim


def test_Viscosity():
    thermoSystem = neqsim.thermo.system.SystemSrkEos(280.0, 10.0)
    thermoSystem.addComponent("methane", 10.0)
    thermoSystem.addComponent("water", 4.0)

    thermoOps = neqsim.thermodynamicOperations.ThermodynamicOperations(
        thermoSystem)
    thermoOps.TPflash()

    gasEnthalpy = thermoSystem.getPhase(0).getEnthalpy()
    assert abs(1079.4821290144278 - gasEnthalpy) < 1e-10

    thermoSystem.initPhysicalProperties("Viscosity")
    gasViscosity = thermoSystem.getPhase(0).getViscosity("kg/msec")
    assert abs(1.0760998263783299e-05 - gasViscosity) < 1e-10
