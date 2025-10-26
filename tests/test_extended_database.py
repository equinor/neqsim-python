import pytest


chemicals = pytest.importorskip("chemicals")

import chemicals.critical as critical_data  # type: ignore  # noqa: E402
from chemicals.critical import Pc, Tc, Vc, Zc, omega  # type: ignore  # noqa: E402
from chemicals.elements import molecular_weight  # type: ignore  # noqa: E402
from chemicals.phase_change import Tb  # type: ignore  # noqa: E402
from chemicals.identifiers import CAS_from_any  # type: ignore  # noqa: E402

from neqsim.thermo.thermoTools import addComponent, fluid


def test_use_extended_database_allows_missing_component():
    system = fluid("srk")

    with pytest.raises(Exception):
        system.addComponent("dimethylsulfoxide", 1.0)

    system.useExtendedDatabase(True)
    system.addComponent("dimethylsulfoxide", 1.0)

    component = system.getPhase(0).getComponent("dimethylsulfoxide")
    cas = CAS_from_any("dimethylsulfoxide")

    assert pytest.approx(component.getTC(), rel=1e-6) == Tc(cas)
    assert pytest.approx(component.getPC(), rel=1e-6) == Pc(cas) / 1.0e5
    assert pytest.approx(component.getAcentricFactor(), rel=1e-6) == omega(cas)

    molar_mass = molecular_weight(CASRN=cas)
    assert molar_mass is not None
    assert pytest.approx(component.getMolarMass(), rel=1e-6) == molar_mass / 1000.0

    normal_boiling_point = Tb(cas)
    if normal_boiling_point is not None:
        assert pytest.approx(component.getNormalBoilingPoint(), rel=1e-6) == normal_boiling_point

    critical_volume = Vc(cas)
    if critical_volume is not None:
        assert pytest.approx(component.getCriticalVolume(), rel=1e-6) == critical_volume * 1.0e6

    critical_compressibility = Zc(cas)
    if critical_compressibility is not None:
        assert (
            pytest.approx(component.getCriticalCompressibilityFactor(), rel=1e-6)
            == critical_compressibility
        )

    triple_point_func = getattr(critical_data, "Ttriple", None) or getattr(
        critical_data, "Tt", None
    )
    if triple_point_func is not None:
        triple_point_temperature = triple_point_func(cas)
        if triple_point_temperature is not None:
            assert (
                pytest.approx(component.getTriplePointTemperature(), rel=1e-6)
                == triple_point_temperature
            )


def test_module_add_component_uses_extended_database():
    system = fluid("srk")

    with pytest.raises(Exception):
        addComponent(system, "dimethylsulfoxide", 1.0)

    system.useExtendedDatabase(True)
    addComponent(system, "dimethylsulfoxide", 1.0)

    assert system.getPhase(0).hasComponent("dimethylsulfoxide")
