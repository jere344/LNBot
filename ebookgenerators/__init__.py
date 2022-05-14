from ebookgenerators import lnbotepub
from ebookgenerators import raw
import os

ebook_generators = {
    "epub": lnbotepub,
    "raw": raw,
}
extensions = {
    "epub": ".epub",
    "pdf": ".pdf",
    "raw": ".zip",
}


def GetEbookFileName(title):
    illegal = """\/:*?"<>|"""
    for char in illegal:
        title.replace(char, " ")
    return title


def DeleteEbook(real_name, user_readable_name, source):
    """Call this when a novel is updated to delete outdated book files"""
    path = f"novels/{source}/{real_name}"
    for ext in extensions.values():
        try:
            os.remove(f"{path}/{GetEbookFileName(user_readable_name)}{ext}")
        except FileNotFoundError:
            pass
