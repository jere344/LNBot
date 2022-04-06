import os
import discord
import ebookgenerators
import config

if config.sharing_small == "local" or config.sharing_large == "local":
    import filesharing.local


async def SendEbook(ctx, real_name, user_readable_name, ebook_type):
    filename = f"{ebookgenerators.GetEbookFileName(user_readable_name)}{ebookgenerators.extensions[ebook_type]}"
    file_path = f"novels/{real_name}/{filename}"

    if not os.path.isfile(file_path):
        ebookgenerators.ebook_generators[ebook_type].Generate(real_name, file_path)

    if os.path.getsize(file_path) < 8_000_000:
        if config.sharing_small == "discord":
            await ctx.send(file=discord.File(file_path))
        if config.sharing_small == "local":
            await ctx.send(filesharing.local.get_url(real_name, filename))
    else:
        if config.sharing_large == "discord":
            await ctx.send(file=discord.File(file_path))
        if config.sharing_large == "local":
            await ctx.send(filesharing.local.get_url(real_name, filename))
