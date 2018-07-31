# -*- coding: utf-8 -*-

# Define self package variable
__version__ = "0.1.a2"
__all__ = ["NanoCount", "Read"]

description = 'EM based transcript abundance from nanopore reads mapped to a transcriptome with minimap2'
long_description = """"""

# Collect info in a dictionary for setup.py
setup_dict = {
    "name": __name__,
    "version": __version__,
    "description": description,
    "long_description": long_description,
    "url": "https://github.com/a-slide/NanoCount",
    "author": 'Adrien Leger',
    "author_email": 'aleg {at} ebi.ac.uk',
    "license": "MIT",
    "python_requires":'>=3.5',
    "classifiers": [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    "install_requires": ['pysam>=0.14.1', 'pandas>=0.23.3'],
    "packages": [__name__],
    "entry_points":{'console_scripts': ['NanoCount = NanoCount.NanoCount:main']}}
