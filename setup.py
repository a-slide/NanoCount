#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
import NanoCount as package

# Define package info
name = "NanoCount"
version = "0.2.0"
description = "EM based transcripts abundance estimation from nanopore reads mapped to a transcriptome with minimap2"
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name = name,
    description = description,
    version = version,
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/a-slide/NanoCount",
    author = 'Adrien Leger',
    author_email = 'aleg@ebi.ac.uk',
    license = "MIT",
    python_requires ='>=3.6',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    install_requires = [
        'pysam>=0.15.4',
        'pandas>=1.0.3',
        'tqdm>=4.46.0',
        'colorlog>=4.1.0'],
    packages = [name],
    entry_points = {'console_scripts': ['NanoCount = NanoCount.__main__:main']})
