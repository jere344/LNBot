import lib
import discord.ext.commands.context as Context
import discord
import sources
import _misc_ as misc
import epubgenerator
from messages import *


@lib.bot.command()
@lib.LnBotDecorator(help_message="Download novel")
async def download(ctx: Context, *novel):
    arguments = {
        "f": False,
        "pdf": False,
        "console": False,
    }

    # Check if there are argument at the end (ex : .download lord of the mysteries -f -pdf)
    # And change the argument dict depending of that
    for e in reversed(novel):
        if e.startswith("-"):
            arguments[e[1:]] = True  # [1:] remove the "-"
            novel = novel[:-1]  # Because the argument is not part of the novel name
        else:
            break

    novel = " ".join(novel)

    novels_found = sources.Search(novel)
    # novel_fund is a list of tupple of (user_readable_name, real_name, source)

    if not novels_found:
        await misc.send(ctx, NoNovelFound(), arguments)
        return

    if len(novels_found) > len(misc.reaction_list):
        await misc.send(ctx, TooManyFound(), arguments)
        return

    selected = await misc.check_which(ctx, novels_found)
    if not selected:
        return

    user_readable_name, real_name, source = selected

    message = await misc.send(ctx, DownloadingNovel(user_readable_name), arguments)
    await sources.DownloadNovel(message, user_readable_name, real_name, source)

    await misc.edit(message, NovelDownloaded(user_readable_name), arguments)
    await ctx.send(
        file=discord.File(
            rf"novels/{real_name}/{epubgenerator.GetEbookFileName(user_readable_name)}"
        )
    )
