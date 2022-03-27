from bs4 import BeautifulSoup, NavigableString
import cloudscraper
import _misc_ as misc
import requests
import re

import json
import os
from messages import *
import epub

headers = {
    "Host": "www.lightnovelworld.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "utf-8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "LNRequestVerifyToken": "CfDJ8FmyhIN_ipxGu0PT0IWOxoko73KMVQ0tEP7G2sEbMDc_DpCXli3NaDRFNbHKn9HsKWaT0S8pZkqUkfzSZo2IlppeEFpZiXAv5--wyJIeo4OzB_3yz3kal11OY3j_WCBjRATaPOc4XYKqStttde5vHUM",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.lightnovelworld.com",
    "DNT": "1",
    "Alt-Used": "www.lightnovelworld.com",
    "Connection": "keep-alive",
    "Referer": "https://www.lightnovelworld.com/search",
    "Cookie": "euconsent-v2=CPVrlMSPVrlMSAKAnAENCGCsAP_AAH_AACaIIpNd_X__bX9j-_5_f_t0eY1P9_r3v-QzjhfNt-8F3L_W_L0X42E7NF36pq4KuR4Eu3LBIQNlHMHUTUmwaokVrzHsak2cpyNKJ7LEmnMZO2dYGHtPn9lDuYKY7_5___fz3j-v_t_-39T378X_3_d5_2---vCfV599jLv9____39nP___9v-_8______8EUgCTDUvIAuzLHBk2jSqFECMKwkKgFABRQDC0RWADg4KdlYBPqCFgAgFSEYEQIMQUYMAgAEEgCQiICQAsEAiAIgEAAIAUYCEABEwCCwAsDAIABQDQsQAoABAkIMjgqOUwICpFooJbKxBKCvY0wgDLPAigURkVAAiSaAFgZCQsHMcASAl4skDTFC-QAiAA.dgAACFgAAAAA; addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.7.4.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.6.14.5.20.6.5.1.3.1.11.29.4.14.4.5.3.10.6.2.9.6.6.4.5.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.142.4.8.35.7.15.1.14.3.1.8.10.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.1.6.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.8.2.15.2.5.5.1.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.2.1.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.4.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.7.4.6.1.10.5.2.6.3.2.2.4.3.2.2.7.2.13.7.12.2.1.3.3.4.5.4.3.2.2.4.1.3.1.1.1.2.9.1.6.9.1.5.2.1.7.2.8.11.1.3.1.1.2.1.3.2.6.1.5.6.1.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.2.2.1.1.4.2.1.2.1.1.1.2.2.4.2.1.2.2.2.4.1.1.1.2.1.1.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.1.5.2.1.6.5.1.1.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.2.1.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.1.4.2.3.2.1.4.1.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.1.3.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1; lncoreantifrg=CfDJ8MVM-CSaaEdCppBBbxyBpd2kJ0C5BfUpfmlq8yZI0x3H5EK5j__c1ph1E6Q8RwU3Mk4zqcwoMTEQeRpnA7gv3SnYAYlPX-mdT2rwbAAUg-g5MhU2_RAWQCMhVqxaGXeNjYEqmB_JdrtiFez-o85eIqc; googtrans=null; cf_clearance=4h.WdgNqsBeLJ8rB2PqXIiSRIa.AU9of4LxkavpnsYA-1648125284-0-150",
}


def Search(novel):

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
    await message.edit(content=UpdateDetected())
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

        await message.edit(content=ChapterDownloaded(downloaded, to_download))

    metadata["chapterlist"] |= ch  # Merge the two dict
    metadata["latest"] = latest_availible

    with open(f"{download_path}/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file)

    await message.edit(content=ChapterlistDownloaded())

    await message.edit(content=GeneratingEbook())
    os.remove(f"{download_path}/{epub.GetEbookFileName(metadata['title'])}")
    epub.Generate(novel)


async def DownloadNovel(message, novel):
    novel_title, novel = novel
    download_path = f"novels/{novel}"

    # Check if the novel is aldready downloaded and if so if new  chapters has been posted
    latest_availible = Latest(novel)
    if os.path.isdir(download_path):
        with open(f"{download_path}/metadata.json", "r", encoding="utf-8") as file:
            latest_downloaded = json.loads(file.read())["latest"]

        if latest_availible == latest_downloaded:
            await message.edit(content=AldreadyDownloaded())
        else:
            await Update(message, novel, latest_availible)

        return

    os.mkdir(download_path)

    metadata = {}
    metadata["source"] = "lightnovelworld"
    metadata["latest"] = latest_availible
    metadata["title"] = novel_title

    metadata["summary"] = ScrapSummary(novel)
    await message.edit(content=SummaryDownloaded())
    metadata["url"] = Url(novel)
    chapterlist = ScrapChapterList(novel)
    metadata["chapterlist"] = chapterlist
    await message.edit(content=ChapterlistDownloaded())

    with open(f"{download_path}/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file)

    pic_data, pic_format = ScrapPic(novel)
    with open(f"{download_path}/cover{pic_format}", "wb") as file:
        file.write(pic_data)
    await message.edit(content=CoverDownloaded())

    await message.edit(content=MetadataDownloaded())

    os.mkdir(f"{download_path}/chapters")
    number_of_chapter = len(chapterlist)

    for chapter_id, chapter_info in chapterlist.items():
        path = f"{download_path}/chapters/{chapter_id}.txt"
        with open(path, "w", encoding="utf-8") as file:
            file.write(ScrapChapter(chapter_info))

        await message.edit(content=ChapterDownloaded(chapter_id, number_of_chapter))

    await message.edit(content=GeneratingEbook())
    epub.Generate(novel)


def Latest(novel: str, proxies={}):
    url = "https://www.lightnovelworld.com/novel/" + novel
    source = requests.get(url, headers=headers).text
    return BeautifulSoup(source, "lxml").find("p", class_="latest text1row").text


def ScrapPic(novel: str, proxies={}) -> tuple:
    """return (picture_data, format of the picture)"""

    url = "https://www.lightnovelworld.com/novel/" + novel
    # Cloudscraper avoid lightnovelworld cloudflare protection
    # Equivalent to request
    source = requests.get(url, headers=headers).text
    # find the url of the cover in website : in a <div class="fixed-img"> find the "data-src" of a <img>
    url_pic = (
        BeautifulSoup(source, "lxml")
        .find("div", class_="fixed-img")
        .find("img")["data-src"]
    )

    # Download the cover
    pic_data = requests.get(url_pic, proxies=proxies, headers=headers)
    pic_data = pic_data.content

    # The picture and the format
    # The last 4 character of the url are the format : .jpg, .png ... Could use split() if some other format are use but never saw them in lightnovelworld
    return pic_data, url_pic[-4:]


def ScrapChapter(info_chapter: str, proxies={}) -> str:
    """return the text of the chapter cleaned. Must have a title announced by a '# '"""
    url = info_chapter[2]
    source = requests.get(url, headers=headers).text
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
    source = requests.get(url, headers=headers).text
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

    source = scraper.get(url, proxies=proxies, headers=headers).text
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
