# PVTsimulation (PVT experiments, characterization, tuning)

NeqSim’s `pvtsimulation` package contains common PVT laboratory experiments (CCE/CME, CVD, DL, separator tests, swelling, viscosity, etc.) and utilities for tuning fluid characterization to match measured data.

This repository supports two ways of running these experiments from Python:

1. **Python wrappers** in `neqsim.thermo` / `neqsim.thermo.thermoTools` (quickest)
2. **Direct Java access** via `from neqsim import jneqsim` (full control, more outputs, tuning)

## Experiment coverage

| Experiment | Java class | Python wrapper | Example |
| --- | --- | --- | --- |
| Saturation pressure (bubble/dew point) | `jneqsim.pvtsimulation.simulation.SaturationPressure` | `neqsim.thermo.saturationpressure()` | `examples/pvtsimulation/pvt_experiments_java_access.py`, `examples/pvtsimulation/pvt_tuning_to_saturation.py` |
| Constant mass expansion (CCE/CME) | `...ConstantMassExpansion` | `neqsim.thermo.CME()` | `examples/pvtsimulation/pvt_experiments_java_access.py`, `examples/pvtsimulation/pvt_tuning_cme.py` |
| Constant volume depletion (CVD) | `...ConstantVolumeDepletion` | `neqsim.thermo.CVD()` | `examples/pvtsimulation/pvt_experiments_java_access.py`, `examples/pvtsimulation/pvt_tuning_cvd.py` |
| Differential liberation (DL) | `...DifferentialLiberation` | `neqsim.thermo.difflib()` | `examples/pvtsimulation/pvt_experiments_java_access.py` |
| Separator test | `...SeparatorTest` | `neqsim.thermo.separatortest()` | `examples/pvtsimulation/pvt_experiments_java_access.py` |
| Swelling test | `...SwellingTest` | `neqsim.thermo.swellingtest()` | `examples/pvtsimulation/pvt_experiments_java_access.py` |
| Viscosity | `...ViscositySim` | `neqsim.thermo.viscositysim()` | `examples/pvtsimulation/pvt_experiments_java_access.py`, `examples/pvtsimulation/pvt_tuning_viscosity.py` |
| GOR / Bo | `...GOR` | `neqsim.thermo.GOR()` | `examples/pvtsimulation/pvt_experiments_java_access.py` |

Other available simulations (direct Java access):

- `jneqsim.pvtsimulation.simulation.WaxFractionSim` (wax appearance / wax fraction vs T,P; requires wax model setup)
- `jneqsim.pvtsimulation.simulation.ViscosityWaxOilSim` (wax + viscosity)
- `jneqsim.pvtsimulation.simulation.DensitySim`
- `jneqsim.pvtsimulation.simulation.SlimTubeSim` (slim-tube style displacement simulation)

## Direct Java access: key patterns

### Passing arrays

Many PVTsimulation methods expect Java `double[]`. With JPype you can pass:

- A Python list (often auto-converted), or
- An explicit `double[]` using `jpype.types.JDouble[:]`

Example:

```python
from jpype.types import JDouble
from neqsim import jneqsim

pressures = [400.0, 300.0, 200.0]
temperatures = [373.15, 373.15, 373.15]

cme = jneqsim.pvtsimulation.simulation.ConstantMassExpansion(oil)
cme.setTemperaturesAndPressures(JDouble[:](temperatures), JDouble[:](pressures))
cme.runCalc()
```

### Experimental data for tuning

For several experiments, NeqSim expects `double[1][n]` experimental data, i.e. a single row with `n` values aligned with your pressure/temperature points:

```python
cme.setExperimentalData([[0.98, 1.02, 1.10]])  # relative volume values
cme.runTuning()
```

## Fluid characterization + PVT lumping

See `examples/pvtsimulation/fluid_characterization_and_lumping.py` for a typical black-oil characterization workflow using:

- `addTBPfraction(...)` and `addPlusFraction(...)`
- `getCharacterization().setLumpingModel("PVTlumpingModel")`
- `getCharacterization().characterisePlusFraction()`

## Run the examples

```bash
python examples/pvtsimulation/pvt_experiments_java_access.py
python examples/pvtsimulation/pvt_tuning_to_saturation.py
python examples/pvtsimulation/pvt_tuning_cme.py
python examples/pvtsimulation/pvt_tuning_cvd.py
python examples/pvtsimulation/pvt_tuning_viscosity.py
```

Tuning scripts default to skipping the actual tuning step; set `run_tuning = True` inside the script when you are ready to tune against measured data.
