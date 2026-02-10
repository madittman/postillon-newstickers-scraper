import json
from dataclasses import dataclass


@dataclass
class UrlsToJsonDumper:
    """Class for dumping all valid URL's from UrlBuilder to a JSON file."""

    # urls is a dict in the format <newsticker number, URL>
    urls: dict[int, str|None]

    def _remove_none_values(self) -> None:
        """Remove all non-existent URLs."""
        self.urls = {k: v for k, v in self.urls.items() if v is not None}

    def dump_urls(self, filename: str) -> None:
        """Method to dump all URLs to a JSON file."""
        self._remove_none_values()
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(self.urls, json_file, ensure_ascii=False, indent=4)
