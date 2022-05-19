import functools
import lib
import CommandHelp


def LnBotDecorator(help_message=False, help_exemple=False, hidden=False):
    """Main décoratr for LNBot.
    Allow to easily log commands and add the commands in the help function"""

    def decorator(func):
        # This is called when a discord command is defined
        # Add function informations to generate the help function dynamically
        if not hidden:
            lib.dict_of_help_command[func.__name__] = CommandHelp.CommandHelp(
                func, help_message, help_exemple
            )

        @functools.wraps(func)
        async def wrapper(ctx, *args, **kwargs):

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator
