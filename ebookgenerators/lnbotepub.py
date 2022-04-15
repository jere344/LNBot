from ebooklib import epub
import json
import lib


def Generate(novel_real_name, file_path: None, source):

    novel_path = lib.novel_path / f"{source} - {novel_real_name}"
    with open(novel_path / "metadata.json", "r", encoding="utf-8") as file:
        metadata = json.loads(file.read())

    book = epub.EpubBook()
    # set metadata
    book.set_identifier("N/A")
    book.set_title(metadata["title"])
    book.set_language("en")
    book.add_author("N/A")

    # necessary since we don't know the extension
    for file in novel_path.iterdir():
        if file.stem == "cover":
            break

    book.set_cover(str(file), open(file, "rb").read())
    spine = []

    # iterate alphanumerically
    for file in sorted(
        [f for f in (novel_path / "chapters").iterdir()],
        key=lambda x: int(x.stem),
    ):
        with open(novel_path / "chapters" / file.name, "r", encoding="utf-8") as file:
            chapter_text = file.read().split("\n\n")

        title_line = 0
        for paragraph in chapter_text:
            if "# " in paragraph:
                break
            title_line += 1

        before_title = "<br><br>".join(chapter_text[:title_line]).replace("\n", "<br>")
        title = chapter_text[title_line].replace("# ", "")
        after_title = "<br><br>".join(chapter_text[title_line + 1 :]).replace(
            "\n", "<br>"
        )

        chapter = epub.EpubHtml(
            title=title.replace("# ", "").strip(),
            file_name=f"{file}.xhtml",
            lang="en",
        )

        chapter.content = f"""<p>
                {before_title}
            </p>
            <h1>
                {title}
            </h1>
            <p>
                {after_title}
            </p>"""

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

    if not file_path:
        file_path = lib.novel_path / f"{source} - {novel_real_name}.epub"
    epub.write_epub(
        file_path,
        book,
        {"epub3_pages": False},
    )
