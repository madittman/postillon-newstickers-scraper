import re
from dataclasses import dataclass
from typing import Generator

from bs4 import Tag

from exceptions.exceptions import NoNewstickerFoundError
from models.newsticker.newsticker_base import NewstickerBase
from models.newstickers_website.newstickers_website_base import NewstickersWebsiteBase
from newstickers_parsers.newstickers_parser_base import NewstickersParserBase


@dataclass
class NewstickersHtmlParser(NewstickersParserBase):
    """Class for extracting and getting NewstickerBase objects from a URL."""

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

        # Remove the newsticker that was found from the 'ticker-content' <div> tag
        # as it doesn't belong to the newsticker's website.
        ticker_content_div_tag: Tag | None = self.soup.find("div", id="ticker-content")
        if ticker_content_div_tag:
            ticker_content_newsticker: str = str(ticker_content_div_tag.string)
            if ticker_content_newsticker in newsticker_strings:
                newsticker_strings.remove(ticker_content_newsticker)

        return newsticker_strings

    def get_next_newsticker(self) -> Generator[NewstickerBase]:
        """Yield the next NewstickerBase object."""
        newstickers_website: NewstickersWebsiteBase = self._get_newstickers_website()
        newstickers_strings: list[str] = self._extract_newsticker_strings()
        for newsticker_string in newstickers_strings:
            newsticker: NewstickerBase = NewstickerBase(
                text=newsticker_string,
                newstickers_website=newstickers_website,
                extracted_from_image=False,
            )
            yield newsticker
