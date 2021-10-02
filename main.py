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
    The caller will not recevie any other exception"""


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


def write_basic_chennal_info(json_data):
    """it writes the chennal basic info,
    i.e: chenal name, chennal type, chennal link"""
    channel_name = json_data["name"]
    channel_type = json_data["type"]
    return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>JSON to HTML</title>
                </head>
                <body>
                <h1>{channel_name}</h1>
                <a href="https://t.me/themuslimarchive">https://t.me/themuslimarchive</a>
                <p>{channel_type}</p>
            """


def output_file(folderpath):
    """for output file name, default file name is current
    timestamp from step 60 'output-2021-09-26 0110.html'"""
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H%M")
    default_file_name = f"result-{dt_string}.html"
    output_path = os.path.join(folderpath, default_file_name)
    return output_path


def validate_image_html(folderpath, message, post_id):
    """it valliadtes images either present or not"""
    photo_existed = ""
    if "photo" in message.keys():
        photo = message["photo"]
        photo_dir = photo[0:7]
        if os.path.isdir(os.path.join(folderpath, photo_dir)):
            if os.path.isfile(os.path.join(folderpath, photo)):
                photo_existed = photo
            else:
                logger.error("<%s> image not found", photo)
        else:
            logger.error(
                "<%s> directory not found", os.path.join(folderpath, photo_dir)
            )
            raise FunctionFailed from Exception

    else:
        logger.error("image not found at Post ID: %s", post_id)
    return photo_existed


def text_formatting(list_text):
    """it checks bold, code, italic, underline, strikethrough type"""
    if list_text["type"] == "bold":
        whole_text = f"""<strong>{list_text["text"]}</strong>"""
    elif list_text["type"] == "code":
        whole_text = f"""<code>{list_text["text"]}</code>"""
    elif list_text["type"] == "italic":
        whole_text = f"""<em>{list_text["text"]}</em>"""
    elif list_text["type"] == "underline":
        whole_text = f"""<u>{list_text["text"]}</u>"""
    elif list_text["type"] == "strikethrough":
        whole_text = f"""<s>{list_text["text"]}</s>"""

    return whole_text


def write_text_html(text):
    """it writes texts with respective formatting"""
    whole_text = ""
    for list_text in text:
        if list_text != " ":
            if isinstance(list_text, str):
                whole_text += list_text
            elif isinstance(list_text, dict):
                if (
                    list_text["type"] == "bold"
                    or list_text["type"] == "code"
                    or list_text["type"] == "italic"
                    or list_text["type"] == "underline"
                    or list_text["type"] == "strikethrough"
                ):
                    whole_text += text_formatting(list_text)
                elif list_text["type"] == "link":
                    whole_text += (
                        f"""<a href="{list_text["text"]}">{list_text["text"]}</a>"""
                    )
                elif list_text["type"] == "text_link":
                    whole_text += (
                        f"""<a href="{list_text["href"]}">{list_text["text"]}</a>"""
                    )
                elif list_text["type"] == "hashtag":
                    whole_text += f"""<a href="#" style="text-decoration:none">
                                    {list_text["text"]} </a>"""
                elif list_text["type"] == "mention":
                    whole_text += f"""<a href="https://t.me/
                                    {list_text["text"][1:]}">{list_text["text"]}</a>"""
                elif list_text["type"] == "email":
                    whole_text += f"""<a href="mailto:
                                    {list_text["text"]}">{list_text["text"]}</a>"""
                elif list_text["type"] == "phone":
                    whole_text += (
                        f"""<a href="tel:{list_text["text"]}">{list_text["text"]}</a>"""
                    )
    whole_text = whole_text.replace("\n", "<br>")
    return whole_text


def create_html(args, folderpath, json_data):
    """it creates the html file from json data"""
    messages = json_data["messages"]
    # to sort order od data
    sort_data(args, messages)
    with open(output_file(folderpath), "w", encoding="utf-8") as file:
        file.write(write_basic_chennal_info(json_data))
        for message in messages:
            post_id = message["id"]
            post_date = message["date"]
            file.write(
                f"""
                    <hr>
                    <h2>Date: {post_date}</h2>
                    <p>id: {post_id}</p>
                    """
            )
            photo = validate_image_html(folderpath, message, post_id)
            if photo != "":
                file.write(
                    f"""
                        <img src={photo} style="width: 260px; height: 251px"/>
                        """
                )
            text = message["text"]
            if text != "":
                if isinstance(text, str):
                    file.write(
                        f"""
                                <p>{text}</p>
                            """
                    )
                elif isinstance(text, list):
                    whole_text = write_text_html(text)
                    file.write(
                        f"""
                                <p>{whole_text}</p>
                            """
                    )
        file.write(
            """
                    </body>
                </html>
                """
        )
    logger.info("HTML file created")


def create_html_with_jinja(json_data):
    """it creates the html file from json data by using jinja"""
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    rendered = env.get_template("template.html").render(content=json_data)

    # write html to a file - index.html in root folder
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered)


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
        # html creating
        create_html(args, folderpath, json_data)
        # html creating by using jinja
        create_html_with_jinja(json_data)
        sys.exit(0)
    except FunctionFailed:
        logger.error("Program terminated unspectedly")
        sys.exit(1)


if __name__ == "__main__":
    main()
