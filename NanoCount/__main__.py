#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#

# Standard library imports
import argparse
from collections import *

# Local imports
from NanoCount import __version__ as package_version
from NanoCount import __name__ as package_name
from NanoCount import __description__ as package_description
from NanoCount.NanoCount import NanoCount as nc

#~~~~~~~~~~~~~~MAIN PARSER ENTRY POINT~~~~~~~~~~~~~~#

def main(args=None):

    # Define parser
    parser = argparse.ArgumentParser(description=package_description)
    parser.add_argument('--version', '-v', action='version', version="{} v{}".format(package_name, package_version))
    parser.add_argument('-i', '--alignment_file', type=str, required=True,
        help="BAM or SAM file containing aligned ONT dRNA-Seq reads including secondary and supplementary alignment")
    parser.add_argument('-o', '--count_file', type=str, required=True,
        help="Output count file")
    parser.add_argument('--min_read_length', type=int, default=50,
        help="Minimal length of the read to be considered valid")
    parser.add_argument('--min_query_fraction_aligned', type=float, default=0.5,
        help="Minimal fraction of the primary hit query aligned to consider the read valid")
    parser.add_argument('--equivalent_threshold', type=float, default=0.9,
        help="Fraction of the alignment score or the alignment length of secondary hits compared to the primary hit to be considered valid hits")
    parser.add_argument('--scoring_value', type=str, default="alignment_score",
        help="Value to use for score thresholding of secondary hits. Either alignment_score or alignment_length")
    parser.add_argument('--convergence_target', type=float, default=0.005,
        help="Convergence target value of the cummulative difference between abundance values of successive EM round to trigger the end of the EM loop")
    parser.add_argument('--verbose', default=False, action='store_true',
        help="If True will be chatty")
    args = parser.parse_args()

    nanocount = nc (
        alignment_file =args.alignment_file,
        min_read_length =args.min_read_length,
        min_query_fraction_aligned =args.min_query_fraction_aligned,
        equivalent_threshold =args.equivalent_threshold,
        scoring_value =args.scoring_value,
        convergence_target =args.convergence_target,
        verbose =args.verbose)

    nanocount.write_count_file (args.count_file)

# execute only if run as a script
if __name__ == "__main__":
    main()
