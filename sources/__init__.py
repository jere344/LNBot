# import glob
# import importlib


# file_list = glob.glob("sources/[!_]*")
# module_list = [
#     e.replace(".py", "").replace("\\", ".").replace("/", ".") for e in file_list
# ]

# for module in module_list:
#     print(module)
#     importlib.import_module(module)

import sources.lightnovelworld as lightnovelworld
import sources.readlightnovel as readlightnovel

# import sources.local as local

from lib import Novel

sources = [lightnovelworld, readlightnovel]


async def DownloadNovel(message, novel: Novel):
    if novel.source == "lightnovelworld":
        await lightnovelworld.DownloadNovel(message, novel)
    elif novel.source == "readlightnovel":
        await readlightnovel.DownloadNovel(message, novel)
    else:
        print("unknown source")


def Search(novel, arguments):
    result = []
    for source in sources:
        if arguments["lang"] == "all" or arguments["lang"] in source.lang:
            if arguments["source"] == "all" or arguments["source"] in source.source:

                result += source.Search(novel)

    return result
