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
from datetime import datetime
import json
import sys


def main(args):
    """ Main entry point of the app """
    if(exists('logfile.logs')):
        remove('logfile.logs')
    logfile('logfile.logs')
    logger.info("hello world")
    logger.info(args)

    sourceFilePath = args.arg
    

    if(isdir(sourceFilePath)):
        logger.error("path is a folder")
        sys.exit(1)
    elif(not exists(sourceFilePath)):
        logger.error("path does not exist")
        sys.exit(1)
    else:
        with open(sourceFilePath, "r", encoding='utf-8') as f:
            json_file = json.load(f)

    # channel content
    channelName = json_file["name"]
    channelType = json_file["type"]

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H%M%S")
    htmlFile = f"output-{dt_string}.html"

    with open(htmlFile, 'w', encoding='utf-8') as f:
        f.write(f"""
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>JSON to HTML</title>
                        </head>
                        <body>
                        <h1>{channelName}</h1>
                        <a href="https://t.me/themuslimarchive">https://t.me/themuslimarchive</a>
                        <p>{channelType}</p>
                """)
        for message in json_file["messages"]:
            postID = message["id"]
            postDate = message["date"]

            f.write(f"""
                        <h2>Date: {postDate}</h2>
                        <p>id: {postID}</p>
                        <hr>
                    """)
        
        f.write("""
                        </body>
                    </html>
                """)

    sys.exit(0)
    


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
