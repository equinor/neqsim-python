# -*- coding: utf-8 -*-
"""
Tune plus fraction to measured saturation pressure
==================================================

This example uses:
  - `pvtsimulation.simulation.SaturationPressure` to calculate saturation pressure
  - `pvtsimulation.modeltuning.TuneToSaturation` to tune plus-fraction molar mass

Typical use:
  - You have a measured bubble-point (oil) or dew-point (gas condensate) pressure at a given T.
  - You want the NeqSim characterized fluid to match that saturation point before tuning against
    full PVT experiments (CCE/CVD/DL, etc).
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


def main() -> None:
    run_tuning = False  # set True when tuning against measured Psat

    oil = _build_oil_with_plus_fraction()

    measured_temperature_k = 273.15 + 80.0

    sat_before = jneqsim.pvtsimulation.simulation.SaturationPressure(oil.clone())
    sat_before.setTemperature(measured_temperature_k, "K")
    sat_before.run()
    psat_before = float(sat_before.getSaturationPressure())

    # Default target: saturation pressure of the *characterized* version of the same fluid.
    # Replace with lab bubble/dew point (keep reasonably close to the initial model to avoid
    # unrealistic tuned heavy-end properties).
    oil_target = oil.clone()
    oil_target.getCharacterization().characterisePlusFraction()
    oil_target.createDatabase(True)
    oil_target.setMixingRule(2)
    oil_target.setMultiPhaseCheck(True)

    sat_target = jneqsim.pvtsimulation.simulation.SaturationPressure(oil_target)
    sat_target.setTemperature(measured_temperature_k, "K")
    sat_target.run()
    measured_psat_bara = float(sat_target.getSaturationPressure())

    print(f"Psat before tuning: {psat_before:.3f} bara")
    print(f"Psat target:        {measured_psat_bara:.3f} bara")

    if not run_tuning:
        print(
            "Skipping tuning (set `run_tuning = True` to run `TuneToSaturation`). "
            "Note: this is an experimental heuristic and may not converge for all fluids."
        )
        return

    sat_sim = jneqsim.pvtsimulation.simulation.SaturationPressure(oil)
    sat_sim.setTemperature(measured_temperature_k, "K")

    tuning = jneqsim.pvtsimulation.modeltuning.TuneToSaturation(sat_sim)
    tuning.setSaturationConditions(measured_temperature_k, measured_psat_bara)
    tuning.setTunePlusMolarMass(True)
    tuning.setTuneVolumeCorrection(False)
    tuning.run()

    sat_after = jneqsim.pvtsimulation.simulation.SaturationPressure(
        tuning.getSimulation().getThermoSystem()
    )
    sat_after.setTemperature(measured_temperature_k, "K")
    sat_after.run()
    psat_after = float(sat_after.getSaturationPressure())

    print(f"Psat after tuning:  {psat_after:.3f} bara")
    print("Tuned system available as: tuning.getSimulation().getThermoSystem()")


if __name__ == "__main__":
    main()
