[THIS REPO IS OUTDATED] 

Check out [lightnovel crawler](https://github.com/dipu-bd/lightnovel-crawler) for a discord bot instead, or my website using the same technology : http://lncrawler.monster/

---

It was made in a few days more as a learning project than an actual usable program. 
I do not guarantee the stability or security of this program.
It is still usable but I advise you to use https://github.com/dipu-bd/lightnovel-crawler/ instead.


# LNBot

> A Discord bot to easily download ebook of your favorites web and light novel.

> Scrap novels from aggregators and let you download them easily through a discord bot.



---

## Table of Contents

- [Try it now](#try-it-now)
- [Use](#user)
- [Installation](#installation)
- [Requirements](#Requirements)
- [Features](#features)

---

## Features

- Download novel from lightnovelworld and readlightnovel
- Multi-language support for the bot : currently French and English are human-translated and Spanish, Deutsch and Italian are translated by github copilot
- Totally open sources
- Add your own commands simply by creating a .py file in the commands folder following "ping.py"as an exemple
- Upload file using discord or self hosted with flask server (google drive coming soon)


## Try it now

You can try the bot right now using [this invitation](https://discord.com/oauth2/authorize?client_id=949308611924987914&scope=bot&permissions=35904) and start downloading novels. But this is hosted on my raspberrypi on my crappy adsl connection, so don't expect good performance or stability.



## Use

```
.download <*novel> [*-options]
.delete <password> <*novel>
.help <?command>
```

Exemple :

![Imgur Image](https://i.imgur.com/OowN1zf.png)

Use .help to show non-hidden commands
Use @LnBotDecorator(hidden=True) to hide command from .help


## Installation

- Clone the repo
- Install [Requirements](#Requirements)
- Create a "TOKEN" file next to main.py and paste your discord bot token here
- Choose language, command prefix ... in config.py or keep defaults
- Start main.py



## Requirements

- [A recent version of python](https://www.python.org/downloads/)
- [discord.py](https://pypi.org/project/discord.py/)
- [EbookLib](https://pypi.org/project/EbookLib/)

```
pip install discord.py
pip install EbookLib
```
