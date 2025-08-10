from neqsim.neqsimpython import jneqsim


def ISO6976(
    fluid,
    numberunit="volume",
    referencetemperaturevolume="15",
    referencetemperaturecombustion="15",
):
    """numberUnit can be 'volume', 'mass', 'molar"""
    iso6976 = jneqsim.standards.gasquality.Standard_ISO6976(fluid)
    iso6976.setReferenceType(numberunit)
    iso6976.setVolRefT(float(referencetemperaturevolume))
    iso6976.setEnergyRefT(float(referencetemperaturecombustion))
    iso6976.calculate()
    return iso6976


def air_fuel_ratio(fluid):
    """Calculates the air fuel ratio for a fluid/fuel [kg air/kg fuel]"""
    elements_h = 0.0
    elements_c = 0.0
    sum_hc = 0.0
    molmass_hc = 0.0
    wtfrac_hc = 0.0

    for i in range(fluid.getNumberOfComponents()):
        if fluid.getComponent(i).isHydrocarbon():
            sum_hc = sum_hc + fluid.getComponent(i).getz()
            molmass_hc = (
                molmass_hc
                + fluid.getComponent(i).getz() * fluid.getComponent(i).getMolarMass()
            )
            elements_c = elements_c + fluid.getComponent(i).getz() * fluid.getComponent(
                i
            ).getElements().getNumberOfElements("C")
            elements_h = elements_h + fluid.getComponent(i).getz() * fluid.getComponent(
                i
            ).getElements().getNumberOfElements("H")

    if sum_hc == 0:
        return 0.0
    else:
        wtfrac_hc = molmass_hc / fluid.getMolarMass()
        molmass_hc /= sum_hc
        elements_c /= sum_hc
        elements_h /= sum_hc

    aconst = elements_c + elements_h / 4
    afr = aconst * (32.0 + 3.76 * 28.0) / 1000.0 / molmass_hc * wtfrac_hc
    return afr
