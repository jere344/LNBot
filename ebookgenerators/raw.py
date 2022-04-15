import zipfile

import lib


def Generate(novel_real_name, file_path, source):
    # shutil.make_archive(file_path[:-4], "zip", f"novels/{source} - {novel_real_name}/c")
    # # [:-4] to avoid .zip.zip
    zf = zipfile.ZipFile(file_path, "w")

    novel_root_path = lib.novel_path / f"{source} - {novel_real_name}"
    for file in (novel_root_path / "chapters").iterdir():
        zf.write(novel_root_path / "chapters" / file)

    zf.write(novel_root_path / "metadata.json")

    # Find cover path
    for file in novel_root_path.iterdir():
        if file[:5] == "cover":
            break
    zf.write(novel_root_path / file)
