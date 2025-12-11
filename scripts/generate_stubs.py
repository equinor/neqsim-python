"""
Script to generate Python type stubs for neqsim Java classes using stubgenj.

This enables IDE autocompletion and type checking for the neqsim Java library
accessed via JPype.

Usage:
    python scripts/generate_stubs.py

The stubs will be generated in the src/neqsim-stubs directory.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def generate_stubs():
    """Generate type stubs for neqsim Java classes."""
    import jpype
    import jpype.imports  # Enable Java imports
    import stubgenj

    # Start JVM if not already started
    if not jpype.isJVMStarted():
        # Import neqsim to start JVM with correct classpath
        import neqsim  # noqa: F401

    # Import the neqsim Java package to get JPackage reference
    from neqsim.neqsimpython import jneqsim

    # Output directory for stubs
    output_dir = src_path / "neqsim-stubs"
    output_dir.mkdir(exist_ok=True)

    # Generate stubs for the neqsim package
    print(f"Generating stubs in {output_dir}...")

    # Generate stubs for the neqsim package (pass JPackage objects)
    # stubgenj expects a list of JPackage objects, not strings
    stubgenj.generateJavaStubs(
        parentPackages=[jneqsim],  # The neqsim JPackage
        useStubsSuffix=True,  # Creates neqsim-stubs folder structure
        outputDir=str(output_dir),
        jpypeJPackageStubs=True,  # Include jpype stubs
        includeJavadoc=True,  # Include javadoc in stubs
    )

    print(f"Stubs generated successfully in {output_dir}")
    print("\nTo use the stubs for type checking, add the stubs path to your IDE.")
    print("For VS Code with Pylance, add to settings.json:")
    print('  "python.analysis.extraPaths": ["src/neqsim-stubs"]')


if __name__ == "__main__":
    generate_stubs()
