from flask import Flask
from flask import send_from_directory
import pathlib

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/download/<foldername>/<filename>")
def download(foldername, filename):
    # pathlib.Path().resolve() is the working directory
    return send_from_directory(
        pathlib.Path().resolve() / "novels" / foldername, filename
    )
