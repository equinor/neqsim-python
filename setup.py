import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neqsim",
    version="0.0.1",
    author="Even Solbraa",
    author_email="esolbraa@gmail.com",
    description="NeqSim is a tool for thermodynamic and process calculations",
    long_description="NeqSim is a tool for thermodynamic and process calculations",
    long_description_content_type="text/markdown",
    url="https://github.com/Statoil/neqsimpython",
    packages=['neqsim',"neqsim.thermo", "neqsim.process", "neqsim.standards"],
    package_dir={'neqsim': 'src/neqsim'},
    package_data={'neqsim': ['lib/*.jar']},
    include_package_data=True,
    install_requires=['py4j',]
)