"""Setup file for ansys-units."""
import os
import shutil

from setuptools import find_namespace_packages, setup

# Get version from version info
__version__ = None
_THIS_FILE = os.path.dirname(__file__)
_VERSION_FILE = os.path.join(_THIS_FILE, "src", "ansys", "units", "_version.py")
with open(_VERSION_FILE, mode="r", encoding="utf8") as fd:
    # execute file from raw string
    exec(fd.read())

# Copy README.rst file to docs folder in ansys.units
_README_FILE = os.path.join(_THIS_FILE, "README.rst")
_DOCS_FILE = os.path.join(_THIS_FILE, "src", "ansys", "units", "docs", "README.rst")
shutil.copy2(_README_FILE, _DOCS_FILE)


install_requires = [
    "importlib-metadata >=4.0",
    "numpy>=1.21.5",
    "platformdirs>=3.5.1",
    "pandas>=1.1.5",
    "h5py>=3.8.0",
    "lxml>=4.9.2",
    "pyyaml>=6.0",
    "docker>=6.1.3",
    "psutil>=5.9.5",
]

packages = []
for package in find_namespace_packages(where="src", include="ansys*"):
    if package.startswith("ansys.units"):
        packages.append(package)

setup(
    name="ansys-units",
    version=__version__,
    url="https://github.com/ansys/pyunits",
    author="ANSYS, Inc.",
    author_email="pyansys.support@ansys.com",
    maintainer="PyAnsys developers",
    maintainer_email="pyansys.maintainers@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_file="LICENSE",
    description="Pythonic interface for units, unit systems, and unit conversions.",
    long_description=open(_README_FILE, encoding="utf8").read(),
    install_requires=install_requires,
    python_requires=">=3.8",
    packages=packages,
    package_dir={"": "src"},
    include_package_data=True,
)
