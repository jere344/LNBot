import lib
import sources
import _misc_ as misc
from messages import *
from lnbotdecorator import LnBotDecorator
import filesharing


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

    selected = await misc.ask_which(ctx, novels_found)
    if not selected:
        return

    if selected.source == "local":
        extension = selected.ebook_path.suffix[1:]
        await misc.edit(message, SendingEbook(extension), arguments)
        await filesharing.SendEbook(ctx, selected, extension)
        return

    message = await misc.send(ctx, DownloadingNovel(selected.title), arguments)
    await sources.DownloadNovel(message, selected)

    await misc.edit(message, NovelDownloaded(selected.title), arguments)

    if arguments["epub"]:
        await misc.edit(message, SendingEbook("epub"), arguments)
        await filesharing.SendEbook(ctx, selected, "epub")
    if arguments["raw"]:
        await misc.edit(message, SendingEbook("raw"), arguments)
        await filesharing.SendEbook(ctx, selected, "raw")
