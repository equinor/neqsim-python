<h1>
  <img src="https://github.com/equinor/neqsim/blob/master/docs/wiki/neqsimlogocircleflatsmall.png" alt="NeqSim Logo" width="120" valign="middle">&nbsp;NeqSim Python
</h1>

<p align="center">
  <strong>Python interface to the NeqSim engine — fluid properties, process simulation, and PVT analysis from Python and Jupyter notebooks.</strong>
</p>

<p align="center">
  <a href="https://github.com/equinor/neqsim-python/actions/workflows/runtests.yml?query=branch%3Amaster"><img src="https://github.com/equinor/neqsim-python/actions/workflows/runtests.yml/badge.svg?branch=master" alt="Tests"></a>
  <a href="https://github.com/equinor/neqsim-python/actions/workflows/publish-to-test-pypi.yml"><img src="https://github.com/equinor/neqsim-python/actions/workflows/publish-to-test-pypi.yml/badge.svg?branch=master" alt="Publish"></a>
  <a href="https://pypi.org/project/neqsim/"><img src="https://img.shields.io/pypi/v/neqsim.svg?label=PyPI" alt="PyPI"></a>
  <a href="https://pypi.org/project/neqsim/"><img src="https://img.shields.io/pypi/pyversions/neqsim.svg" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-process-simulation">Process Simulation</a> ·
  <a href="#-pvt-simulation">PVT Simulation</a> ·
  <a href="#-examples">Examples</a> ·
  <a href="https://equinor.github.io/neqsimhome/">Docs</a> ·
  <a href="https://github.com/equinor/neqsim/discussions">Community</a>
</p>

---

## What is NeqSim Python?

NeqSim Python is part of the [NeqSim project](https://equinor.github.io/neqsimhome/) — a Python interface to the [NeqSim Java library](https://github.com/equinor/neqsim) for estimation of fluid behavior and process design for oil and gas production.

It provides Python toolboxes such as [thermoTools](https://github.com/equinor/neqsim-python/blob/master/src/neqsim/thermo/thermoTools.py) and [processTools](https://github.com/equinor/neqsim-python/blob/master/src/neqsim/process/processTools.py) that streamline the use of NeqSim, plus direct access to the full Java API via the `jneqsim` gateway.

| Capability | What you get |
|------------|-------------|
| **Thermodynamics** | 60+ EOS models (SRK, PR, CPA, GERG-2008, …), flash calculations, phase envelopes |
| **Physical properties** | Density, viscosity, thermal conductivity, surface tension |
| **Process simulation** | 33+ equipment types — separators, compressors, heat exchangers, valves, pumps, reactors |
| **PVT simulation** | CME, CVD, differential liberation, separator tests, swelling, viscosity |
| **Pipeline & flow** | Steady-state multiphase pipe flow (Beggs & Brill), pipe networks |

---

## 🚀 Quick Start

### Install

<table>
<tr><td><strong>pip</strong> (requires Java 11+)</td><td><strong>conda</strong> (Java included)</td></tr>
<tr>
<td>

```bash
pip install neqsim
```

</td>
<td>

```bash
conda install -c conda-forge neqsim
```

</td>
</tr>
</table>

> **Prerequisites:** Python 3.9+ and Java 11+. The conda package automatically installs OpenJDK — no separate Java setup needed. For pip, install Java from [Adoptium](https://adoptium.net/).

### Try it now

```python
from neqsim.thermo import fluid

# Create a natural gas fluid
fl = fluid('srk')
fl.addComponent('methane', 0.85)
fl.addComponent('ethane', 0.10)
fl.addComponent('propane', 0.05)
fl.setTemperature(25.0, 'C')
fl.setPressure(60.0, 'bara')
fl.setMixingRule('classic')

from neqsim.thermo import TPflash, printFrame
TPflash(fl)
printFrame(fl)
```

---

## 🔧 Process Simulation

NeqSim Python provides multiple ways to build process simulations:

<details>
<summary><strong>1. Python Wrappers</strong> — recommended for beginners & notebooks</summary>

Simple functions with a global process — great for prototyping:

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

</details>

<details>
<summary><strong>2. ProcessContext</strong> — recommended for production code</summary>

Context manager with explicit process control — supports multiple independent processes:

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

</details>

<details>
<summary><strong>3. ProcessBuilder</strong> — fluent API for configuration-driven design</summary>

Chainable builder pattern:

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

</details>

<details>
<summary><strong>4. Direct Java Access</strong> — full control via jneqsim</summary>

Explicit process management using the Java API — for advanced features see the [NeqSim Java repo](https://github.com/equinor/neqsim):

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

</details>

### Choosing an Approach

| Use Case | Recommended Approach |
|----------|---------------------|
| Learning & prototyping | Python wrappers |
| Jupyter notebooks | Python wrappers |
| Production applications | ProcessContext |
| Multiple parallel processes | ProcessContext |
| Configuration-driven design | ProcessBuilder |
| Advanced Java features | Direct Java access |

---

## 🧪 PVT Simulation

NeqSim includes a `pvtsimulation` package for common PVT experiments (CCE/CME, CVD, differential liberation, separator tests, swelling, viscosity, etc.) and tuning workflows.

- [PVT simulation documentation](docs/pvt_simulation.md)
- [PVT examples with direct Java access](examples/pvtsimulation/README.md)

---

## 📂 Examples

Explore ready-to-run examples in the [examples folder](https://github.com/equinor/neqsim-python/tree/master/examples):

- Process simulation — [processApproaches.py](https://github.com/equinor/neqsim-python/blob/master/examples/processApproaches.py) (all four approaches)
- Flash calculations, phase envelopes, hydrate prediction
- Compressor trains, heat exchangers, separation processes
- Jupyter notebooks in [examples/jupyter/](https://github.com/equinor/neqsim-python/tree/master/examples/jupyter)
- [Google Colab examples](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/examples_of_NeqSim_in_Colab.ipynb)

---

## ⚙️ Technical Notes

[JPype](https://github.com/jpype-project/jpype) bridges Python and Java. See the [JPype installation guide](https://jpype.readthedocs.io/en/latest/install.html) for platform-specific details. Ensure Python and Java are both 64-bit (or both 32-bit) — mixing architectures will crash on import.

The full list of Python dependencies is on the [dependencies page](https://github.com/equinor/neqsim-python/network/dependencies).

---

## 🏗️ Contributing

We welcome contributions — bug fixes, new examples, documentation improvements, and more.

- [CONTRIBUTING.md](CONTRIBUTING.md) — Code of conduct and PR process
- [NeqSim Python Wiki](https://github.com/equinor/neqsim-python/wiki) — Guides and usage patterns

---

## 📚 Documentation & Resources

| Resource | Link |
|----------|------|
| **NeqSim homepage** | [equinor.github.io/neqsimhome](https://equinor.github.io/neqsimhome/) |
| **Python wiki** | [neqsim-python/wiki](https://github.com/equinor/neqsim-python/wiki) |
| **JavaDoc API** | [JavaDoc](https://equinor.github.io/neqsimhome/javadoc/site/apidocs/index.html) |
| **Discussion forum** | [GitHub Discussions](https://github.com/equinor/neqsim/discussions) |
| **NeqSim Java** | [equinor/neqsim](https://github.com/equinor/neqsim) |
| **MATLAB binding** | [equinor/neqsimmatlab](https://github.com/equinor/neqsimmatlab) |
| **Releases** | [GitHub Releases](https://github.com/equinor/neqsim-python/releases) |

---

## Versioning

NeqSim uses [SemVer](https://semver.org/) for versioning.

## Authors

Even Solbraa (esolbraa@gmail.com), Marlene Louise Lund

NeqSim development was initiated at [NTNU](https://www.ntnu.edu/employees/even.solbraa). A number of master and PhD students have contributed — we greatly acknowledge their contributions.

## License

[Apache-2.0](LICENSE)
