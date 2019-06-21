#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
import NanoCount as package

# Collect info in a dictionary for setup.py
setup(
    name = package.__name__,
    version = package.__version__,
    description = package.__description__,
    url = "https://github.com/a-slide/NanoCount",
    author = 'Adrien Leger',
    author_email = 'aleg@ebi.ac.uk',
    license = "MIT",
    python_requires ='>=3.5',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    install_requires = [
        'pysam>=0.14.1',
        'pandas>=0.23.3'],
    packages = [package.__name__],
    entry_points = {'console_scripts': ['NanoCount = NanoCount.__main__:main']})
