# import glob
# import importlib


# file_list = glob.glob("sources/[!_]*")
# module_list = [
#     e.replace(".py", "").replace("\\", ".").replace("/", ".") for e in file_list
# ]

# for module in module_list:
#     print(module)
#     importlib.import_module(module)

import sources.lightnovelworld
import sources.readlightnovel


async def DownloadNovel(message, title, novel, source):
    if source == "lightnovelworld":
        await sources.lightnovelworld.DownloadNovel(message, (title, novel))
    elif source == "readlightnovel":
        await sources.readlightnovel.DownloadNovel(message, title, novel)
    else:
        print("unknown source")


def Search(novel):
    return sources.lightnovelworld.Search(novel) + sources.readlightnovel.Search(novel)
