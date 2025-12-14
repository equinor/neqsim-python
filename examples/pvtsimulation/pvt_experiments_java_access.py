# -*- coding: utf-8 -*-
"""
PVTsimulation experiments (direct Java access)
============================================

This script demonstrates NeqSim's PVTsimulation package using direct Java access:

    from neqsim import jneqsim

Covered experiments (typical PVT lab / reservoir studies):
  - Saturation pressure (bubble/dew point): SaturationPressure
  - Constant mass expansion (CCE/CME): ConstantMassExpansion
  - Constant volume depletion (CVD): ConstantVolumeDepletion
  - Differential liberation (DL): DifferentialLiberation
  - Separator test: SeparatorTest
  - Swelling test: SwellingTest
  - Viscosity study: ViscositySim
  - GOR / Bo vs pressure: GOR

Notes:
  - NeqSim pressures are in bara (bar absolute) unless you explicitly manage units.
  - Temperatures here are in Kelvin when passed to PVTsimulation classes.
  - For simpler usage, see wrapper functions in `neqsim.thermo.thermoTools`.
"""

from __future__ import annotations

from jpype.types import JDouble

from neqsim import jneqsim
from neqsim.thermo import TPflash, fluid


def _as_list(java_array) -> list[float]:
    return [float(x) for x in java_array]


def _build_oil_for_pvt_experiments():
    oil = fluid("srk")
    oil.addComponent("methane", 50.0)
    oil.addComponent("ethane", 10.0)
    oil.addComponent("propane", 5.0)
    oil.addComponent("n-butane", 5.0)
    oil.addComponent("n-hexane", 10.0)
    oil.addPlusFraction("C20", 20.0, 381.0 / 1000.0, 0.88)

    oil.createDatabase(True)
    oil.setMixingRule(2)  # "classic" (kij from DB)
    oil.setMultiPhaseCheck(True)
    oil.useVolumeCorrection(True)
    return oil


def main() -> None:
    oil = _build_oil_for_pvt_experiments()

    reservoir_temperature_k = 273.15 + 100.0
    oil.setTemperature(reservoir_temperature_k)
    oil.setPressure(250.0)
    TPflash(oil)

    print("\n--- Saturation pressure ---")
    sat = jneqsim.pvtsimulation.simulation.SaturationPressure(oil.clone())
    sat.setTemperature(reservoir_temperature_k, "K")
    sat.run()
    psat = float(sat.getSaturationPressure())
    print(f"Psat @ {reservoir_temperature_k:.2f} K: {psat:.3f} bara")

    pressures = [400.0, 350.0, 300.0, 250.0, 200.0, 150.0, 100.0, 50.0]
    temperatures = [reservoir_temperature_k] * len(pressures)

    print("\n--- Constant Mass Expansion (CCE/CME) ---")
    cme = jneqsim.pvtsimulation.simulation.ConstantMassExpansion(oil.clone())
    cme.setTemperaturesAndPressures(JDouble[:](temperatures), JDouble[:](pressures))
    cme.setTemperature(reservoir_temperature_k, "K")
    cme.runCalc()
    print("relativeVolume:", _as_list(cme.getRelativeVolume()))
    print("liquidRelativeVolume:", _as_list(cme.getLiquidRelativeVolume()))
    print("Yfactor:", _as_list(cme.getYfactor()))
    print("isoThermalCompressibility [1/bar]:", _as_list(cme.getIsoThermalCompressibility()))

    print("\n--- Constant Volume Depletion (CVD) ---")
    cvd = jneqsim.pvtsimulation.simulation.ConstantVolumeDepletion(oil.clone())
    cvd.setPressures(JDouble[:](pressures))
    cvd.setTemperature(reservoir_temperature_k, "K")
    cvd.runCalc()
    print("relativeVolume:", _as_list(cvd.getRelativeVolume()))
    print("liquidRelativeVolume:", _as_list(cvd.getLiquidRelativeVolume()))
    print("cummulativeMolePercDepleted [%]:", _as_list(cvd.getCummulativeMolePercDepleted()))

    print("\n--- Differential Liberation (DL) ---")
    dl = jneqsim.pvtsimulation.simulation.DifferentialLiberation(oil.clone())
    dl.setPressures(JDouble[:](pressures + [1.01325]))
    dl.setTemperature(reservoir_temperature_k, "K")
    dl.runCalc()
    print("Bo [m3/Sm3]:", _as_list(dl.getBo()))
    print("Rs [Sm3/Sm3]:", _as_list(dl.getRs()))
    print("oilDensity [kg/m3]:", _as_list(dl.getOilDensity()))

    print("\n--- Separator test ---")
    sep_pressures = [50.0, 10.0, 1.01325]
    sep_temperatures = [313.15, 303.15, 293.15]
    sep = jneqsim.pvtsimulation.simulation.SeparatorTest(oil.clone())
    sep.setSeparatorConditions(JDouble[:](sep_temperatures), JDouble[:](sep_pressures))
    sep.runCalc()
    print("separator GOR [Sm3/Sm3]:", _as_list(sep.getGOR()))
    print("separator Bo [m3/Sm3]:", _as_list(sep.getBofactor()))

    print("\n--- Swelling test ---")
    injection_gas = fluid("srk")
    injection_gas.addComponent("CO2", 100.0)
    injection_gas.createDatabase(True)
    injection_gas.setMixingRule(2)

    mol_percent_injected = [0.0, 1.0, 5.0, 10.0, 20.0]
    swell = jneqsim.pvtsimulation.simulation.SwellingTest(oil.clone())
    swell.setInjectionGas(injection_gas)
    swell.setTemperature(reservoir_temperature_k, "K")
    swell.setCummulativeMolePercentGasInjected(JDouble[:](mol_percent_injected))
    swell.runCalc()
    print("swell pressures [bara]:", _as_list(swell.getPressures()))
    print("relativeOilVolume [-]:", _as_list(swell.getRelativeOilVolume()))

    print("\n--- Viscosity study ---")
    visc = jneqsim.pvtsimulation.simulation.ViscositySim(oil.clone())
    visc.setTemperaturesAndPressures(JDouble[:](temperatures), JDouble[:](pressures))
    visc.runCalc()
    print("oilViscosity [Pa*s]:", _as_list(visc.getOilViscosity()))
    print("gasViscosity [Pa*s]:", _as_list(visc.getGasViscosity()))

    print("\n--- GOR / Bo vs pressure ---")
    gor = jneqsim.pvtsimulation.simulation.GOR(oil.clone())
    gor.setTemperaturesAndPressures(JDouble[:](temperatures), JDouble[:](pressures))
    gor.runCalc()
    print("GOR [Sm3/Sm3]:", _as_list(gor.getGOR()))
    print("Bo [m3/Sm3]:", _as_list(gor.getBofactor()))

    print("\nDone.")


if __name__ == "__main__":
    main()
