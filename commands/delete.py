import lib
import discord.ext.commands.context as Context
from sources import lightnovelworld
import _misc_ as misc
import os
from lnbotdecorator import LnBotDecorator


@lib.bot.command()
@LnBotDecorator()
async def delete(ctx: Context, password: str, *novel):
    if password != "oursbrun":
        # I know storing password in clear stuck but good enough for my use
        await ctx.send("Wrong password")
        return

    novel = " ".join(novel)

    novels_found = lightnovelworld.Search(novel)
    # novel_fund is a list of tupple of (user_readable_name, real_name)

    if not novels_found:
        await ctx.send(f"No novel found")
        return

    if len(novels_found) > len(misc.reaction_list):
        await ctx.send(f"Too many novels founds, please enter a more precize search")
        return

    real_name = await misc.check_which(ctx, novels_found)[1]
    os.rmdir(f"novels/{real_name}")
