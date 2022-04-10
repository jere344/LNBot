import threading
from filesharing.local.flaskapp import app
import config
from urllib.parse import quote


def main():
    app.run(host=config.host, port=config.port, debug=True, use_reloader=False)


threading.Thread(target=main).start()


def get_url(novel, filename, source):
    return f"http://{config.host}:{config.port}/download/{quote(source + ' - ' + novel)}/{quote(filename)}"
