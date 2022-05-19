import lib
import discord.ext.commands.context as Context
import time
from lnbotdecorator import LnBotDecorator


@lib.bot.command()
@LnBotDecorator(help_message="UwU", hidden=True)
async def spin(ctx: Context):
    """UwU"""
    to_spin = "UwU"
    message = await ctx.send(to_spin[0])
    len_to_spin = len(to_spin)
    for i in range(200):
        time.sleep(0.1)
        await message.edit(content=" " + to_spin[0 : i % len_to_spin + 1])
