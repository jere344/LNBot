import lib
import discord.ext.commands.context as Context
import time


@lib.bot.command()
@lib.LnBotDecorator(
    help_message="UwU",
)
async def spin(ctx: Context):
    to_spin = "UwU"
    message = await ctx.send(to_spin[0])
    len_to_spin = len(to_spin)
    for i in range(200):
        time.sleep(0.1)
        await message.edit(content=" " + to_spin[0 : i % len_to_spin + 1])
