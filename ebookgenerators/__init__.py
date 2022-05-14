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


from lib import Novel


def DeleteEbook(novel: Novel):
    """Call this when a novel is updated to delete outdated book files"""
    path = f"novels/{novel.source}/{novel.real_name}"
    for ext in extensions.values():
        try:
            os.remove(f"{path}/{GetEbookFileName(novel.title)}{ext}")
        except FileNotFoundError:
            pass
