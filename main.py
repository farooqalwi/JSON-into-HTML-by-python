#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


import argparse
from genericpath import isdir
from logzero import logger, logfile
import json
import sys
import os
from datetime import datetime

class FunctionFailed(Exception):
    """We use this custom exception whenver our function fails for any reason
    The caller will not recevie any other exception"""


def validatePath_folder(path):
    """this function validates user given folder path, 
    incase valid path returns the path"""
    if(os.path.isdir(path)):
        return path
    else:
        logger.error("Path is not a folder")
        raise FunctionFailed from Exception

def isExist_JSON(folderPath):
    """it checks either 'json' file exists or not"""
    filePath = f"{os.path.join(folderPath, 'result.json')}"
    if(os.path.isfile(filePath)):
        return filePath
    else:
        logger.error(f"<{folderPath}> does not contain 'result.json' file")
        raise FunctionFailed from Exception

def readJson(filePath):
    """it reads json data, if valid json returns 
    the data otherwise exit the program"""
    with open(filePath, "r", encoding='utf-8') as f:
        try:
            json_file = json.load(f)
        except json.decoder.JSONDecodeError as err:
            logger.error(f"Invalid JSON provided <{err}>")
            raise FunctionFailed from Exception
        return json_file

def sortData(messages):
    """it sorts the json data, 'asc' for ascending, 
    'desc' for descending. by default sorted by 'desc'"""
    if(args.sort == "desc"):
        messages.reverse()
    elif(args.sort != "asc"):
        logger.error("sort order mismatch")
        raise FunctionFailed from Exception

def writeBasicInfo_Chennal(json_data):
    """it writes the chennal basic info, 
    i.e: chenal name, chennal type, chennal link"""
    channelName = json_data["name"]
    channelType = json_data["type"]
    return (f"""
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

def outputFile(folderPath):
    """for output file name, default file name is current
    timestamp from step 60 'output-2021-09-26 0110.html' """
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H%M")
    defaultFileName = f"result-{dt_string}.html"
    outputPath = os.path.join(folderPath, defaultFileName)
    return outputPath

def validateImage_HTML(folderPath, message, postID):
    """it valliadtes images either present or not"""
    if("photo" in message.keys()):
        photo = message["photo"]
        photoDir = photo[0:7]
        if(os.path.isdir(os.path.join(folderPath, photoDir))):
            if(os.path.isfile(os.path.join(folderPath, photo))):
                return photo
            else:
                logger.error(f"<{photo}> image not found")
        else:
            logger.error(f"<{os.path.join(folderPath, photoDir)}> directory not found")
            raise FunctionFailed from Exception
    else:
        logger.error(f"image not found at Post ID: {postID}")

def writeText_HTML(text):
    """it writes texts with respective formatting"""
    wholeText = ""
    for listText in text:
        if(listText != " "):
            if(type(listText) == str):
                wholeText += listText
            elif(type(listText) == dict):
                if(listText["type"] == "bold"):
                    wholeText+= f"""<strong>{listText["text"]}</strong>"""
                elif(listText["type"] == "code"):
                    wholeText+= f"""<code>{listText["text"]}</code>"""
                elif(listText["type"] == "italic"):
                    wholeText+= f"""<em>{listText["text"]}</em>"""
                elif(listText["type"] == "underline"):
                    wholeText+= f"""<u>{listText["text"]}</u>"""
                elif(listText["type"] == "strikethrough"):
                    wholeText+= f"""<s>{listText["text"]}</s>"""
                elif(listText["type"] == "link"):
                    wholeText+= f"""<a href="{listText["text"]}">{listText["text"]}</a>"""
                elif(listText["type"] == "text_link"):
                    wholeText+= f"""<a href="{listText["href"]}">{listText["text"]}</a>"""
                elif(listText["type"] == "hashtag"):
                    wholeText+= f"""<a href="#" style="text-decoration:none">{listText["text"]} </a>"""
                elif(listText["type"] == "mention"):
                    wholeText+= f"""<a href="https://t.me/{listText["text"][1:]}">{listText["text"]}</a>"""
                elif(listText["type"] == "email"):
                    wholeText+= f"""<a href="mailto:{listText["text"]}">{listText["text"]}</a>"""
                elif(listText["type"] == "phone"):
                    wholeText+= f"""<a href="tel:{listText["text"]}">{listText["text"]}</a>"""
    wholeText = wholeText.replace("\n", "<br>")
    return wholeText

def create_HTML(folderPath, json_data):
    """it creates the html file from json data"""
    messages = json_data["messages"]
    # to sort order od data
    sortData(messages)
    with open(outputFile(folderPath), 'w', encoding='utf-8') as f:
        f.write(writeBasicInfo_Chennal(json_data))
        for message in messages:
            postID = message["id"]
            postDate = message["date"]
            f.write(f"""
                    <hr>
                    <h2>Date: {postDate}</h2>
                    <p>id: {postID}</p>
                    """)
            photo = validateImage_HTML(folderPath, message, postID)
            f.write(f"""
                    <img src={photo} style="width: 260px; height: 251px"/>
                    """)
            text = message["text"]
            if(text != ""):
                if(type(text) == str):
                    f.write(f"""
                                <p>{text}</p>
                            """)
                elif(type(text) == list):
                    wholeText = writeText_HTML(text)
                    f.write(f"""
                                <p>{wholeText}</p>
                            """)
        f.write("""
                    </body>
                </html>
                """)
    logger.info("HTML file created")

def createLog():
    """it creates log file, default file name is current timestamp 
    "log-20210928220001.log" year month date hour minute seconds"""
    if(not os.path.isdir("logs")):
        os.mkdir("logs")
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        logfile(os.path.join("logs", f"log-{dt_string}.log"))
        logger.info("Logs folder created")
    else:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        logfile(os.path.join("logs", f"log-{dt_string}.log"))

def main(args):
    """ Main entry point of the app """
    try:
        # path from cmd
        path = args.arg

        # folder path after validation
        folderPath = validatePath_folder(path)

        # json file path
        jsonPath = isExist_JSON(folderPath)

        # json data
        json_data = readJson(jsonPath)

        # html creating
        create_HTML(folderPath, json_data)

        sys.exit(0)
    except FunctionFailed:
        logger.error("Program terminated unspectedly")
        sys.exit(1)



if __name__ == "__main__":
    """ This is executed when run from the command line """ 
    createLog()
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Use for source file path, this is required.")

    # for sorting order, 'asc' for ascending, 'desc' for descending. by default sorted by 'desc'
    parser.add_argument("-s", dest="sort", default="desc", help="To sord post, use 'asc' for ascending, 'desc' for descending order. by default sorted by 'desc'")

    if len(sys.argv) == 1:
        logger.error("Source file was not provided.")
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    main(args)