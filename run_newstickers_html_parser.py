"""
Run NewstickersHtmlParser to extract the newstickers from a URL.
This requires a stored JSON file to load the URLs from!
"""

import json
from typing import Generator

from models.newsticker.newsticker_base import NewstickerBase
from newstickers_parsers.newstickers_html_parser import NewstickersHtmlParser

JSON_FILE: str = "urls.json"


def run_newstickers_html_parser() -> Generator[NewstickerBase]:
    """Wrapper for NewstickersHtmlParser that yields the next NewstickerBase object."""

    # Read in the JSON file
    with open(JSON_FILE, "r", encoding="utf-8") as json_file:
        urls: dict[str, str] = json.load(json_file)

    # Iterate over URLs and yield the next NewstickerBase object
    for number, url in urls.items():
        newstickers_html_parser: NewstickersHtmlParser = NewstickersHtmlParser(url=url)
        for newsticker_base in newstickers_html_parser.get_next_newsticker():
            yield newsticker_base


if __name__ == "__main__":
    # ONLY for testing
    for _newsticker_base in run_newstickers_html_parser():
        print(f"Newsticker: {_newsticker_base}\n")
