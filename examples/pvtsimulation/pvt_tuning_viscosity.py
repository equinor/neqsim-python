# -*- coding: utf-8 -*-
"""
Tune to viscosity data
=====================

This example uses `pvtsimulation.simulation.ViscositySim` with:

  - `setTemperaturesAndPressures(temps, pressures)`
  - `setExperimentalData([[...viscosity...]]])`
  - `runTuning()`

Replace the example data with your measured viscosities.
"""

from __future__ import annotations

from jpype.types import JDouble

from neqsim import jneqsim
from neqsim.thermo import fluid


def _build_oil_for_viscosity():
    oil = fluid("srk")
    oil.addComponent("n-heptane", 6.78)
    oil.addPlusFraction("C20", 10.62, 381.0 / 1000.0, 0.88)
    oil.getCharacterization().characterisePlusFraction()
    oil.createDatabase(True)
    oil.setMixingRule(2)
    oil.setMultiPhaseCheck(True)
    oil.useVolumeCorrection(True)
    return oil


def _as_list(java_array) -> list[float]:
    return [float(x) for x in java_array]


def main() -> None:
    run_tuning = False  # set True when tuning against measured viscosities

    oil = _build_oil_for_viscosity()

    temperatures_k = [300.15, 293.15, 283.15, 273.15]
    pressures_bara = [5.0, 5.0, 5.0, 5.0]

    # Example viscosity data in Pa*s (replace with lab values).
    exp_viscosity = [2.0e-4, 2.8e-4, 4.0e-4, 5.5e-4]

    visc = jneqsim.pvtsimulation.simulation.ViscositySim(oil)
    visc.setTemperaturesAndPressures(
        JDouble[:](temperatures_k), JDouble[:](pressures_bara)
    )
    visc.runCalc()
    mu_before = _as_list(visc.getOilViscosity())

    print("oil viscosity before tuning [Pa*s]:", mu_before)

    if not run_tuning:
        print(
            "Skipping tuning (set `run_tuning = True` to run `ViscositySim.runTuning`). "
            "Note: tuning convergence depends on data/initial fluid and may fail for some cases."
        )
        return

    visc.setExperimentalData([exp_viscosity])
    visc.getOptimizer().setMaxNumberOfIterations(20)
    try:
        visc.runTuning()
    except Exception as exc:
        print(f"Tuning failed: {exc}")
        return
    visc.runCalc()
    mu_after = _as_list(visc.getOilViscosity())

    print("oil viscosity after tuning  [Pa*s]:", mu_after)


if __name__ == "__main__":
    main()
