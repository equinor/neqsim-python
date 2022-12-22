from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_req = ['jpype1', 'pandas']
test_req = ['pytest']
interactive_req = ['matplotlib', 'tabulate', 'jupyter']

setup(
    name="neqsim",
    version="2.4.13",
    author="Even Solbraa",
    author_email="esolbraa@gmail.com",
    description="NeqSim is a tool for thermodynamic and process calculations",
    long_description="NeqSim (Non-Equilibrium Simulator) is a library for estimation of fluid behaviour for oil and gas production. The basis for NeqSim is fundamental mathematical models related to phase behaviour and physical properties of oil and gas.",
    long_description_content_type="text/markdown",
    url="https://github.com/Equinor/neqsimpython",
    packages=find_packages(),
    package_data={'neqsim': ['lib/*.jar','lib/libj8/*.jar']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_req,
    tests_suite='tests',
    test_requirements=test_req,
    extras_require={'test': test_req, 'interactive': interactive_req},
    python_requires='>=3'
)
