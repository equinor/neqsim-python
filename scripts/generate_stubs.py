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


def sanitize_python_local_references(stubs_dir: Path):
    """Remove Python mixin implementation details from generated Java stubs.

    Rich notebook display is registered through local Python mixin classes such
    as ``register.<locals>._StreamDisplay``. JPype exposes those runtime bases
    to stubgenj, but their qualified names are not valid Python syntax and must
    not be written to ``.pyi`` files.

    Args:
        stubs_dir: Directory containing generated stub files.
    """
    local_type = r"register\.<locals>\.[A-Za-z_][A-Za-z0-9_]*"
    local_import = rf"^from [A-Za-z0-9_.]+ import {local_type}\n"

    for pyi_file in stubs_dir.rglob("*.pyi"):
        content = pyi_file.read_text(encoding="utf-8")
        new_content = re.sub(local_import, "", content, flags=re.MULTILINE)
        new_content = re.sub(rf",\s*{local_type}", "", new_content)
        new_content = re.sub(rf"{local_type},\s*", "", new_content)
        new_content = re.sub(local_type, "typing.Protocol", new_content)
        new_content = (
            "\n".join(line.rstrip() for line in new_content.splitlines()).rstrip()
            + "\n"
        )

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
        sanitize_python_local_references(temp_output_dir)

        # Clean up existing jneqsim-stubs output
        jneqsim_stubs_out = src_path / "jneqsim-stubs"
        if jneqsim_stubs_out.exists():
            shutil.rmtree(jneqsim_stubs_out)

        # Move jpype-stubs as-is (it's at temp_output_dir/jpype-stubs)
        jpype_stubs = temp_output_dir / "jpype-stubs"
        if jpype_stubs.exists():
            jpype_stubs_out = src_path / "jpype-stubs"
            if jpype_stubs_out.exists():
                shutil.rmtree(jpype_stubs_out)
            shutil.move(str(jpype_stubs), str(jpype_stubs_out))

        # Move stubs from temp directory to final output directory
        # (must keep -stubs suffix for uv discovery)
        shutil.move(str(neqsim_stubs), str(jneqsim_stubs_out))

        # Clean up temp directory
        shutil.rmtree(temp_output_dir)

    print(f"Stubs generated successfully in {jneqsim_stubs_out}")
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
