#!/usr/bin/env python3
"""
This script converts json into html
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


import json
import argparse
import sys
import os
from datetime import datetime
from logzero import logger, logfile
from jinja2 import Environment, FileSystemLoader


class FunctionFailed(Exception):
    """We use this custom exception whenver our function fails for any reason
    The caller will not receive any other exception"""


def validate_path_folder(path):
    """this function validates user given folder path,
    incase valid path returns the path"""
    if os.path.isdir(path):
        validated_path = path
    else:
        logger.error("Path is not a folder")
        raise FunctionFailed from Exception

    return validated_path


def is_exist_json(folderpath):
    """it checks either 'json' file exists or not"""
    filepath = f"{os.path.join(folderpath, 'result.json')}"
    if os.path.isfile(filepath):
        json_existed = filepath
    else:
        logger.error("<%s> does not contain 'result.json' file", folderpath)
        raise FunctionFailed from Exception

    return json_existed


def read_json(filepath):
    """it reads json data, if valid json returns
    the data otherwise exit the program"""
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            json_file = json.load(file)
        except json.decoder.JSONDecodeError as err:
            logger.error("Invalid JSON provided <%s>", err)
            raise FunctionFailed from Exception
        return json_file


def sort_data(args, messages):
    """it sorts the json data, 'asc' for ascending,
    'desc' for descending. by default sorted by 'desc'"""
    if args.sort == "desc":
        messages.reverse()
    elif args.sort != "asc":
        logger.error("sort order mismatch")
        raise FunctionFailed from Exception


def output_file(folderpath):
    """for output file name, default file name is current
    timestamp from step 60 'output-2021-09-26 0110.html'"""
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H%M")
    default_file_name = f"result-{dt_string}.html"
    output_path = os.path.join(folderpath, default_file_name)
    return output_path


def create_html_with_jinja(args, folderpath, json_data):
    """it creates the html file from json data by using jinja"""
    messages = json_data["messages"]
    # to sort order od data
    sort_data(args, messages)
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    rendered = env.get_template("template.html").render(
        content=json_data, messages=messages
    )

    # write html to a file - index.html in root folder
    with open(output_file(folderpath), "w", encoding="utf-8") as file:
        file.write(rendered)

    logger.info("HTML file created")


def create_log():
    """it creates log file, default file name is current timestamp
    "log-20210928220001.log" year month date hour minute seconds"""
    if not os.path.isdir("logs"):
        os.mkdir("logs")
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        logfile(os.path.join("logs", f"log-{dt_string}.log"))
        logger.info("Logs folder created")
    else:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        logfile(os.path.join("logs", f"log-{dt_string}.log"))


def main():
    """ Main entry point of the app """
    try:
        create_log()
        parser = argparse.ArgumentParser()
        # Required positional argument
        parser.add_argument("arg", help="Use for source file path, this is required.")
        # for sorting order, 'asc' for ascending, 'desc' for descending. by default sorted by 'desc'
        parser.add_argument(
            "-s",
            dest="sort",
            default="desc",
            help="""To sord post, use 'asc' for ascending,
                    'desc' for descending order. by default sorted by 'desc'""",
        )
        if len(sys.argv) == 1:
            logger.error("Source file was not provided.")
            parser.print_help()
            raise FunctionFailed from Exception
        args = parser.parse_args()
        # path from cmd
        path = args.arg
        # folder path after validation
        folderpath = validate_path_folder(path)
        # json file path
        json_path = is_exist_json(folderpath)
        # json data
        json_data = read_json(json_path)
        # html creating by using jinja
        create_html_with_jinja(args, folderpath, json_data)
        sys.exit(0)
    except FunctionFailed:
        logger.error("Program terminated unspectedly")
        sys.exit(1)


if __name__ == "__main__":
    main()
