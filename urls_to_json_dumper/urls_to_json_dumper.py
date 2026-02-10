import json
from dataclasses import dataclass


@dataclass
class UrlsJsonDumper:
    """Class for dumping all valid URL's from UrlBuilder to a JSON file."""

    # urls is a dict in the format <newsticker number, URL>
    urls: dict[int, str|None]

    def _clean_urls(self) -> None:
        """Remove all non-existent URLs."""
        self.urls = {k: v for k, v in self.urls.items() if v is not None}

    def dump_urls(self) -> None:
        """Method to clean and dump all valid URLs to a JSON file 'urls.json'."""
        self._clean_urls()
        with open("urls.json", "w", encoding="utf-8") as json_file:
            json.dump(self.urls, json_file, ensure_ascii=False, indent=4)
