import pytest


chemicals = pytest.importorskip("chemicals")

from chemicals.critical import Pc, Tc, omega  # type: ignore  # noqa: E402
from chemicals.identifiers import CAS_from_any  # type: ignore  # noqa: E402

from neqsim.thermo.thermoTools import addComponent, fluid


def test_use_extended_database_allows_missing_component():
    system = fluid("srk")

    with pytest.raises(Exception):
        addComponent(system, "dimethylsulfoxide", 1.0)

    system.useExtendedDatabase(True)
    addComponent(system, "dimethylsulfoxide", 1.0)

    component = system.getPhase(0).getComponent("dimethylsulfoxide")
    cas = CAS_from_any("dimethylsulfoxide")

    assert pytest.approx(component.getTC(), rel=1e-6) == Tc(cas)
    assert pytest.approx(component.getPC(), rel=1e-6) == Pc(cas) / 1.0e5
    assert pytest.approx(component.getAcentricFactor(), rel=1e-6) == omega(cas)
