import pytest
import jpype

@pytest.fixture(scope="session")
def shutdown_jvm():
    # Setup: ensure the JVM is started (if needed)
    if not jpype.isJVMStarted():
        jpype.startJVM(convertStrings=False)
        # Configure the classpath, etc.

    yield

    # Teardown: explicitly shut down the JVM
    if jpype.isJVMStarted():
        jpype.shutdownJVM()