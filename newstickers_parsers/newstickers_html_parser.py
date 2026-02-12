import re
from dataclasses import dataclass
from typing import Generator

from bs4 import Tag

from exceptions.exceptions import NoNewstickerFoundError
from models.newsticker import Newsticker
from models.newstickers_website import NewstickersWebsite
from newstickers_parsers.newstickers_parser import NewstickersParser


@dataclass
class NewstickersHtmlParser(NewstickersParser):
    """Class for extracting and getting Newsticker objects from a URL."""

    def _extract_newsticker_strings(self) -> list[str]:
        """Return the extracted newstickers from self.soup as a list of strings."""

        # Match everything between '+++'
        newsticker_strings: list[str] = re.findall(
            r"\+\+\+.*?\+\+\+", self.soup.get_text()
        )

        # Only one word can't be a newsticker
        newsticker_strings = [
            nt_str for nt_str in newsticker_strings if len(nt_str.split()) > 3
        ]

        # Raise error if no newsticker was found
        if len(newsticker_strings) == 0:
            raise NoNewstickerFoundError(f"No newsticker found on URL '{self.url}'")

        # Remove the newsticker that was found from the 'ticker-content' div
        # as it doesn't belong to the newsticker's website.
        ticker_content_div: Tag | None = self.soup.find("div", id="ticker-content")
        if ticker_content_div:
            ticker_content_newsticker: str = str(ticker_content_div.string)
            if ticker_content_newsticker in newsticker_strings:
                newsticker_strings.remove(ticker_content_newsticker)

        return newsticker_strings

    def get_next_newsticker(self) -> Generator[Newsticker]:
        """Yield the next Newsticker object."""
        newstickers_website: NewstickersWebsite = self._get_newstickers_website()
        newstickers_strings: list[str] = self._extract_newsticker_strings()
        for newsticker_string in newstickers_strings:
            newsticker: Newsticker = Newsticker(
                text=newsticker_string,
                newstickers_website=newstickers_website,
                extracted_from_image=False,
            )
            yield newsticker
