# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~ #
# Standard library imports
import sys
import os
from collections import *
import logging
import datetime
import inspect

# Third party imports
import colorlog
import NanoCount as pkg

# ~~~~~~~~~~~~~~FUNCTIONS~~~~~~~~~~~~~~ #


def opt_summary(local_opt):
    """Simplifiy option dict creation"""
    d = OrderedDict()
    d["Package name"] = pkg.__name__
    d["Package version"] = pkg.__version__
    d["Timestamp"] = str(datetime.datetime.now())
    for i, j in local_opt.items():
        if not i == "self":
            d[i] = j
    return d


def get_logger(name=None, verbose=False, quiet=False):
    """Multilevel colored log using colorlog"""

    # Define conditional color formatter
    formatter = colorlog.LevelFormatter(
        fmt={
            'DEBUG': '%(log_color)s\t[DEBUG]: %(msg)s',
            'INFO': '%(log_color)s\t%(msg)s',
            'WARNING': '%(log_color)s## %(msg)s ##',
            'ERROR': '%(log_color)sERROR: %(msg)s',
            'CRITICAL': '%(log_color)sCRITICAL: %(msg)s',
        },
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'bold_blue',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_purple',
        },
        reset=True,
    )

    # Define logger with custom formatter
    logging.basicConfig(format='%(message)s')
    logging.getLogger().handlers[0].setFormatter(formatter)
    log = logging.getLogger(name)

    # Define logging level depending on verbosity
    if verbose:
        log.setLevel(logging.DEBUG)
    elif quiet:
        log.setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)

    return log


def log_dict(d, logger, header="", indent="\t", level=1):
    """ log a multilevel dict """
    if header:
        logger(header)
    if isinstance(d, Counter):
        for i, j in d.most_common():
            logger("{}{}: {:,}".format(indent * level, i, j))
    else:
        for i, j in d.items():
            if isinstance(j, dict):
                logger("{}{}".format(indent * level, i, j))
                log_dict(j, logger, level=level + 1)
            else:
                logger("{}{}: {}".format(indent * level, i, j))


def log_list(l, logger, header="", indent="\t"):
    """ log a list """
    if header:
        logger(header)
    for i in l:
        logger("{}*{}".format(indent, i))


def doc_func(func):
    """Parse the function description string"""

    if inspect.isclass(func):
        func = func.__init__

    docstr_list = []
    for l in inspect.getdoc(func).split("\n"):
        l = l.strip()
        if l:
            if l.startswith("*"):
                break
            else:
                docstr_list.append(l)

    return " ".join(docstr_list)


def make_arg_dict(func):
    """Parse the arguments default value, type and doc"""

    # Init method for classes
    if inspect.isclass(func):
        func = func.__init__

    if inspect.isfunction(func) or inspect.ismethod(func):
        # Parse arguments default values and annotations
        d = OrderedDict()
        for name, p in inspect.signature(func).parameters.items():
            if not p.name in [
                "self",
                "cls",
            ]:  # Object stuff. Does not make sense to include in doc
                d[name] = OrderedDict()
                if not name in [
                    "kwargs",
                    "args",
                ]:  # Include but skip default required and type
                    # Get Annotation
                    if p.annotation != inspect._empty:
                        d[name]["type"] = p.annotation
                    # Get default value if available
                    if p.default == inspect._empty:
                        d[name]["required"] = True
                    else:
                        d[name]["default"] = p.default

        # Parse the docstring in a dict
        docstr_dict = OrderedDict()
        lab = None
        for l in inspect.getdoc(func).split("\n"):
            l = l.strip()
            if l:
                if l.startswith("*"):
                    lab = l[1:].strip()
                    docstr_dict[lab] = []
                elif lab:
                    docstr_dict[lab].append(l)

        # Concatenate and copy doc in main dict
        for name in d.keys():
            if name in docstr_dict:
                d[name]["help"] = " ".join(docstr_dict[name])
        return d


def arg_from_docstr(parser, func, arg_name, short_name=None):
    """Get options corresponding to argument name from docstring and deal with special cases"""

    if short_name:
        arg_names = ["-{}".format(short_name), "--{}".format(arg_name)]
    else:
        arg_names = ["--{}".format(arg_name)]

    arg_dict = make_arg_dict(func)[arg_name]

    if "help" in arg_dict:
        if "default" in arg_dict:
            if arg_dict["default"] == "" or arg_dict["default"] == []:
                arg_dict["help"] += " (default: None)"
            else:
                arg_dict["help"] += " (default: %(default)s)"
        else:
            arg_dict["help"] += " (required)"

        if "type" in arg_dict:
            if arg_dict["type"] == bool:
                arg_dict["help"] += " [boolean]"
            else:
                arg_dict["help"] += " [%(type)s]"

    # Special case for boolean args
    if arg_dict["type"] == bool:
        del arg_dict["type"]
        if arg_dict["default"] == False:
            arg_dict["action"] = 'store_true'
        elif arg_dict["default"] == True:
            arg_dict["action"] = 'store_false'

    # Special case for lists args
    elif isinstance(arg_dict["type"], list):
        arg_dict["nargs"] = '*'
        arg_dict["type"] = arg_dict["type"][0]

    parser.add_argument(*arg_names, **arg_dict)


def jhelp(f: "python function or method"):
    """
    Display a Markdown pretty help message for functions and class methods (default __init__ is a class is passed)
    jhelp also display default values and type annotations if available.
    The docstring synthax should follow the same synthax as the one used for this function
    * f
        Function or method to display the help message for
    """
    # Private import as this is only needed if using jupyter
    from IPython.core.display import display, Markdown

    f_doc = doc_func(f)
    arg_doc = make_arg_dict(f)

    # Signature and function documentation
    s = "**{}** ({})\n\n{}\n\n---\n\n".format(f.__name__, ", ".join(arg_doc.keys()), f_doc)

    # Args doc
    for arg_name, arg_val in arg_doc.items():
        # Arg signature section
        s += "* **{}**".format(arg_name)
        if "default" in arg_val:
            if arg_val["default"] == "":
                s += " (default: \"\")".format(arg_val["default"])
            else:
                s += " (default: {})".format(arg_val["default"])
        if "required" in arg_val:
            s += " (required)"
        if "type" in arg_val:
            if isinstance(arg_val["type"], type):
                s += " [{}]".format(arg_val["type"].__name__)
            elif isinstance(arg_val["type"], list):
                s += " [list({})]".format(arg_val["type"][0].__name__)
            else:
                s += " [{}]".format(arg_val["type"])
        s += "\n\n"
        # Arg doc section
        if "help" in arg_val:
            s += "{}\n\n".format(arg_val["help"])

    # Display in Jupyter
    display(Markdown(s))


def head(fp, n=10, sep="\t", max_char_col=50, comment=None):
    """
    Emulate linux head cmd. Handle gziped files and bam files
    * fp
        Path to the file to be parse.
    * n
        Number of lines to print starting from the begining of the file (Default 10)
    """
    line_list = []

    # Get lines
    try:
        open_fun, open_mode = (gzip.open, "rt") if fp.endswith(".gz") else (open, "r")
        with open_fun(fp, open_mode) as fh:
            line_num = 0
            while line_num < n:
                l = next(fh).strip()
                if comment and l.startswith(comment):
                    continue
                if sep:
                    line_list.append(l.split(sep))
                else:
                    line_list.append(l)
                line_num += 1

    except StopIteration:
        pass

    # Add padding if sep given
    if sep:
        try:
            # Find longest elem per col
            col_len_list = [0 for _ in range(len(line_list[0]))]
            for ls in line_list:
                for i in range(len(ls)):
                    len_col = len(ls[i])
                    if len_col > max_char_col:
                        col_len_list[i] = max_char_col
                    elif len_col > col_len_list[i]:
                        col_len_list[i] = len_col

            # Add padding
            line_list_tab = []
            for ls in line_list:
                s = ""
                for i in range(len(ls)):
                    len_col = col_len_list[i]
                    len_cur_col = len(ls[i])
                    if len_cur_col <= len_col:
                        s += ls[i] + " " * (len_col - len_cur_col) + " "
                    else:
                        s += ls[i][0 : len_col - 3] + "..."
                line_list_tab.append(s)
            line_list = line_list_tab

        # Fall back to non tabulated display
        except IndexError:
            return head(fp=fp, n=n, sep=None)

    for l in line_list:
        print(l)
    print()
