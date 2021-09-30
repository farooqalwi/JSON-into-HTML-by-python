import json
from jinja2 import Environment, FileSystemLoader

with open("result.json", "r", encoding="utf-8") as f:
    content = json.load(f)

postNumber = len(content["messages"])

fileLoader = FileSystemLoader("templates")
env = Environment(loader=fileLoader)
rendered = env.get_template("template.html").render(
    content=content, postNumber=postNumber
)

# write html to a file - index.html
fileName = "index.html"
with open(fileName, "w", encoding="utf-8") as f:
    f.write(rendered)
