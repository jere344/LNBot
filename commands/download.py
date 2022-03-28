import lib
import sources
import _misc_ as misc
from messages import *
from lnbotdecorator import LnBotDecorator
import lnbotepub


@lib.bot.command()
@LnBotDecorator(help_message="Download novel")
async def download(ctx, *novel):
    arguments = {
        "v": config.v,
        "pdf": config.pdf,
        "console": config.console,
        "epub": config.epub,
        "lang": config.download_lang,
        "source": config.source,
    }

    # Check if there are argument at the end (ex : .download lord of the mysteries -f -pdf)
    # And change the argument dict depending of that
    for e in reversed(novel):
        if e.startswith("-"):
            arg = e[1:]
            if arg in arguments:
                # Not a common behaviour but the easiest one I found here
                # Option do not set to enabled, but switch state
                arguments[arg] = not arguments[arg]

                # Remove argument from the novel name
                novel = novel[:-1]
            elif ":" in arg:
                arg, value = arg.split(":")
                arguments[arg] = value

                novel = novel[:-1]
        else:
            break

    novel = " ".join(novel)

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

    user_readable_name, real_name, source = selected

    message = await misc.send(ctx, DownloadingNovel(user_readable_name), arguments)
    await sources.DownloadNovel(message, user_readable_name, real_name, source)

    await misc.edit(message, NovelDownloaded(user_readable_name), arguments)

    if arguments["epub"]:
        await misc.edit(message, SendingEpub(), arguments)
        await lnbotepub.send_epub(ctx, real_name, user_readable_name)
