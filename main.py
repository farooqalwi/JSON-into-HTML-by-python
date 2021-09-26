#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from genericpath import exists, isdir, isfile
from os import remove
from logzero import logger, logfile
from datetime import datetime
import json
import sys
import os


def main(args):
    """ Main entry point of the app """
    sourceFilePath = args.arg
    if(os.path.isdir(sourceFilePath)):
        logger.error("Source path is a folder")
        sys.exit(1)
    elif(not os.path.isfile(sourceFilePath)):
        logger.error("Source path does not exist")
        sys.exit(1)
    else:
        with open(sourceFilePath, "r", encoding='utf-8') as f:
            json_file = json.load(f)
    

    # for output file name, default file name is current timestamp from step 60 "output-2021-09-26 0110.html"
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H%M")
    defaultFileName = f"result-{dt_string}.html"

    if(args.output != ""):
        outputPath = args.output
    else:
        outputPath = defaultFileName

    if(os.path.isdir(outputPath)):
        # incase it is only folder then create output file with default file name
        outputPath = f"{outputPath}\{defaultFileName}"
        if(os.path.isfile(outputPath)):
            logger.error("Output file is already present")
            sys.exit(1)
    elif(os.path.isfile(outputPath) or os.path.isfile(f"{outputPath}.html")):
        logger.error("Output file is already present")
        sys.exit(1)
    elif(".html" not in outputPath):
        # file name without extension creating in current directory
        outputPath = f"{outputPath}.html"
    elif(".html" in outputPath):
        # incase full path with file name
        outputPath = outputPath
    elif(not os.path.isdir(outputPath)):
        logger.error("Destination path does not exist")
        sys.exit(1)

    
    # channel content
    channelName = json_file["name"]
    channelType = json_file["type"]
    messages = json_file["messages"]

    # for sorting order, 'asc' for ascending, 'desc' for descending. by default sorted by 'desc'
    if(args.sort == "desc"):
        messages.reverse()
    elif(args.sort != "asc"):
        logger.error("sort order mismatch")
        sys.exit(1)

    with open(outputPath, 'w', encoding='utf-8') as f:
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
        for message in messages:
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
    
    logger.info("HTML file created")
    sys.exit(0)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    if(os.path.isfile('logfile.logs')):
        remove('logfile.logs')
    logfile('logfile.logs')
    
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Use for source file path, this is required.")

    # for output path
    parser.add_argument("-o", dest="output", default="", help="Use for output destination, default output path is current folder.")
    
    # for sorting order, 'asc' for ascending, 'desc' for descending. by default sorted by 'desc'
    parser.add_argument("-s", dest="sort", default="desc", help="To sord post, use 'asc' for ascending, 'desc' for descending order. by default sorted by 'desc'")

    if len(sys.argv) == 1:
        logger.error("Source file was not provided.")
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    main(args)