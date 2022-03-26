from typing import Callable
import inspect


class CommandHelp:
    """Try to dynamicaly generate a help menu for the command with function arguments.
    Allow overwriting automaticaly generated commands by passing argument to the main decorator"""

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
