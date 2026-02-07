import json
import re
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup


@dataclass
class HtmlParser:
    """Class for extracting newstickers from URLs."""

    urls: dict[int, str] = field(
        init=False
    )  # All URLs in the format <newsticker number, URL>

    def __post_init__(self) -> None:
        """Set self.urls by loading the JSON file 'urls.json'."""
        with open("urls.json", "r", encoding="utf-8") as json_file:
            self.urls = json.load(json_file)

    @staticmethod
    def _parse_url(url: str) -> list[str]:
        """Parse the URL and return the extracted newstickers."""
        newstickers: list[str] = []
        response: requests.models.Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        # Match everything between '+++'
        segments: list[str] = re.findall(r"\+\+\+.*?\+\+\+", soup.get_text())
        for segment in segments:
            if len(segment.split()) <= 3:  # Only one word can't be a newsticker
                continue
            newstickers.append(segment)

        # Output the results
        for _newsticker in newstickers:
            print(_newsticker)
        print()

        return newstickers

    def parse_urls(self) -> None:
        for number, url in self.urls.items():
            self._parse_url(url)
