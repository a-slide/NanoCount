#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name="NanoCount",
    description="NanoCount estimates transcripts abundance from Oxford Nanopore *direct-RNA sequencing* datasets, using an expectation-maximization approach like RSEM, Kallisto, salmon, etc to handle the uncertainty of multi-mapping reads",
    version="0.4.0.post4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-slide/NanoCount/",
    author="Adrien Leger",
    author_email="aleg@ebi.ac.uk",
    license="MIT",
    python_requires=">=3.6",
    classifiers=["Development Status :: 3 - Alpha", "Intended Audience :: Science/Research", "Topic :: Scientific/Engineering :: Bio-Informatics", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
    install_requires=["tqdm>=4.51.0", "numpy>=1.19.4", "pysam>=0.16.0", "pandas>=1.1.4",  "colorlog>=4.1.0"],
    packages=["NanoCount"],
    entry_points={"console_scripts": ["NanoCount=NanoCount.__main__:main"]},
)
