# PVTsimulation examples (direct Java access)

These examples use **direct Java access** (`from neqsim import jneqsim`) for full control of NeqSim's `pvtsimulation` package.

Files:

- `pvt_experiments_java_access.py`: Run common PVT experiments (Psat, CME, CVD, DL, separator test, swelling, viscosity, GOR).
- `pvt_tuning_to_saturation.py`: Tune plus-fraction molar mass to match a measured saturation pressure (bubble/dew point).
- `pvt_tuning_cme.py`: Tune to match experimental CME relative-volume data.
- `pvt_tuning_cvd.py`: Tune to match experimental CVD relative-volume data.
- `pvt_tuning_viscosity.py`: Tune to match experimental viscosity data.
- `fluid_characterization_and_lumping.py`: Typical black-oil characterization workflow (TBP/plus fraction + PVT lumping).

Run:

```bash
python examples/pvtsimulation/pvt_experiments_java_access.py
```

Tuning scripts default to skipping the actual tuning step; set `run_tuning = True` inside the script when you are ready to tune against measured data.
