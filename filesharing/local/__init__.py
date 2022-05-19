import threading
from filesharing.local.flaskapp import app
import config
import pathlib
from urllib.parse import quote


def main():
    app.run(host=config.host, port=config.port, debug=True, use_reloader=False)


threading.Thread(target=main).start()

from lib import Novel


def get_url(novel: Novel):
    """Generate an url to download the novel using the local host method"""
    return f"http://{config.host}:{config.port}/download/{quote(str(novel.ebook_path))}"
