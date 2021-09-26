#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from genericpath import exists, isdir
from os import remove
from logzero import logger, logfile
import json


def main(args):
    """ Main entry point of the app """
    if(exists('logfile.logs')):
        remove('logfile.logs')
    logfile('logfile.logs')
    logger.info("hello world")
    logger.info(args)

    path = args.arg

    if(isdir(path)):
        logger.error("path is a folder")
    elif(not exists(path)):
        logger.error("path does not exist")
    else:
        with open(path, "r", encoding='utf-8') as f:
            json_file = json.load(f)
            print(json_file)
    


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
