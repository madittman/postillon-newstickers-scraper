"""
Build all URLs with UrlBuilder and dump to JSON file with UrlsToJsonDumper.
"""

from datetime import datetime

import requests

from url_builder.url_builder import UrlBuilder
from urls_to_json_dumper.urls_to_json_dumper import UrlsToJsonDumper

JSON_FILE: str = "urls.json"
NOW: datetime = datetime.now()
url_builder: UrlBuilder = UrlBuilder()
url_builder.set_all_params(  # Adjust parameters to set where to start from
    year=2026,
    month=2,
    number=2358,
)

# urls is a dict in the format <newsticker number, URL>
urls: dict[int, str | None] = {}

# Build all URLs
try:
    while url_builder <= NOW:
        newsticker_number: int = url_builder.get_number()
        urls[newsticker_number] = url_builder.get_url()
        print(f"Built URL {url_builder.get_url()}")
        url_builder.increment_number()  # get the next newsticker
except (
    requests.exceptions.RequestException
):  # Raise exception when there is no newer newsticker
    print("All URLs built!")

# Dump URLs to JSON file 'urls.json'
url_json_dumper: UrlsToJsonDumper = UrlsToJsonDumper(urls=urls)
url_json_dumper.dump_urls(JSON_FILE)
print(f"All URLs dumped to JSON file '{JSON_FILE}'!")
