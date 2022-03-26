if __name__ == "__main__":

    with open("TOKEN") as file:
        TOKEN = file.read()
        if not TOKEN:
            import sys

            print(
                "\n\n\t\t\t/!\  You need paste your bot token in the TOKEN file. More info on https://www.writebots.com/discord-bot-token/\n"
            )

            sys.exit()

    import os

    if not os.path.isdir("novels"):
        os.mkdir("novels")

    import lib
    import commands  # do not remove

    lib.bot.run(TOKEN)
