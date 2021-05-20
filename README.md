# NeqSim Python
NeqSim Python is part of the [NeqSim project](https://equinor.github.io/neqsimhome/). NeqSim Python is a Python interface to the [NeqSim Java library](https://github.com/equinor/neqsim) for estimation of fluid behavior and process design for oil and gas production. NeqSim Python toolboxes (eg. [thermoTools](https://github.com/equinor/neqsimpython/blob/master/src/neqsim/thermo/thermoTools.py) and [processTools](https://github.com/equinor/neqsimpython/blob/master/src/neqsim/process/processTools.py)) are implemented to streamline use of neqsim in Python. Examples of use are given in jupyter workbooks.

## Releases
The NeqSim Python package is distributed as a pip package. See the [Wiki](https://github.com/equinor/neqsimpython/wiki) for instructions on how to use it. Install the package by running
>pip install neqsim

## Getting Started
See the [NeqSim Python Wiki](https://github.com/equinor/neqsimpython/wiki) for how to use NeqSim Python via Python or in Jupyter notebooks. Also see [examples of use of NeqSim for Gas Processing in Colab](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/examples_of_NeqSim_in_Colab.ipynb#scrollTo=kHt6u-utpvYf). Learn and ask questions in [Discussions for use and development of NeqSim](https://github.com/equinor/neqsim/discussions). 

### Prerequisites
A Java run time environment ([Java JRE](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)) needs to be installed. The Python package [JPype](https://github.com/jpype-project/jpype) is used to connect Python and Java. Read the [installation requirements for Jpype](https://jpype.readthedocs.io/en/latest/install.html). Be aware that mixing 64 bit Python with 32 bit Java and vice versa crashes on import of the jpype module. The needed Python packages are listed in the [NeqSim Python dependencies page](https://github.com/equinor/neqsimpython/network/dependencies).

### Initial setup
The NeqSim Python package is installed by downloading/cloning the library to your local computer (alternatively fork it to your private reprository). The following commands are dependent on a local installation of [GIT](https://git-scm.com/). |pypidownloads| |pypiversion| 

```bash
git clone https://github.com/equinor/neqsimpython.git
cd neqsimpython
pip install .
```
## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## NeqSim Slack collaboration hub
Discussions related to NeqSim development and use is done using [Slack for NeqSim](https://neqsim.slack.com). 
Use the [invitation link](https://join.slack.com/t/neqsim/shared_invite/enQtNjU1ODQ1MDQyMjEzLWU5MWEyNDA3YTlmNThmMGQ1OGMyODgzYzdlZTM5NTVjNDMzOGIyOTU4MTYwNzZkNmZiNDczZjBjMGZkNzlkZTE) to join the group.

## Discussion forum
Questions related to neqsim can be posted in the [github discussion pages](https://github.com/equinor/neqsim/discussions).

## Versioning
NeqSim use [SemVer](https://semver.org/) for versioning.

## Licence
NeqSim is distributed under the [Apache-2.0](https://github.com/equinor/neqsimsource/blob/master/LICENSE) licence.

## Acknowledgments
A number of master and PhD students at NTNU have contributed to development of NeqSim. We greatly acknowledge their contributions.
