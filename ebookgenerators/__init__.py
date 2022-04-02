from ebookgenerators import lnbotepub
from ebookgenerators import raw
import discord
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


async def SendEbook(ctx, real_name, user_readable_name, ebook_type):

    file_path = f"novels/{real_name}/{GetEbookFileName(user_readable_name)}{extensions[ebook_type]}"

    if not os.path.isfile(file_path):
        ebook_generators[ebook_type].Generate(real_name, file_path)

    await ctx.send(file=discord.File(rf"{file_path}"))


def DeleteEbook(real_name, user_readable_name):
    """Call this when a novel is updated to delete outdated book files"""
    path = f"novels/{real_name}"
    for ext in extensions.values():
        try:
            os.remove(f"{path}/{GetEbookFileName(user_readable_name)}{ext}")
        except FileNotFoundError:
            pass
