# from messages import *
from pathlib import Path
from lib import Novel
import config

# from lib import Novel

lang = ["all"]
source = "local"


def Search(search_query):
    """Fetch the list of novel matching search_query.
    Is sensitive to the order of words, to lower/uppercase and any special character"""
    novels_found = []

    match = "*" + search_query.replace(" ", "*") + "*"
    i = 0
    for lang, path in config.libraries.items():
        for file in Path(path).rglob(match):
            if file.is_file():
                novel = Novel(file.stem, file.name, "local", lang)
                novel.ebook_path = file
                novels_found.append(novel)
                i += 1

                if i > 50:
                    break

    return novels_found
