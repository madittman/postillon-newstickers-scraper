import json
from dataclasses import dataclass
from typing import Union


@dataclass
class UrlJsonDumper:
    """Class for dumping all valid URL's from UrlBuilder to a JSON file."""

    # All URLs in the format <newsticker number, URL>
    urls: dict[int, Union[str, None]]

    def _clean_urls(self) -> None:
        # Somehow newsticker 1796 has number 1795 in URL and newsticker 1795 doesn't exist
        if 1795 in self.urls:
            self.urls[1796] = self.urls[1795]
            self.urls[1795] = None

        # Remove all non-existent URLs
        self.urls = {k: v for k, v in self.urls.items() if v is not None}

    def dump_urls(self) -> None:
        """Method to clean and dump all valid URLs to a JSON file 'urls.json'."""
        self._clean_urls()
        with open("urls.json", "w", encoding="utf-8") as json_file:
            json.dump(self.urls, json_file, ensure_ascii=False, indent=4)
