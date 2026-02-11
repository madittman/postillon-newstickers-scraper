import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Generator

import requests
from bs4 import BeautifulSoup, Tag

from exceptions.exceptions import (NoNewstickerFoundError,
                                   NoPostBodyDivFoundError,
                                   NoValidDateFoundError,
                                   NoValidTitleFoundError)
from models.newsticker import Newsticker
from models.newstickers_website import NewstickersWebsite


@dataclass
class NewstickersHtmlParser:
    """Class for extracting and getting Newsticker objects from a URL."""

    url: str
    soup: BeautifulSoup = field(
        init=False
    )

    def __post_init__(self) -> None:
        """Call URL and set BeautifulSoup object."""
        response: requests.models.Response = requests.get(self.url)
        self.soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        if not self.soup.find("div", class_="post-body"):
            raise NoPostBodyDivFoundError(f"Could not find the 'post-body' div from {self.url}")

    def _get_title_string(self) -> str:
        """Return the title of the newstickers website as string."""
        title: Tag | None = self.soup.title
        if not title:
            raise NoValidTitleFoundError(f"Title '{title}' could not be parsed")
        title_string: str = str(title.string)

        # Raise error if title doesn't match the format 'Newsticker (<number>) .*'
        pattern: str = r"^Newsticker\s\(\d+\).*"
        if not re.fullmatch(pattern, title_string):
            raise NoValidTitleFoundError(f"Title '{title}' does not match format 'Newsticker (<number>) .*")

        return title_string

    @staticmethod
    def _get_number_from_title_string(title_string) -> int:
        """Return the newsticker's number from the title string as int."""

        # The inner (\d+) captures just the number into group 1
        match: re.Match[str] | None = re.search(r'\((\d+)\)', title_string)
        if match is None:
            raise NoValidTitleFoundError(f"Title '{title_string}' could not be parsed")
        return int(match.group(1))

    def _get_date(self) -> date:
        """Return the date of the newstickers website as date object."""
        time: Tag | None = self.soup.time
        if not time:
            raise NoValidDateFoundError(f"Time '{time}' could not be parsed")
        date_string: str = str(time.string)

        # Raise error when date doesn't match the format 'day.month.year'
        pattern = r"^[\d]{1,2}\.[\d]{1,2}\.[\d]{1,2}$"
        if not re.fullmatch(pattern, date_string):
            raise NoValidDateFoundError(f"Date '{date_string}' does not match format 'day.month.year'")

        # Parse the date string
        return datetime.strptime(date_string, "%d.%m.%y").date()

    def _get_newstickers_website(self) -> NewstickersWebsite:
        """Return NewstickersWebsite object."""
        title_string: str = self._get_title_string()

        # Extract the newsticker's number from title
        number: int = self._get_number_from_title_string(title_string)

        date_obj: date = self._get_date()

        return NewstickersWebsite(
            number=number,
            title=title_string,
            date=date_obj,
            url=self.url,
        )

    def _extract_newsticker_strings(self) -> list[str]:
        """Return the extracted newstickers from self.soup as a list of strings."""

        # Match everything between '+++'
        newsticker_strings: list[str] = re.findall(r"\+\+\+.*?\+\+\+", self.soup.get_text())

        # Only one word can't be a newsticker
        newsticker_strings = [nt_str for nt_str in newsticker_strings if len(nt_str.split()) > 3]

        # Raise error if no newsticker was found
        if len(newsticker_strings) == 0:
            raise NoNewstickerFoundError(f"No newsticker found on URL {self.url}")

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