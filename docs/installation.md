# Installation

## Create a clean virtual environment (optional but recommended)

Ideally, before installation, create a clean **python3.6+** virtual environment to deploy the package.
Earlier version of Python 3 should also work (not tested) but **Python 2 is not supported**.
For example one can use conda or virtualenvwrapper.

With [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html):

```bash
mkvirtualenv NanoCount -p python3.6
workon NanoCount
```

With [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```bash
conda create -n NanoCount python=3.6
conda activate NanoCount
```

## Dependencies

[Minimap2](https://github.com/lh3/minimap2) is not a direct dependency but is required to generate the BAM alignment required by NanoCount.

`NanoCount` relies on a the following robustly maintained third party python libraries:

* pysam>=0.15.4
* pandas>=1.0.3
* tqdm>=4.46.0
* colorlog>=4.1.0

The correct versions of packages are installed together with the software when using pip or conda.

## Option 1: Installation with pip from pypi (recommended)

Install or upgrade the package with pip from pypi

```bash
pip install NanoCount
```

You can also update to the **unstable** development version from test.pypi repository

```bash
pip install --index-url https://test.pypi.org/simple/ NanoCount -U
```

## Option 2: Installation with conda from Anaconda cloud

**If you want to be sure to get the last version don't forget to add my channel and to specify the last version number**

```bash
# First installation
conda install -c aleg nanocount=[VERSION]
```

You can also get the **unstable** development version from my dev channel

```bash
conda update -c aleg_dev nanocount=[VERSION]
```

## Option 3: Installation with pip from Github

Or from github to get the last version

```bash
# First installation
pip install git+https://github.com/a-slide/NanoCount.git

# First installation bleeding edge
pip install git+https://github.com/a-slide/NanoCount.git@dev

# Update to last version
pip install git+https://github.com/a-slide/NanoCount.git --upgrade
```

## Option 4: Clone the repository and install locally in develop mode

With this option, the package will be locally installed in *editable* or *develop mode*. This allows the package to be both installed and editable in project form. This is the recommended option if you wish to modify the code and/or participate to the development of the package (see [contribution guidelines](contributing.md)).

```bash
# Clone repo localy
git clone https://github.com/a-slide/NanoCount.git

# Enter in repo directory
cd NanoCount

# Make setup.py executable
chmod u+x setup.py

# Install with pip3
pip3 install -e ./
```
