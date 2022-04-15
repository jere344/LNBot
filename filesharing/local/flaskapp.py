from flask import Flask
from flask import send_from_directory
import lib

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/download/<foldername>/<filename>")
def download(foldername, filename):
    absolute_novel_path = lib.novel_path.absolute()
    folder_path = absolute_novel_path / foldername

    if folder_path.parent != absolute_novel_path:
        return "Invalid path"
    else:
        return send_from_directory(folder_path, filename)
