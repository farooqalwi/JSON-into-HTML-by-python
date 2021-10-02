"""
This script is used to convert json to html
"""
import json
from jinja2 import Environment, FileSystemLoader

with open("result.json", "r", encoding="utf-8") as f:
    content = json.load(f)

fileLoader = FileSystemLoader("templates")
env = Environment(loader=fileLoader)
rendered = env.get_template("template.html").render(content=content)

# write html to a file - index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered)
