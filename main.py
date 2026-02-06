from datetime import datetime
from typing import Union

import requests

from url_builder.url_builder import UrlBuilder
from url_json_dumper.url_json_dumper import UrlJsonDumper

if __name__ == "__main__":
    now: datetime = datetime.now()
    url_builder: UrlBuilder = UrlBuilder()
    url_builder.set_all_params(
        year=2017,
        month=9,
        number=1103,
    )

    # All URLs in the format <newsticker number, URL>
    urls: dict[int, Union[str, None]] = {}
    try:
        while url_builder <= now:
            newsticker_number: int = url_builder.get_number()
            urls[newsticker_number] = url_builder.get_url()
            print(f"Built URL {url_builder.get_url()}")
            url_builder.increment_number()  # get the next newsticker
    except (
        requests.exceptions.RequestException
    ):  # Raise exception when there is no newer newsticker
        print("All URLs built!")

    url_json_dumper: UrlJsonDumper = UrlJsonDumper(urls=urls)
    url_json_dumper.dump_urls()
    print("All URLs dumped to JSON!")
