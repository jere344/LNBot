import threading
from filesharing.local.flaskapp import app
import config


def main():
    app.run(host=config.host, port=config.port, debug=True, use_reloader=False)


threading.Thread(target=main).start()


def get_url(novel, filename):
    return f"http://{config.host}:{config.port}/download/{novel}/{filename}"
