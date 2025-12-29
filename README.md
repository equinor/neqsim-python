![NeqSim Logo](https://github.com/equinor/neqsim/blob/master/docs/wiki/neqsimlogocircleflatsmall.png)

![Run tests](https://github.com/equinor/neqsim-python/actions/workflows/runtests.yml/badge.svg?branch=master)
![Publish package](https://github.com/equinor/neqsim-python/actions/workflows/publish-to-test-pypi.yml/badge.svg?branch=master)

# NeqSim Python

NeqSim Python is part of the [NeqSim project](https://equinor.github.io/neqsimhome/). NeqSim Python is a Python interface to the [NeqSim Java library](https://github.com/equinor/neqsim) for estimation of fluid behavior and process design for oil and gas production. NeqSim Python toolboxes (eg. [thermoTools](https://github.com/equinor/neqsim-python/blob/master/src/neqsim/thermo/thermoTools.py) and [processTools](https://github.com/equinor/neqsim-python/blob/master/src/neqsim/process/processTools.py)) are implemented to streamline use of neqsim in Python. Examples of use are given in the [examples folder](https://github.com/equinor/neqsim-python/tree/master/examples).

## Installation

NeqSim Python can be installed via **pip** or **conda**.

### Using pip

```bash
pip install neqsim
```

### Using Conda

NeqSim is available on conda-forge. Install with:

```bash
conda install -c conda-forge neqsim
```

Or add conda-forge to your channels and install:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install neqsim
```

**Note:** The conda package automatically includes Java (OpenJDK) as a dependency, so no separate Java installation is required.

### Prerequisites

- Python 3.9 or higher
- Java 11 or higher (automatically installed with conda, or install separately for pip)

## Getting Started

See the [NeqSim Python Wiki](https://github.com/equinor/neqsim-python/wiki) for how to use NeqSim Python via Python or in Jupyter notebooks. Also see [examples of use of NeqSim for Gas Processing in Colab](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/examples_of_NeqSim_in_Colab.ipynb#scrollTo=kHt6u-utpvYf). Learn and ask questions in [Discussions for use and development of NeqSim](https://github.com/equinor/neqsim/discussions).

## Process Simulation

NeqSim Python provides multiple ways to build process simulations:

### 1. Python Wrappers (Recommended for beginners)

Simple functions with a global process - great for notebooks and prototyping:

```python
from neqsim.thermo import fluid
from neqsim.process import stream, compressor, separator, runProcess, clearProcess

clearProcess()
feed = fluid('srk')
feed.addComponent('methane', 0.9)
feed.addComponent('ethane', 0.1)
feed.setTemperature(30.0, 'C')
feed.setPressure(50.0, 'bara')
feed.setTotalFlowRate(10.0, 'MSm3/day')

inlet = stream('inlet', feed)
sep = separator('separator', inlet)
comp = compressor('compressor', sep.getGasOutStream(), pres=100.0)
runProcess()

print(f"Compressor power: {comp.getPower()/1e6:.2f} MW")
```

### 2. ProcessContext (Recommended for production)

Context manager with explicit process control - supports multiple independent processes:

```python
from neqsim.thermo import fluid
from neqsim.process import ProcessContext

feed = fluid('srk')
feed.addComponent('methane', 0.9)
feed.addComponent('ethane', 0.1)
feed.setTemperature(30.0, 'C')
feed.setPressure(50.0, 'bara')

with ProcessContext("Compression Train") as ctx:
    inlet = ctx.stream('inlet', feed)
    sep = ctx.separator('separator', inlet)
    comp = ctx.compressor('compressor', sep.getGasOutStream(), pres=100.0)
    ctx.run()
    print(f"Compressor power: {comp.getPower()/1e6:.2f} MW")
```

### 3. ProcessBuilder (Fluent API)

Chainable builder pattern - ideal for configuration-driven design:

```python
from neqsim.thermo import fluid
from neqsim.process import ProcessBuilder

feed = fluid('srk')
feed.addComponent('methane', 0.9)
feed.addComponent('ethane', 0.1)
feed.setTemperature(30.0, 'C')
feed.setPressure(50.0, 'bara')

process = (ProcessBuilder("Compression Train")
    .add_stream('inlet', feed)
    .add_separator('separator', 'inlet')
    .add_compressor('compressor', 'separator', pressure=100.0)
    .run())

print(f"Compressor power: {process.get('compressor').getPower()/1e6:.2f} MW")
```

### 4. Direct Java Access (Full control)

Explicit process management using jneqsim - for advanced features see [neqsim java API](https://github.com/equinor/neqsim):

```python
from neqsim import jneqsim
from neqsim.thermo import fluid

feed = fluid('srk')
feed.addComponent('methane', 0.9)
feed.addComponent('ethane', 0.1)
feed.setTemperature(30.0, 'C')
feed.setPressure(50.0, 'bara')

# Create equipment using Java classes
inlet = jneqsim.process.equipment.stream.Stream('inlet', feed)
sep = jneqsim.process.equipment.separator.Separator('separator', inlet)
comp = jneqsim.process.equipment.compressor.Compressor('compressor', sep.getGasOutStream())
comp.setOutletPressure(100.0)

# Create and run process explicitly
process = jneqsim.process.processmodel.ProcessSystem()
process.add(inlet)
process.add(sep)
process.add(comp)
process.run()

print(f"Compressor power: {comp.getPower()/1e6:.2f} MW")
```

### Choosing an Approach

| Use Case                    | Recommended Approach |
| --------------------------- | -------------------- |
| Learning & prototyping      | Python wrappers      |
| Jupyter notebooks           | Python wrappers      |
| Production applications     | ProcessContext       |
| Multiple parallel processes | ProcessContext       |
| Configuration-driven design | ProcessBuilder       |
| Advanced Java features      | Direct Java access   |

See the [examples folder](https://github.com/equinor/neqsim-python/tree/master/examples) for more process simulation examples, including [processApproaches.py](https://github.com/equinor/neqsim-python/blob/master/examples/processApproaches.py) which demonstrates all four approaches.

## PVT Simulation (PVTsimulation)

NeqSim also includes a `pvtsimulation` package for common PVT experiments (CCE/CME, CVD, differential liberation, separator tests, swelling, viscosity, etc.) and tuning workflows.

- Documentation: `docs/pvt_simulation.md`
- Direct Java access examples: `examples/pvtsimulation/README.md`

## Prerequisites

Java version 8 or higher ([Java JDK](https://adoptium.net/)) needs to be installed. The Python package [JPype](https://github.com/jpype-project/jpype) is used to connect Python and Java. Read the [installation requirements for Jpype](https://jpype.readthedocs.io/en/latest/install.html). Be aware that mixing 64 bit Python with 32 bit Java and vice versa crashes on import of the jpype module. The needed Python packages are listed in the [NeqSim Python dependencies page](https://github.com/equinor/neqsim-python/network/dependencies).

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Discussion forum

Questions related to neqsim can be posted in the [github discussion pages](https://github.com/equinor/neqsim/discussions).

## Versioning

NeqSim use [SemVer](https://semver.org/) for versioning.

## Licence

NeqSim is distributed under the [Apache-2.0](https://github.com/equinor/neqsimsource/blob/master/LICENSE) licence.

## Acknowledgments

A number of master and PhD students at NTNU have contributed to development of NeqSim. We greatly acknowledge their contributions.
