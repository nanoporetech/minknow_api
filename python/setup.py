from setuptools import setup, find_packages
from pathlib import Path
import sys

# this allows us to import the version without importing the minknow module (which may require
# dependencies that aren't installed yet)
sys.path.insert(0, "./minknow_api")
from _version import __version__ as VERSION

del sys.path[0]


def get_readme():
    MK_API_ROOT = Path(__file__).parent
    return (MK_API_ROOT / "README.md").read_text()


INSTALL_REQUIRES = [
    # Python 3.7 has importlib.resources built in
    # Version 3.3 drops support for Python 3.5
    "importlib-resources<3.3; python_version < '3.7.0'",
    "grpcio~=1.37",
    "numpy~=1.11",  # minknow_api.data
    "protobuf~=3.15",  # 3.15 includes use of 'optional' for scalar fields
    "packaging>=15.0",
    "pyrfc3339~=1.1",
]

setup(
    name="minknow_api",
    version=VERSION,
    author="Oxford Nanopore Technologies PLC",
    author_email="info@nanoporetech.com",
    url="https://github.com/nanoporetech/minknow_api",
    description="MinKNOW RPC API bindings",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    package_data={"": ["*.crt"]},
    entry_points={"console_scripts": []},
)
