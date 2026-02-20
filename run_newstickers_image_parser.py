"""
Run NewstickersImageParser to extract the newsticker on the newsticker's image from a URL.
This requires a stored JSON file to load the URLs from!
"""

import json
from typing import Generator

from models.newsticker.newsticker_base import NewstickerBase
from newstickers_parsers.newstickers_image_parser import NewstickersImageParser

JSON_FILE: str = "urls.json"


def run_newstickers_image_parser() -> Generator[NewstickerBase | None]:
    """Wrapper for NewstickersImageParser that yields the next NewstickerBase object."""

    # Read in the JSON file
    with open(JSON_FILE, "r", encoding="utf-8") as json_file:
        urls: dict[str, str] = json.load(json_file)

    # Iterate over URLs and yield the next NewstickerBase object
    for number, url in urls.items():
        newstickers_image_parser: NewstickersImageParser = NewstickersImageParser(
            url=url
        )
        yield newstickers_image_parser.get_newsticker()


if __name__ == "__main__":
    # ONLY for testing
    for _newsticker_base in run_newstickers_image_parser():
        print(f"Newsticker: {_newsticker_base}\n")
