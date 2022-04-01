import lib
import sources
import _misc_ as misc
from messages import *
from lnbotdecorator import LnBotDecorator
import ebookgenerators


@lib.bot.command()
@LnBotDecorator(
    help_message=DownloadHelpMessage().__str__(),  # I don't know why I need to use __str__() here but it doesn't work without it
    help_exemple="download lord of the mysteries",
)
async def download(ctx, *novel):
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

    message = await misc.send(ctx, DownloadingNovel(user_readable_name), arguments)
    await sources.DownloadNovel(message, user_readable_name, real_name, source)

    await misc.edit(message, NovelDownloaded(user_readable_name), arguments)

    if arguments["epub"]:
        await misc.edit(message, SendingEbook("epub"), arguments)
        await ebookgenerators.SendEbook(ctx, real_name, user_readable_name, "epub")
    if arguments["raw"]:
        await misc.edit(message, SendingEbook("raw"), arguments)
        await ebookgenerators.SendEbook(ctx, real_name, user_readable_name, "raw")
