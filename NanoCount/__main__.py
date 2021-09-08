#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~ #

# Standard library imports
import argparse

# Local imports
import NanoCount as pkg
from NanoCount.NanoCount import NanoCount as nc
from NanoCount.common import *

# ~~~~~~~~~~~~~~MAIN PARSER ENTRY POINT~~~~~~~~~~~~~~ #


def main(args=None):

    # Define parser
    parser = argparse.ArgumentParser(description=pkg.__description__)
    parser.add_argument("--version", action="version", version="{} v{}".format(pkg.__name__, pkg.__version__))

    parser_io = parser.add_argument_group("Input/Output options")
    arg_from_docstr(parser=parser_io, func=nc, arg_name="alignment_file", short_name="i")
    arg_from_docstr(parser=parser_io, func=nc, arg_name="count_file", short_name="o")
    arg_from_docstr(parser=parser_io, func=nc, arg_name="filter_bam_out", short_name="b")

    parser_ms = parser.add_argument_group("Misc options")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="min_alignment_length", short_name="l")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="min_query_fraction_aligned", short_name="f")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="sec_scoring_value", short_name="s")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="sec_scoring_threshold", short_name="t")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="convergence_target", short_name="c")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="max_em_rounds", short_name="e")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="extra_tx_info", short_name="x")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="primary_score", short_name="p")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="keep_suplementary", short_name="a")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="max_dist_3_prime", short_name="d")
    arg_from_docstr(parser=parser_ms, func=nc, arg_name="max_dist_5_prime", short_name="u")

    parser_vb = parser.add_argument_group("Verbosity options")
    arg_from_docstr(parser=parser_vb, func=nc, arg_name="verbose", short_name="v")
    arg_from_docstr(parser=parser_vb, func=nc, arg_name="quiet", short_name="q")

    # Parse args and run main function
    args = parser.parse_args()
    nanocount = nc(**vars(args))


# execute only if run as a script
if __name__ == "__main__":
    main()
