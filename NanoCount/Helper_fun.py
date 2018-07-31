# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
import sys

#~~~~~~~~~~~~~~FUNCTIONS~~~~~~~~~~~~~~#

def stderr_print (*args):
    """reproduce print with stdout.write
    """
    sys.stderr.write(" ".join(str(a) for a in args))
    sys.stderr.flush()
