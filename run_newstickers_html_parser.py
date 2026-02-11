"""
Run NewstickersHtmlParser to extract the newstickers from a URL.
This requires a stored urls.json to load the URLs from!
"""
import json

from newstickers_parsers.newstickers_html_parser import NewstickersHtmlParser


with open("urls.json", "r", encoding="utf-8") as json_file:
    urls: dict[str, str] = json.load(json_file)

# ONLY for testing
for number, url in urls.items():
    newstickers_html_parser: NewstickersHtmlParser = NewstickersHtmlParser(url=url)
    print()
    print(url)
    for newsticker in newstickers_html_parser.get_next_newsticker():
        print(newsticker)