import os
import sys
import time
from ebooklib import epub

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from file_utils import read_file_data, clear_file_cache  # noqa: E402


def test_read_file_data_caching(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("first")
    first = read_file_data(str(file_path))
    assert first == "first"

    # Read again without modification should use cache
    second = read_file_data(str(file_path))
    assert second == "first"

    time.sleep(0.01)
    file_path.write_text("second")
    third = read_file_data(str(file_path))
    assert third == "second"

    clear_file_cache()


def _create_epub(path, text):
    book = epub.EpubBook()
    book.set_identifier("id")
    book.set_title("Test")
    book.set_language("en")
    chapter = epub.EpubHtml(title="Intro", file_name="intro.xhtml", lang="en")
    chapter.content = f"<p>{text}</p>"
    book.add_item(chapter)
    book.toc = (epub.Link("intro.xhtml", "Intro", "intro"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chapter]
    epub.write_epub(path, book)


def test_read_epub_file(tmp_path):
    epub_path = tmp_path / "book.epub"
    _create_epub(str(epub_path), "hello")
    content = read_file_data(str(epub_path))
    assert "hello" in content
