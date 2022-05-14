import os
import discord
import ebookgenerators
import config
from lib import Novel

if config.sharing_small == "local" or config.sharing_large == "local":
    import filesharing.local


async def SendEbook(ctx, novel: Novel, ebook_type):
    if novel.source == "local":
        if not ebook_type in novel.ebook_path:
            await ctx.send(f"No {ebook_type} found for {novel.title}")
            return
        file_path = novel.ebook_path[ebook_type]
        filename = os.path.basename(file_path)

    else:
        filename = f"{ebookgenerators.GetEbookFileName(novel.title)}{ebookgenerators.extensions[ebook_type]}"
        file_path = f"novels/{novel.source}/{novel.real_name}/{filename}"

        if not os.path.isfile(file_path):
            ebookgenerators.ebook_generators[ebook_type].Generate(file_path, novel)

    if os.path.getsize(file_path) < 8_000_000:
        if config.sharing_small == "discord":
            await ctx.send(file=discord.File(file_path))
        if config.sharing_small == "local":
            await ctx.send(filesharing.local.get_url(filename, novel))
    else:
        if config.sharing_large == "discord":
            await ctx.send(file=discord.File(file_path))
        if config.sharing_large == "local":
            await ctx.send(filesharing.local.get_url(filename, novel))
