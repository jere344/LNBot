from ebooklib import epub
import os
import os.path
import json
from lib import Novel


def Generate(file_path, novel: Novel):
    novel_path = f"novels/{novel.source}/{novel.real_name}"
    with open(f"{novel_path}/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.loads(file.read())

    book = epub.EpubBook()
    # set metadata
    book.set_identifier("N/A")
    book.set_title(metadata["title"])
    book.set_language("en")
    book.add_author("N/A")

    # necessary since we don't know the extension
    for file in os.listdir(novel_path):
        if file[:5] == "cover":
            break
    pic_path = f"{novel_path}/{file}"

    book.set_cover(file, open(pic_path, "rb").read())
    spine = []

    for file in sorted(
        os.listdir(f"{novel_path}/chapters"), key=lambda x: int(x.split(".")[0])
    ):
        with open(f"{novel_path}/chapters/{file}", "r", encoding="utf-8") as file:
            chapter_text = file.read().split("\n\n")

        title_line = 0
        for paragraph in chapter_text:
            if "# " in paragraph:
                break
            title_line += 1

        before_title = "<br><br>".join(chapter_text[:title_line])
        title = chapter_text[title_line].replace("# ", "")
        after_title = "<br><br>".join(chapter_text[title_line + 1 :])

        chapter = epub.EpubHtml(
            title=title.replace("# ", "").strip(),
            file_name=f"{file}.xhtml",
            lang="en",
        )

        chapter.content = (
            f"""<p>
                {before_title}
            </p>
            <h1>
                {title}
            </h1>
            <p>
                {after_title}
            </p>""".replace(
                "<<", "&lt;&lt;"
            )
            .replace(">>", "&gt;&gt;")
            .replace("\n", "<br>")
            .replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        )

        book.add_item(chapter)
        spine.append(chapter)

    style = open("epubstyle.css", encoding="utf-8").read()
    css = epub.EpubItem(
        uid="stylesheet",
        file_name="stylesheet.css",
        media_type="text/css",
        content=style,
    )

    book.toc = tuple(spine)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.add_item(css)
    book.spine = spine
    epub.write_epub(
        file_path,
        book,
        {"epub3_pages": False},
    )
