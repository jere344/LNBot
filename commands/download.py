import lib
import discord.ext.commands.context as Context
import discord
import sources
import _misc_ as misc
import epubgenerator


@lib.bot.command()
@lib.LnBotDecorator(help_message="Download novel")
async def download(ctx: Context, *novel):
    novel = " ".join(novel)

    novels_found = sources.Search(novel)
    # novel_fund is a list of tupple of (user_readable_name, real_name, source)

    if not novels_found:
        await ctx.send(f"No novel found")
        return

    if len(novels_found) > len(misc.reaction_list):
        await ctx.send(f"Too many novels founds, please enter a more precize search")
        return

    selected = await misc.check_which(ctx, novels_found)
    if not selected:
        return

    user_readable_name, real_name, source = selected

    message = await ctx.send(f"Downloading {user_readable_name}")
    await sources.DownloadNovel(message, user_readable_name, real_name, source)

    await message.edit(content=f"{user_readable_name} downloaded, sending...")
    await ctx.send(
        file=discord.File(
            rf"novels/{real_name}/{epubgenerator.GetEbookFileName(user_readable_name)}"
        )
    )
