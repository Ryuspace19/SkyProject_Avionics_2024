# setup.py

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("HPAC24_HPAdisplay.pyx")
)
