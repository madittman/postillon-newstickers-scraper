from datetime import datetime
from typing import Union

import requests

from url_builder.url_builder import UrlBuilder
from url_json_dumper.url_json_dumper import UrlJsonDumper

if __name__ == "__main__":
    now: datetime = datetime.now()
    url_builder: UrlBuilder = UrlBuilder()
    url_builder._set_all_params(  # ONLY for testing
        year=2021,
        month=12,
        number=1742,
    )

    # All URLs in the format <newsticker number, URL>
    urls: dict[int, Union[str, None]] = {}
    try:
        now = datetime(2022, 5, 1)  # ONLY for testing
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
