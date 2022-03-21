import functools
from typing import Callable
from discord.ext import commands
import json
import inspect


def save_json(location, content) -> None:
    with open(location, "w", encoding="utf-8") as file:
        json.dump(content, file)


class Client(commands.Bot):
    async def on_message(self, message):
        if message.author == self.user:
            return

        return await super().on_message(message)


bot = Client(command_prefix=".", help_command=None)

dict_of_help_command = {}


class CommandHelp:
    def __init__(self, func: Callable, message=None, exemple=None) -> None:
        if not message:
            self.message = "No help availible for this command"
        else:
            self.message = message

        if not exemple:

            self.exemple = (
                func.__name__
                + " "
                + "".join(
                    [
                        f"<{str(e).split('=')[0]}>? " if "=" in str(e) else f"<{e}> "
                        for e in inspect.signature(func).parameters.values()
                    ][1:]
                )
            )
        else:
            self.exemple = exemple


def LnBotDecorator(help_message=False, help_exemple=False, hidden=False):
    def decorator(func: Callable):
        # This is called when a function is defined
        # Add function informations to generate the help function dynamically
        if not hidden:
            dict_of_help_command[func.__name__] = CommandHelp(
                func, help_message, help_exemple
            )

        @functools.wraps(func)
        async def wrapper(ctx, *args, **kwargs):

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator


@bot.command()
@LnBotDecorator(help_exemple="help rp")
async def help(ctx, commande=None):
    if commande:
        if commande not in dict_of_help_command:
            ctx.send("Cette commande n'existe pas")
            return
        await ctx.send(
            f"```\n.{dict_of_help_command[commande].exemple}\n>>> {dict_of_help_command[commande].message}\n```"
        )
    else:
        help_message = "\n".join(
            [
                f"{key:20s} .{value.exemple}\n"
                for key, value in dict_of_help_command.items()
            ]
        )

        await ctx.send(f"```\n{help_message}\n```")
