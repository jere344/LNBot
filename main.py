import os

if __name__ == "__main__":
    if not os.path.isfile("TOKEN"):
        open("TOKEN", "w").close()
    if not os.path.isdir("novels"):
        os.mkdir("novels")

    with open("TOKEN") as file:
        TOKEN = file.read()
        if not TOKEN:
            import sys

            print(
                "\n\n\t\t\t/!\  You need paste your bot token in the TOKEN file. More info on https://www.writebots.com/discord-bot-token/\n"
            )

            sys.exit()

    import lib
    import commands  # do not remove

    lib.bot.run(TOKEN)
