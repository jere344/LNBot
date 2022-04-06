from flask import Flask
from flask import send_from_directory, abort
import pathlib

app = Flask(__name__)
novels_path = pathlib.Path().resolve().joinpath("novels")
app.config["UPLOAD_FOLDER"] = novels_path


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/download/<foldername>/<filename>")
def download(foldername, filename):
    try:
        return send_from_directory(
            directory=app.config["UPLOAD_FOLDER"],
            path=foldername,
            filename=filename,
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)


import threading


def main():
    app.run(port=5000, debug=True, use_reloader=False)


app_thread = threading.Thread(target=main).start()
