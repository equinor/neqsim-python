# -*- coding: utf-8 -*-
"""
Tune to CME (CCE) relative-volume data
=====================================

This example uses `pvtsimulation.simulation.ConstantMassExpansion` with:

  - `setTemperaturesAndPressures(temps, pressures)`
  - `setExperimentalData([[...relative volumes...]]])`
  - `runTuning()`

NeqSim's CME tuning currently uses the optimizer to adjust plus-fraction properties
(notably plus-fraction molar mass) to better match the experimental relative-volume curve.
"""

from __future__ import annotations

from jpype.types import JDouble

from neqsim import jneqsim
from neqsim.thermo import fluid


def _build_oil_with_plus_fraction():
    oil = fluid("srk")
    oil.addComponent("methane", 50.0)
    oil.addComponent("ethane", 10.0)
    oil.addComponent("propane", 5.0)
    oil.addComponent("n-butane", 5.0)
    oil.addComponent("n-hexane", 10.0)
    oil.addPlusFraction("C20", 20.0, 381.0 / 1000.0, 0.88)

    oil.createDatabase(True)
    oil.setMixingRule(2)
    oil.setMultiPhaseCheck(True)
    oil.useVolumeCorrection(True)
    return oil


def _as_list(java_array) -> list[float]:
    return [float(x) for x in java_array]


def main() -> None:
    run_tuning = False  # set True when tuning against measured CME data

    oil = _build_oil_with_plus_fraction()

    temperature_k = 273.15 + 80.0
    pressures = [400.0, 350.0, 300.0, 250.0, 200.0, 150.0]
    temperatures = [temperature_k] * len(pressures)

    # Example data (replace with lab CCE/CME data aligned with the pressures above).
    # Format expected by NeqSim: double[1][n], i.e. a single row of n data points.
    exp_relative_volume = [0.98, 1.02, 1.08, 1.18, 1.38, 1.80]

    cme = jneqsim.pvtsimulation.simulation.ConstantMassExpansion(oil)
    cme.setTemperature(temperature_k, "K")
    cme.setTemperaturesAndPressures(JDouble[:](temperatures), JDouble[:](pressures))

    cme.runCalc()
    rv_before = _as_list(cme.getRelativeVolume())

    print("CME relativeVolume before tuning:", rv_before)

    if not run_tuning:
        print(
            "Skipping tuning (set `run_tuning = True` to run `ConstantMassExpansion.runTuning`). "
            "Note: tuning convergence depends on data/initial fluid and may fail for some cases."
        )
        return

    cme.setExperimentalData([exp_relative_volume])
    cme.getOptimizer().setMaxNumberOfIterations(10)
    try:
        cme.runTuning()
    except Exception as exc:
        print(f"Tuning failed: {exc}")
        return

    rv_after = _as_list(cme.getRelativeVolume())
    print("CME relativeVolume after tuning: ", rv_after)


if __name__ == "__main__":
    main()
