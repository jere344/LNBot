import requests
from bs4 import BeautifulSoup, NavigableString
import os
import json
import ebookgenerators
from messages import *

lang = ["EN"]
source = "https://www.readlightnovel.me/"

header = {"X-Requested-With": "XMLHttpRequest"}


def Search(novel):
    response = requests.post(
        "https://www.readlightnovel.me/search/autocomplete",
        {"q": novel},
        headers=header,
    )

    soup = BeautifulSoup(response.text, features="lxml")
    novel_founds = {}
    novel_founds = [
        (
            li.find("span", class_="title").text,
            li.find("a")["href"].split("/")[-1],
            "readlightnovel",
            "EN",
        )
        for li in soup.findAll("li")
    ]
    return novel_founds


async def update(message, soup, metadata, novel, latest_release):
    new_chapterlist = chapterlist(soup).items()
    nmb_chapter = len(new_chapterlist)

    for i, (nmb, chapter) in enumerate(new_chapterlist):
        if str(nmb) in metadata["chapterlist"]:
            continue
        await message.edit(content=ChapterDownloaded(i, nmb_chapter))
        download_chapter(novel, nmb, chapter)

    metadata["latest"] = latest_release

    with open(
        f"novels/readlightnovel - {novel}/metadata.json", "w", encoding="utf-8"
    ) as file:
        json.dump(metadata, file)

    ebookgenerators.DeleteEbook(novel, metadata["title"], "readlightnovel")


async def DownloadNovel(message, title, novel):
    download_path = f"novels/readlightnovel - {novel}"

    url = f"https://www.readlightnovel.me/{novel}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    latest_release = latest(soup)

    if os.path.isdir(download_path):
        await message.edit(content=AldreadyDownloaded())

        with open(f"{download_path}/metadata.json", "r", encoding="utf-8") as file:
            metadata = json.loads(file.read())

        if latest_release != metadata["latest"]:
            await message.edit(content=UpdateDetected())
            update(message, soup, metadata, novel, latest_release)

        return

    os.mkdir(download_path)

    metadata = {}

    metadata["source"] = "readlightnovel"
    metadata["language"] = "EN"
    metadata["title"] = title
    metadata["url"] = url
    metadata["summary"] = summary(soup)
    await message.edit(content=SummaryDownloaded())
    metadata["latest"] = latest(soup)

    metadata["chapterlist"] = chapterlist(soup)
    await message.edit(content=ChapterlistDownloaded())
    cover(soup, novel)
    await message.edit(content=CoverDownloaded())
    await message.edit(content=MetadataDownloaded())

    os.mkdir(f"{download_path}/chapters")
    number_of_chapter = len(metadata["chapterlist"])
    for i, (nmb, chapter) in enumerate(metadata["chapterlist"].items()):
        download_chapter(novel, nmb, chapter)
        await message.edit(content=ChapterDownloaded(i, number_of_chapter))

    with open(f"{download_path}/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file)


def latest(soup):
    return (
        soup.find("div", class_="novel-detail-item", style="display:flex;")
        .find("a")
        .text
    )


def chapterlist(soup):
    """ID : Nmb, Title, Url"""
    list_of_chapters = {}

    i = 0
    for ul in soup.find_all("ul", class_="chapter-chs"):
        for a in ul.find_all("a"):
            list_of_chapters[i] = (i, a.text, a["href"])
            i += 1

    return list_of_chapters


def summary(soup):
    return "\n\n".join(
        [
            span.text
            for span in soup.find("div", class_="novel-right")
            .find("div", "novel-detail-body")
            .find_all("span")
        ]
    )


def cover(soup, novel):
    cover_url = soup.find("div", class_="novel-cover").find("img")["src"]
    cover_data = requests.get(cover_url, allow_redirects=True)
    cover_format = cover_url.split(".")[-1]
    with open(f"novels/readlightnovel - {novel}/cover.{cover_format}", "wb") as file:
        file.write(cover_data.content)


def is_ads(tag):
    if tag.has_attr("class"):
        if tag["class"] == ["hid"]:
            return True
    return False


def download_chapter(novel, nmb, chapter_info):
    _, title, url = chapter_info

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    text = "\n\n".join(
        [
            e
            for e in [
                p.text.strip()
                for p in soup.find("div", id="chapterhidden", class_="hidden")
                if not isinstance(p, NavigableString) and not is_ads(p)
            ]
            if e
        ]
    )  # enjoy

    if "Chapter" in text[:50]:
        text = text.replace("Chapter", "# Chapter", 1)
    elif "chapter" in text[:50]:
        text = text.replace("chapter", "# chapter", 1)
    else:
        text = f"# {title}\n\n{text}"

    with open(
        f"novels/readlightnovel - {novel}/chapters/{nmb}.txt", "w", encoding="utf-8"
    ) as file:
        file.write(text)
