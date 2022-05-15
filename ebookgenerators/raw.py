import zipfile
import os
from lib import Novel


def Generate(novel: Novel):
    # shutil.make_archive(file_path[:-4], "zip", f"novels/{source}/{novel_real_name}/c")
    # # [:-4] to avoid .zip.zip
    zf = zipfile.ZipFile(novel.ebook_path, "w")

    novel_root_path = f"novels/{novel.source}/{novel.real_name}"
    for file in os.listdir(f"{novel_root_path}/chapters"):
        zf.write(f"{novel_root_path}/chapters/{file}")

    zf.write(f"{novel_root_path}/metadata.json")

    # Find cover path
    for file in os.listdir(novel_root_path):
        if file[:5] == "cover":
            break
    zf.write(f"{novel_root_path}/{file}")
