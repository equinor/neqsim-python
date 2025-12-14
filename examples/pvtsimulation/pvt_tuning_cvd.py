# -*- coding: utf-8 -*-
"""
Tune to CVD relative-volume data
===============================

This example uses `pvtsimulation.simulation.ConstantVolumeDepletion` with:

  - `setTemperaturesAndPressures(temps, pressures)` (for tuning)
  - `setExperimentalData([[...relative volumes...]]])`
  - `runTuning()`

Replace the example data with your lab CVD relative volumes aligned with the pressures.
"""

from __future__ import annotations

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
    run_tuning = False  # set True when tuning against measured CVD data

    oil = _build_oil_with_plus_fraction()

    temperature_k = 273.15 + 80.0
    pressures = [400.0, 350.0, 300.0, 250.0, 200.0, 150.0, 100.0]
    temperatures = [temperature_k] * len(pressures)

    exp_relative_volume = [0.96, 0.98, 1.00, 1.05, 1.15, 1.30, 1.60]

    cvd = jneqsim.pvtsimulation.simulation.ConstantVolumeDepletion(oil)
    cvd.setTemperature(temperature_k, "K")
    cvd.setTemperaturesAndPressures(temperatures, pressures)

    cvd.runCalc()
    rv_before = _as_list(cvd.getRelativeVolume())

    print("CVD relativeVolume before tuning:", rv_before)

    if not run_tuning:
        print(
            "Skipping tuning (set `run_tuning = True` to run `ConstantVolumeDepletion.runTuning`). "
            "Note: tuning convergence depends on data/initial fluid and may fail for some cases."
        )
        return

    cvd.setExperimentalData([exp_relative_volume])
    cvd.getOptimizer().setMaxNumberOfIterations(20)
    try:
        cvd.runTuning()
    except Exception as exc:
        print(f"Tuning failed: {exc}")
        return

    rv_after = _as_list(cvd.getRelativeVolume())
    print("CVD relativeVolume after tuning: ", rv_after)


if __name__ == "__main__":
    main()
