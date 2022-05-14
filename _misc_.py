import discord.ext.commands.context as Context
import discord
import lib
from asyncio.exceptions import TimeoutError
from lib import Novel
from messages import NovelFounds


reaction_list = [
    "0️⃣",
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟",
]


async def ask_which(ctx: Context, novels_found: list[Novel]) -> Novel:

    # Ask user which novel to download : list all novel founds and place reactions
    novel_list_message = "\n".join(
        f"{reaction_list[i]} : [{novel.lang}][{novel.source}] {novel.title}"
        for i, novel in enumerate(novels_found)
    )
    message = await ctx.send(NovelFounds(len(novels_found), novel_list_message))
    for i in range(len(novels_found)):
        await message.add_reaction(reaction_list[i])

    # Check for reaction
    def check(reaction, user):
        return (
            user == ctx.author
            and str(reaction.emoji) in reaction_list[: i + 1]
            and reaction.message == message
        )

    try:
        reaction: discord.reaction.Reaction
        reaction, *_ = await lib.bot.wait_for("reaction_add", timeout=60.0, check=check)
    except TimeoutError:
        return

    return novels_found[reaction_list.index(reaction.emoji)]


class placeholderMessage:
    async def send(self, message):
        print(message)

    async def edit(self, content):
        print(content)


async def send(ctx, message, argument):
    if argument["console"]:
        print(message)
    if argument["v"]:
        return await ctx.send(message)

    return placeholderMessage()


async def edit(message, content, argument):
    if argument["console"]:
        print(content)

    return await message.edit(content=content)


import config


def parse_novel_and_arguments(*novel):
    arguments = {
        "v": config.v,
        "pdf": config.pdf,
        "console": config.console,
        "epub": config.epub,
        "lang": config.download_lang,
        "source": config.source,
        "raw": config.raw,
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
    return novel, arguments
