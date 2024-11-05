![NeqSim Logo](https://github.com/equinor/neqsim/blob/master/docs/wiki/neqsimlogocircleflatsmall.png)

![Run tests](https://github.com/equinor/neqsim-python/actions/workflows/runtests.yml/badge.svg?branch=master)
![Publish package](https://github.com/equinor/neqsim-python/actions/workflows/publish-to-test-pypi.yml/badge.svg?branch=master)

# NeqSim Python

NeqSim Python is part of the [NeqSim project](https://equinor.github.io/neqsimhome/). NeqSim Python is a Python interface to the [NeqSim Java library](https://github.com/equinor/neqsim) for estimation of fluid behavior and process design for oil and gas production. NeqSim Python toolboxes (eg. [thermoTools](https://github.com/equinor/neqsimpython/blob/master/neqsim/thermo/thermoTools.py) and [processTools](https://github.com/equinor/neqsimpython/blob/master/neqsim/process/processTools.py)) are implemented to streamline use of neqsim in Python. Examples of use are given in the [examples folder](https://github.com/equinor/neqsim-python/tree/master/examples).

## Releases

NeqSim Python is distributed as a pip package. Please read the [Prerequisites](#prerequisites).

End-users should install neqsim python with some additional packages by running
```
pip install neqsim
```

## Getting Started

See the [NeqSim Python Wiki](https://github.com/equinor/neqsimpython/wiki) for how to use NeqSim Python via Python or in Jupyter notebooks. Also see [examples of use of NeqSim for Gas Processing in Colab](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/examples_of_NeqSim_in_Colab.ipynb#scrollTo=kHt6u-utpvYf). Learn and ask questions in [Discussions for use and development of NeqSim](https://github.com/equinor/neqsim/discussions).

### Prerequisites

Java version 8 or higher ([Java JDK](https://adoptium.net/)) needs to be installed. The Python package [JPype](https://github.com/jpype-project/jpype) is used to connect Python and Java. Read the [installation requirements for Jpype](https://jpype.readthedocs.io/en/latest/install.html). Be aware that mixing 64 bit Python with 32 bit Java and vice versa crashes on import of the jpype module. The needed Python packages are listed in the [NeqSim Python dependencies page](https://github.com/equinor/neqsimpython/network/dependencies).


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
