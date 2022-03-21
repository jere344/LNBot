from bs4 import BeautifulSoup, NavigableString
import cloudscraper

import requests
import re

import json
import os
import epubgenerator


def Search(novel):
    headers = {
        "User-Agent": "Mozilla",
        "LNRequestVerifyToken": "CfDJ8MVM-CSaaEdCppBBbxyBpd00ZSIZbqOnci8HzkzAnmePwLiORFaKaw2UD1yTM89IIh3vi3v3euUMI8hryEqd6iJoMth9JJf_mFuyhmnGhsp8hFTn1qfezXnGsbD5-xn39Lw02gLuOdr7s03VyOpYsg8",
        "Cookie": "lncoreantifrg=CfDJ8MVM-CSaaEdCppBBbxyBpd2kJ0C5BfUpfmlq8yZI0x3H5EK5j__c1ph1E6Q8RwU3Mk4zqcwoMTEQeRpnA7gv3SnYAYlPX-mdT2rwbAAUg-g5MhU2_RAWQCMhVqxaGXeNjYEqmB_JdrtiFez-o85eIqc",
    }

    response = requests.post(
        "https://www.lightnovelworld.com/lnsearchlive",
        {"inputContent": novel},
        headers=headers,
    )
    soup = BeautifulSoup(json.loads(response.content)["resultview"], features="lxml")
    novels_found = []
    for li in soup.find_all("li"):
        a = li.find("a")
        novels_found.append((a["title"], a["href"][7:], "lightnovelworld"))
        # [7:] remove the /novel/

    return novels_found


async def Update(message, novel, latest_availible):
    await message.edit(
        content="Novel aldready downloaded, but an update was detected, downloading new chapters..."
    )
    download_path = f"novels/{novel}"

    with open(f"{download_path}/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.loads(file.read())

    number_of_downloaded_chapter = len(metadata["chapterlist"])
    from_page = int(number_of_downloaded_chapter / 100) + 1  # 100 chapter per page

    ch = ScrapChapterList(novel, from_page=from_page)

    downloaded = 0
    to_download = len(ch)
    for chapter_id, chapter_info in ch.items():
        downloaded += 1
        if chapter_id in metadata["chapterlist"]:
            continue

        path = f"{download_path}/chapters/{chapter_id}.txt"
        with open(path, "w", encoding="utf-8") as file:
            file.write(ScrapChapter(chapter_info))

        await message.edit(content=f"{downloaded}/{to_download} chapters downloaded")

    metadata["chapterlist"] |= ch  # Merge the two dict
    metadata["latest"] = latest_availible

    with open(f"{download_path}/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file)

    await message.edit(content=f"Chapter list updated")

    await message.edit(content=f"Generating ebook...")
    os.remove(f"{download_path}/{epubgenerator.GetEbookFileName(metadata['title'])}")
    epubgenerator.Generate(novel)


async def DownloadNovel(message, novel):
    novel_title, novel = novel
    download_path = f"novels/{novel}"

    # Check if the novel is aldready downloaded and if so if new  chapters has been posted
    latest_availible = Latest(novel)
    if os.path.isdir(download_path):
        with open(f"{download_path}/metadata.json", "r", encoding="utf-8") as file:
            latest_downloaded = json.loads(file.read())["latest"]

        if latest_availible == latest_downloaded:
            await message.edit(content="Novel aldready downloaded, sending...")
        else:
            await Update(message, novel, latest_availible)

        return

    os.mkdir(download_path)

    metadata = {}
    metadata["source"] = "lightnovelworld"
    metadata["latest"] = latest_availible
    metadata["title"] = novel_title

    metadata["summary"] = ScrapSummary(novel)
    await message.edit(content="Summary downloaded")
    metadata["url"] = Url(novel)
    chapterlist = ScrapChapterList(novel)
    metadata["chapterlist"] = chapterlist
    await message.edit(content="Chapter list downloaded")

    with open(f"{download_path}/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file)

    pic_data, pic_format = ScrapPic(novel)
    with open(f"{download_path}/cover{pic_format}", "wb") as file:
        file.write(pic_data)
    await message.edit(content="Cover downloaded")

    await message.edit(content="Metadata downloaded")

    os.mkdir(f"{download_path}/chapters")
    number_of_chapter = len(chapterlist)

    for chapter_id, chapter_info in chapterlist.items():
        path = f"{download_path}/chapters/{chapter_id}.txt"
        with open(path, "w", encoding="utf-8") as file:
            file.write(ScrapChapter(chapter_info))

        await message.edit(
            content=f"{chapter_id}/{number_of_chapter} chapters downloaded"
        )

    await message.edit(content=f"downloaded, generating ebook")
    epubgenerator.Generate(novel)


def Latest(novel: str, proxies={}):
    url = "https://www.lightnovelworld.com/novel/" + novel
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )

    source = scraper.get(url, proxies=proxies).text
    return BeautifulSoup(source, "lxml").find("p", class_="latest text1row").text


def ScrapPic(novel: str, proxies={}) -> tuple:
    """return (picture_data, format of the picture)"""

    url = "https://www.lightnovelworld.com/novel/" + novel
    # Cloudscraper avoid lightnovelworld cloudflare protection
    # Equivalent to request
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )
    source = scraper.get(url, proxies=proxies).text
    # find the url of the cover in website : in a <div class="fixed-img"> find the "data-src" of a <img>
    url_pic = (
        BeautifulSoup(source, "lxml")
        .find("div", class_="fixed-img")
        .find("img")["data-src"]
    )

    # Download the cover
    pic_data = scraper.get(url_pic, proxies=proxies)
    pic_data = pic_data.content

    # The picture and the format
    # The last 4 character of the url are the format : .jpg, .png ... Could use split() if some other format are use but never saw them in lightnovelworld
    return pic_data, url_pic[-4:]


def ScrapChapter(info_chapter: str, proxies={}) -> str:
    """return the text of the chapter cleaned. Must have a title announced by a '# '"""
    url = info_chapter[2]
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )
    source = scraper.get(url, proxies=proxies).text
    soup = BeautifulSoup(source, "lxml").find("div", id="chapter-container")

    for br in soup.find_all("br"):
        br.replace_with("\n" + br.text)
    for hr in soup.find_all("hr"):
        hr.replace_with("\n\n\n\n" + hr.text)
    for h3 in soup.find_all("</h3>"):
        h3.replace_with("\n\n")

    text = "\n\n".join(
        [
            paragraph_text
            for paragraph_text in [
                paragraph.text
                for paragraph in soup
                if not isinstance(paragraph, NavigableString)
            ]
            if not "lightno" in paragraph_text
        ]
    )

    text = re.sub("Posted on \w* \d{1,2}.* by .*\n", "", text)

    if "Chapter" in text[:50]:
        text = text.replace("Chapter", "# Chapter", 1)
    elif "chapter" in text[:50]:
        text = text.replace("chapter", "# chapter", 1)
    else:
        text = f"# {info_chapter[1]}\n\n{text}"

    return text


def ScrapSummary(novel: str, proxies={}) -> str:
    """return the summary"""

    url = "https://www.lightnovelworld.com/novel/" + novel
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )

    source = scraper.get(url, proxies=proxies).text
    soup = BeautifulSoup(source, "lxml").find("div", class_="content")

    br = False
    for br in soup.find_all("br"):
        br.replace_with("\n" + br.text)
        br = True

    return (
        soup.text.replace("\n", "\n\n").strip().replace("%", "%%")
        if not br
        else soup.text.strip().replace("%", "%%")
    )


def ScrapOnePageOfChapter(url, proxies={}):
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )

    source = scraper.get(url, proxies=proxies).text
    # Every chapter of the page are in <ul class="chapter-list">
    list = BeautifulSoup(source, "lxml").find("ul", class_="chapter-list")

    i = 0
    ch = {}

    # Element is one chapter
    for element in list:
        # Sometimes there is a NavigableString in the middle wich throw error
        if isinstance(element, NavigableString):
            continue

        a = element.text.split("\n\n")
        url = "https://www.lightnovelworld.com" + element.find("a")["href"]
        nmbchapter = str(int(element["data-orderno"]) - 1)

        ch[nmbchapter] = (
            a[1].replace("(lightnovelworld.com)", ""),
            a[2],
            url,
        )

        i += 1
    return i, ch


def ScrapChapterList(novel: str, from_page=1, proxies={}) -> dict:
    """return a dict of :
    "ID  : (chapter, title, url)"
    ID is for sorting, only int, begin at 1
    chapter is the official number of the chapter (can be 0, 25, 43.5 ...)
    It's better if the title can contain the true title, but if not possible just put f"Chapter {chapter}"
    url will be use to download the chapter so must point directly to it"""

    fixed_url = f"https://www.lightnovelworld.com/novel/{novel}/Chapters/page-"

    ch = {}
    page = from_page

    while True:
        url = fixed_url + str(page)
        i, ch_one_page = ScrapOnePageOfChapter(url, proxies)
        ch = ch | ch_one_page  # python 3.9 merge dict

        # If the list of chapter go to 100 it mean that the page is full and there is probably another page after
        if i == 100:
            page += 1
        else:
            # If if finish at for exemple chapter 524 there is no page 6 (page 6 = chapter 600-700)
            break

    return ch


def Url(novel):
    return "https://www.lightnovelworld.com/novel/" + novel
