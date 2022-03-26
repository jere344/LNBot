import lib
from sources import lightnovelworld
import _misc_ as misc
import os
from lnbotdecorator import LnBotDecorator
import shutil


@lib.bot.command()
@LnBotDecorator()
async def delete(ctx, password: str, *novel):
    await ctx.message.delete()
    if not novel:
        return

    if password != "oursbrun":
        # I know storing password in clear stuck but good enough for my use
        await ctx.send("Wrong password")
        return

    novel = " ".join(novel)

    # If it's a folder, just delete it
    if os.path.isdir(f"novels/{novel}"):
        shutil.rmtree(f"novels/{novel}")
        return
    # else it's probably a novel name so we need to check which

    novels_found = lightnovelworld.Search(novel)

    if not novels_found:
        await ctx.send(f"No novel found")
        return

    if len(novels_found) > len(misc.reaction_list):
        await ctx.send(f"Too many novels founds, please enter a more precize search")
        return

    _, real_name, *_ = await misc.ask_which(ctx, novels_found)
    try:
        shutil.rmtree(f"novels/{real_name}")
    except FileNotFoundError:
        await ctx.send("Novel not downloaded")
        return

    await ctx.send("Novel deleted")
