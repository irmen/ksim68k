import os
import sys
import enum
import re
import textwrap
import unittest
from setuptools import setup

if sys.version_info < (3, 5):
    raise SystemExit("ksim68k requires Python 3.5 or newer")

module_path = os.path.abspath(".")  # to make sure the compiler can find the required include files
PKG_VERSION = re.search(r'^__version__\s*=\s*"(.+)"', open("ksim68k.py", "rt").read(), re.MULTILINE).groups()[0]

print("VERSION",PKG_VERSION)

if __name__ == "__main__":
    setup(
        name="ksim68k",
        version=PKG_VERSION,
        cffi_modules=["build_ffi_module.py:ffibuilder"],
        include_dirs=[module_path],
        zip_safe=False,
        include_package_data=False,
        py_modules=["ksim68k"],
        install_requires=["cffi>=1.3.0"],
        setup_requires=["cffi>=1.3.0"],
        python_requires=">=3.5"
    )
