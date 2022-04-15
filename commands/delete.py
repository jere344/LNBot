import lib
from sources import lightnovelworld
import _misc_ as misc
from lnbotdecorator import LnBotDecorator
import shutil


@lib.bot.command()
@LnBotDecorator()
async def delete(ctx, password: str, *novel):
    if not novel:
        return

    if password != "oursbrun":
        # I know storing password in clear stuck but good enough for my use
        await ctx.send("Wrong password")
        return

    novel = " ".join(novel)

    novels_found = lightnovelworld.Search(novel)

    if not novels_found:
        await ctx.send(f"No novel found")
        return

    if len(novels_found) > len(misc.reaction_list):
        await ctx.send(f"Too many novels founds, please enter a more precize search")
        return

    _, real_name, source, _ = await misc.ask_which(ctx, novels_found)
    try:
        shutil.rmtree(lib.novel_path / f"{source} - {real_name}")
    except FileNotFoundError:
        await ctx.send("Novel not downloaded")
        return

    await ctx.send("Novel deleted")
