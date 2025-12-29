# Publishing NeqSim to Conda-Forge

This guide explains how to publish NeqSim to conda-forge for easy installation via Anaconda.

## Option 1: Submit to conda-forge (Recommended)

### Step 1: Ensure PyPI Package is Published

The conda-forge recipe pulls from PyPI, so ensure the latest version is published:

```bash
poetry build
poetry publish
```

### Step 2: Fork and Clone staged-recipes

```bash
git clone https://github.com/conda-forge/staged-recipes.git
cd staged-recipes
git checkout -b neqsim
```

### Step 3: Create the Recipe

Copy the recipe from the `conda/` directory:

```bash
mkdir recipes/neqsim
cp /path/to/neqsim-python/conda/meta.yaml recipes/neqsim/
```

### Step 4: Get the SHA256 Hash

After publishing to PyPI, get the hash:

```bash
curl -sL https://pypi.io/packages/source/n/neqsim/neqsim-3.1.5.tar.gz | sha256sum
```

Update `meta.yaml` with the hash.

### Step 5: Test Locally (Optional)

```bash
conda build recipes/neqsim
```

### Step 6: Submit Pull Request

Push your branch and create a PR to conda-forge/staged-recipes:

```bash
git add recipes/neqsim
git commit -m "Add neqsim recipe"
git push origin neqsim
```

Then open a PR at https://github.com/conda-forge/staged-recipes

### Step 7: Maintenance

Once accepted, a feedstock repository will be created at:
https://github.com/conda-forge/neqsim-feedstock

For version updates, submit PRs to the feedstock.

## Option 2: Personal Anaconda Channel

For quick testing or private distribution:

### Step 1: Create Anaconda Account

Register at https://anaconda.org

### Step 2: Build the Package

```bash
cd neqsim-python
conda build conda/
```

### Step 3: Upload to Anaconda

```bash
anaconda login
anaconda upload /path/to/conda-bld/noarch/neqsim-*.tar.bz2
```

### Step 4: Install from Your Channel

```bash
conda install -c YOUR_USERNAME neqsim
```

## Option 3: Using environment.yml (Immediate Solution)

Users can install immediately using the provided environment file:

```bash
conda env create -f environment.yml
conda activate neqsim-env
```

This installs all dependencies via conda (including Java) and neqsim via pip.

## Key Benefits of Conda Distribution

1. **Automatic Java Installation**: OpenJDK is installed as a conda dependency
2. **Cross-platform**: Works on Windows, macOS, and Linux
3. **Environment Management**: Easy to create isolated environments
4. **Reproducibility**: Pin exact versions for reproducible builds

## Testing the Installation

```python
import neqsim
from neqsim.thermo import fluid

# Create a simple fluid
gas = fluid('srk')
gas.addComponent('methane', 0.9)
gas.addComponent('ethane', 0.1)
gas.setTemperature(25.0, 'C')
gas.setPressure(50.0, 'bara')

# Run a flash calculation
from neqsim.thermo import TPflash
TPflash(gas)

print(f"Density: {gas.getDensity('kg/m3'):.2f} kg/m³")
```
