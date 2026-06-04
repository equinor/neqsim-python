"""
Script to generate Python type stubs for neqsim Java classes using stubgenj.

This enables IDE autocompletion and type checking for the neqsim Java library
accessed via JPype.

The Java package 'neqsim' is exposed as 'jneqsim' in Python to avoid naming
conflicts with the Python 'neqsim' package. The stubs are generated accordingly.

Usage:
    python scripts/generate_stubs.py

The stubs will be generated in the src/jneqsim directory.
"""

import re
import shutil
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def rename_package_in_stubs(stubs_dir: Path, old_name: str, new_name: str):
    """
    Rename all references from old_name to new_name in stub files.
    This handles the neqsim -> jneqsim renaming to avoid conflicts
    with the Python neqsim package.
    """
    for pyi_file in stubs_dir.rglob("*.pyi"):
        content = pyi_file.read_text(encoding="utf-8")

        # Replace import statements and type references
        # Match 'neqsim.' but not 'jneqsim.' (negative lookbehind)
        new_content = re.sub(rf"(?<!j){old_name}\.", f"{new_name}.", content)

        if new_content != content:
            pyi_file.write_text(new_content, encoding="utf-8")


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

    # Temporary output directory (stubgenj will create 'neqsim-stubs')
    temp_output_dir = src_path / "temp-stubs"
    if temp_output_dir.exists():
        shutil.rmtree(temp_output_dir)
    temp_output_dir.mkdir(exist_ok=True)

    # Final output directory: stubs live directly under src/ alongside neqsim/
    final_output_dir = src_path

    print("Generating stubs...")

    # Generate stubs for the neqsim package (pass JPackage objects)
    stubgenj.generateJavaStubs(
        parentPackages=[jneqsim],  # The neqsim JPackage
        useStubsSuffix=True,  # Creates neqsim-stubs folder structure
        outputDir=str(temp_output_dir),
        jpypeJPackageStubs=True,  # Include jpype stubs
        includeJavadoc=True,  # Include javadoc in stubs
    )

    # Rename neqsim -> jneqsim in all stub files to avoid conflict
    # with Python neqsim package
    neqsim_stubs = temp_output_dir / "neqsim-stubs"
    if neqsim_stubs.exists():
        print("Renaming 'neqsim' -> 'jneqsim' in stubs to avoid naming conflict...")
        rename_package_in_stubs(temp_output_dir, "neqsim", "jneqsim")

        # Clean up existing jneqsim output
        jneqsim_stubs_out = final_output_dir / "jneqsim"
        if jneqsim_stubs_out.exists():
            shutil.rmtree(jneqsim_stubs_out)

        # Move jpype-stubs as-is (it's at temp_output_dir/jpype-stubs)
        jpype_stubs = temp_output_dir / "jpype-stubs"
        if jpype_stubs.exists():
            jpype_stubs_out = final_output_dir / "jpype-stubs"
            if jpype_stubs_out.exists():
                shutil.rmtree(jpype_stubs_out)
            shutil.move(str(jpype_stubs), str(jpype_stubs_out))

        # Move stubs from temp directory to final output directory
        shutil.move(str(neqsim_stubs), str(jneqsim_stubs_out))

        # Clean up temp directory
        shutil.rmtree(temp_output_dir)

    print(f"Stubs generated successfully in {final_output_dir / 'jneqsim'}")
    print("\n" + "=" * 60)
    print("USAGE INSTRUCTIONS")
    print("=" * 60)
    print("\nThe Java 'neqsim' package stubs are available as 'jneqsim'")
    print("to avoid conflicts with the Python 'neqsim' package.")
    print("\nFor VS Code with Pylance, add to settings.json:")
    print('  "python.analysis.extraPaths": ["src"]')
    print("\nFor mypy, add to pyproject.toml:")
    print("  [tool.mypy]")
    print('  mypy_path = "src"')


if __name__ == "__main__":
    generate_stubs()
