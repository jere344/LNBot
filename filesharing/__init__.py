import os
import discord
import ebookgenerators
import config
from lib import Novel
import pathlib

if config.sharing_small == "local" or config.sharing_large == "local":
    import filesharing.local

    # importing filesharing.local start a new thread for flask th handle download request


async def SendEbook(ctx, novel: Novel, ebook_type=None) -> None:
    """Send the ebook the novel.
    the local source do not have an ebook_type.
    For this source the novel variable contain an ebook_path"""
    if novel.source != "local":
        filename = f"{ebookgenerators.GetEbookFileName(novel.title)}{ebookgenerators.extensions[ebook_type]}"
        novel.ebook_path = (
            pathlib.Path().resolve()
            / "novels"
            / novel.source
            / novel.real_name
            / filename
        )

    if not os.path.isfile(novel.ebook_path):
        ebookgenerators.ebook_generators[ebook_type].Generate(novel)

    if os.path.getsize(novel.ebook_path) < 8_000_000:
        if config.sharing_small == "discord":
            await ctx.send(file=discord.File(novel.ebook_path))
        if config.sharing_small == "local":
            await ctx.send(filesharing.local.get_url(novel))
    else:
        if config.sharing_large == "discord":
            await ctx.send(file=discord.File(novel.ebook_path))
        if config.sharing_large == "local":
            await ctx.send(filesharing.local.get_url(novel))
