import messages
import lib

if __name__ == "__main__":
    if not lib.main_path / "TOKEN":
        open(lib.main_path / "TOKEN", "w").close()
    if not lib.novel_path.exists():
        lib.novel_path.mkdir()

    with open("TOKEN") as file:
        TOKEN = file.read()
        if not TOKEN:
            import sys

            print(messages.BotToken())

            sys.exit()

    import lib
    import commands  # do not remove

    lib.bot.run(TOKEN)
