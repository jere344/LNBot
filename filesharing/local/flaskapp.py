from flask import Flask
from flask import send_file
import pathlib
import config
from urllib.parse import unquote

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/download/<path>")
def download(path):
    path = pathlib.Path(unquote(path))
    if not path.exists():
        return "<p>File not found</p>"
    if path.is_dir():
        return "<p>Directory not supported</p>"

    for library in config.libraries.values():
        if pathlib.Path(library) in path.parents:
            return send_file(path)

    if (pathlib.Path().resolve() / "novels") in path.parents:
        return send_file(path)

    return "<p>Permission denied</p>"
