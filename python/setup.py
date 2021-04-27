from setuptools import setup, find_packages
import sys

# this allows us to import the version without importing the minknow module (which may require
# dependencies that aren't installed yet)
sys.path.insert(0, "./minknow_api")
from _version import __version__ as VERSION

del sys.path[0]

INSTALL_REQUIRES = [
    "grpcio~=1.25",
    "numpy~=1.11",  # minknow_api.data
    "protobuf~=3.11",
    "packaging>=15.0",
]

setup(
    name="minknow_api",
    version=VERSION,
    author="Oxford Nanopore Technologies Ltd",
    author_email="info@nanoporetech.com",
    description="MinKNOW RPC API bindings",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": []},
)
