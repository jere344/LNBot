import lib
import sources
import _misc_ as misc
from messages import *
from lnbotdecorator import LnBotDecorator
import json
import discord


@lib.bot.command()
@LnBotDecorator(help_message="Download novel")
async def info(ctx, *novel):
    novel, arguments = misc.parse_novel_and_arguments(*novel)

    novels_found = sources.Search(novel, arguments)
    # novel_fund is a list of tupple of (user_readable_name, real_name, source)

    if not novels_found:
        await misc.send(ctx, NoNovelFound(), arguments)
        return
    if len(novels_found) > len(misc.reaction_list):
        await misc.send(ctx, TooManyFound(), arguments)
        return

    selected = await misc.ask_which(ctx, novels_found)
    if not selected:
        return

    user_readable_name, real_name, source, *_ = selected

    try:
        with open(
            lib.novel_path / f"{source} - {real_name}" / "metadata.json", "r"
        ) as file:
            metadata = json.loads(file.read())
    except FileNotFoundError:
        await misc.send(ctx, NovelNotDownloaded(), arguments)
        return

    # We don't know the extension of the file
    for file in lib.novel_path / f"{source} - {real_name}":
        if file.stem == "cover":
            break

    await ctx.send(file=discord.File(lib.novel_path / f"{source} - {real_name}" / file))

    await ctx.send(
        f"""
**Summary :**
{metadata['summary']}

**Latest :**
{metadata["latest"]}

**url :**
{metadata['url']}
"""
    )
