import threading
from filesharing.local.flaskapp import app
import config
from urllib.parse import quote


def main():
    app.run(host=config.host, port=config.port, debug=True, use_reloader=False)


threading.Thread(target=main).start()

from lib import Novel


def get_url(filename, novel: Novel):
    return f"http://{config.host}:{config.port}/download/{quote(novel.source)}/{quote(novel.real_name)}/{quote(filename)}"
