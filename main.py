import lib
import commands  # do not remove

with open("TOKEN") as file:
    TOKEN = file.read()


if __name__ == "__main__":
    lib.bot.run(TOKEN)
