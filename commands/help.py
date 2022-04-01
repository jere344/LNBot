import lib
from lnbotdecorator import LnBotDecorator
import config


@lib.bot.command()
@LnBotDecorator(help_exemple="help ping")
async def help(ctx, commande=None):
    if commande:
        if commande not in lib.dict_of_help_command:
            ctx.send("Cette commande n'existe pas")
            return
        await ctx.send(
            f"```\n{config.command_prefix}{lib.dict_of_help_command[commande].exemple}\n>>> {lib.dict_of_help_command[commande].message}\n```"
        )
    else:
        help_message = "\n".join(
            [
                f"{key:20s} {config.command_prefix}{value.exemple}\n"
                for key, value in lib.dict_of_help_command.items()
            ]
        )

        await ctx.send(f"```\n{help_message}\n```")
