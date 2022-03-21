import lib
import discord.ext.commands.context as Context
import random


@lib.bot.command()
@lib.LnBotDecorator(
    help_message="Défit le bot au ping-pong. Vous allez perdre.",
)
async def ping(ctx: Context):
    await ctx.send("pong")
