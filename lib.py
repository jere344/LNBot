from discord.ext import commands
import json
import config


def save_json(location, content) -> None:
    with open(location, "w", encoding="utf-8") as file:
        json.dump(content, file)


class Client(commands.Bot):
    async def on_message(self, message):
        if message.author == self.user:
            return

        return await super().on_message(message)


bot = Client(command_prefix=config.command_prefix, help_command=None)

dict_of_help_command = {}
