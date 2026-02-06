from datetime import datetime

import requests

from url_builder.url_builder import UrlBuilder

if __name__ == "__main__":
    now: datetime = datetime.now()
    url_builder: UrlBuilder = UrlBuilder()
    url_builder._set_all_params(
        year=2026,
        month=1,
        number=2355,
    )

    try:
        while url_builder <= now:
            print(url_builder.get_url())
            url_builder.increment_number()
    except requests.exceptions.RequestException:
        print("All URLs built!")
