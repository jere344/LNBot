import discord.ext.commands.context as Context
import discord
import lib
from asyncio.exceptions import TimeoutError


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


async def check_which(ctx: Context, novels_found: tuple):

    # Ask user which novel to download : list all novel founds and place reactions
    novel_list_message = "\n".join(
        f"{reaction_list[i]} : [{source}] {title}"
        for i, (title, novel, source) in enumerate(novels_found)
    )
    message = await ctx.send(
        f"{len(novels_found)} novel{'' if len(novels_found) == 1 else 's'} founds :```{novel_list_message}```"
    )
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
