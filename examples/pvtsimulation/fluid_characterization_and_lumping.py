# -*- coding: utf-8 -*-
"""
Fluid characterization + PVT lumping (black oil style)
=====================================================

This example shows a typical characterization workflow when you have:
  - Light ends as normal components (N2/CO2/C1.../C6)
  - Heavy end as TBP cuts and a final plus fraction (e.g. C11+)

Key steps:
  1) Add TBP fractions and a plus fraction with molar mass and density
  2) Select PVT lumping model (PVTlumpingModel) and number of pseudo components
  3) `characterisePlusFraction()` to split/lump the plus fraction into pseudo components
  4) Create database + set mixing rule + enable volume correction

You can then run PVTsimulation experiments (CCE/CVD/DL/sep test) on the characterized fluid.
"""

from __future__ import annotations

from neqsim.thermo import TPflash, fluid, printFrame


def main() -> None:
    oil = fluid("srk", 273.15 + 100.0, 250.0)

    oil.addComponent("nitrogen", 0.34)
    oil.addComponent("CO2", 3.59)
    oil.addComponent("methane", 67.42)
    oil.addComponent("ethane", 9.02)
    oil.addComponent("propane", 4.31)
    oil.addComponent("i-butane", 0.93)
    oil.addComponent("n-butane", 1.71)
    oil.addComponent("i-pentane", 0.74)
    oil.addComponent("n-pentane", 0.85)
    oil.addComponent("n-hexane", 1.38)

    oil.addTBPfraction("C7", 1.50, 109.00 / 1000.0, 0.6912)
    oil.addTBPfraction("C8", 1.69, 120.20 / 1000.0, 0.7255)
    oil.addTBPfraction("C9", 1.14, 129.50 / 1000.0, 0.7454)
    oil.addTBPfraction("C10", 0.80, 135.30 / 1000.0, 0.7864)
    oil.addPlusFraction("C11", 4.58, 256.20 / 1000.0, 0.8398)

    oil.getCharacterization().setLumpingModel("PVTlumpingModel")
    oil.getCharacterization().getLumpingModel().setNumberOfPseudoComponents(12)
    oil.getCharacterization().characterisePlusFraction()

    oil.createDatabase(True)
    oil.setMixingRule(2)
    oil.setMultiPhaseCheck(True)
    oil.useVolumeCorrection(True)

    TPflash(oil)
    printFrame(oil)

    lumping = oil.getCharacterization().getLumpingModel()
    n_lumped = int(lumping.getNumberOfLumpedComponents())
    print(f"\nNumber of lumped components: {n_lumped}")
    for i in range(n_lumped):
        print(f"{i:2d}: {lumping.getLumpedComponentName(i)}")


if __name__ == "__main__":
    main()

