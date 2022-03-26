import lib
import discord.ext.commands.context as Context
from lnbotdecorator import LnBotDecorator


@lib.bot.command()
@LnBotDecorator(
    help_message="Défit le bot au ping-pong. Vous allez perdre.",
)
async def ping(ctx: Context):
    await ctx.send("pong")
