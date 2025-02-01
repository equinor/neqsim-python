import pytest
import jpype

@pytest.fixture(scope="session", autouse=True)
def manage_jvm():
    if not jpype.isJVMStarted():
        jpype.startJVM(convertStrings=False, "-Xms512m", "-Xmx2g")
        # Set up your classpath as needed
    yield
    if jpype.isJVMStarted():
        jpype.shutdownJVM()