import lib
import commands  # do not remove


if __name__ == "__main__":
    with open("TOKEN") as file:
        TOKEN = file.read()

    lib.bot.run(TOKEN)
