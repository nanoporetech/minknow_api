import os
import py_compile
import sys
from pathlib import Path


def check_syntax(path):
    for service_file in path.glob("*_service.py"):
        assert py_compile.compile(str(service_file))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = Path(os.getcwd())
    else:
        path = Path(sys.argv[1])

    check_syntax(path)
