import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_faulthandler():
    try:
        import faulthandler

        # Enable then disable faulthandler to prevent pytest from taking over error handlers
        faulthandler.enable()
        faulthandler.disable()
    except Exception:
        pass
