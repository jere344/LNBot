import os
import messages

if __name__ == "__main__":
    if not os.path.isfile("TOKEN"):
        open("TOKEN", "w").close()
    if not os.path.isdir("novels"):
        os.mkdir("novels")

    with open("TOKEN") as file:
        TOKEN = file.read()
        if not TOKEN:
            import sys

            print(messages.BotToken())

            sys.exit()

    import lib
    import commands  # do not remove

    lib.bot.run(TOKEN)
