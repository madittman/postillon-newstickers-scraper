"""
Run NewstickersImageParser to extract the newsticker on the newsticker's image from a URL.
This requires a stored JSON file to load the URLs from!
"""

import json

from models.newsticker import Newsticker
from newstickers_parsers.newstickers_image_parser import NewstickersImageParser

JSON_FILE: str = "urls.json"
with open(JSON_FILE, "r", encoding="utf-8") as json_file:
    urls: dict[str, str] = json.load(json_file)

# ONLY for testing
for number, url in urls.items():
    newstickers_image_parser: NewstickersImageParser = NewstickersImageParser(url=url)
    newsticker: Newsticker | None = newstickers_image_parser.get_newsticker()
    print(f"URL: {url}")
    print(f"Newsticker: {newsticker}")
    print()
