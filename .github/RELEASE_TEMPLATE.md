# NeqSim Python <version>

NeqSim Python is the Python interface to the NeqSim engine for thermodynamic calculations, physical properties, process simulation, and PVT analysis from Python and Jupyter notebooks.

## Highlights

- <Main user-facing change or engine update.>
- <Important fix or compatibility improvement.>
- <Packaging, documentation, or maintenance note if relevant.>

## Install

Use pip when you already have Java installed:

```bash
pip install --upgrade neqsim==<version>
```

Use conda when you want OpenJDK installed with the package:

```bash
conda install -c conda-forge neqsim=<version>
```

Requirements:

- Python 3.9 or newer.
- Java 8 or newer for pip installs.
- Conda installs include OpenJDK through conda-forge.

Verify the installed package version without starting the JVM:

```bash
python -c "from importlib.metadata import version; print(version('neqsim'))"
```

## Quick Start

```python
from neqsim.thermo import TPflash, fluid, printFrame

natural_gas = fluid("srk")
natural_gas.addComponent("methane", 0.85)
natural_gas.addComponent("ethane", 0.10)
natural_gas.addComponent("propane", 0.05)
natural_gas.setTemperature(25.0, "C")
natural_gas.setPressure(60.0, "bara")
natural_gas.setMixingRule("classic")

TPflash(natural_gas)
printFrame(natural_gas)
```

## Useful Links

- Full changelog: https://github.com/equinor/neqsim-python/compare/v<previous-version>...v<version>
- Documentation: https://equinor.github.io/neqsimhome/
- Python examples: https://github.com/equinor/neqsim-python/tree/master/examples
- Java engine: https://github.com/equinor/neqsim
- Discussions: https://github.com/equinor/neqsim/discussions

## Maintainer Checklist

- Confirm `pyproject.toml` and `conda/meta.yaml` use this version.
- Confirm bundled JAR files match this version for each supported Java runtime.
- Run the relevant tests or packaging checks before publishing.
- Publish the GitHub release only when ready to trigger the PyPI release workflow.
