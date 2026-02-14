import re
import sys
import time
from abc import ABC
from dataclasses import dataclass, field
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup, Tag

from exceptions.exceptions import (
    NoPostBodyDivFoundError,
    NoValidDateFoundError,
    NoValidTitleFoundError,
)
from models.newstickers_website import NewstickersWebsite


@dataclass
class NewstickersParser(ABC):
    """
    Abstract base class for extracting newstickers from different sources.
    """

    url: str
    soup: BeautifulSoup = field(init=False)

    def __post_init__(self) -> None:
        """Call URL and set BeautifulSoup object."""
        back_off: int = 5
        response: requests.models.Response = requests.get(self.url)

        # Sleep for an increasing amount of seconds if there have been too many requests for the URL
        while response.status_code == 429:
            response = requests.get(self.url)
            print(
                f"> Too many requests for URL '{self.url}'\n"
                + f"Sleeping for {back_off} seconds...\n",
                file=sys.stderr,
            )
            time.sleep(back_off)
            back_off *= 2

        # Raise error for 4xx or 5xx responses
        response.raise_for_status()

        self.soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        if not self.soup.find("div", class_="post-body"):
            raise NoPostBodyDivFoundError(
                f"Could not find the 'post-body' <div> tag from URL '{self.url}'"
            )

    def _get_title_string(self) -> str:
        """Return the title of the newstickers website as string."""
        title_tag: Tag | None = self.soup.title
        if not title_tag:
            raise NoValidTitleFoundError(
                f"Title from URL '{self.url}' could not be parsed"
            )
        title_string: str = str(title_tag.string)

        # Raise error if title doesn't match the format 'word1-word2-...-wordN (<number>).*'
        pattern: str = r"^[\w-]+ \(\d+\).*"
        if not re.fullmatch(pattern, title_string):
            raise NoValidTitleFoundError(
                f"Title '{title_string}' from URL '{self.url}' does not match format 'Newsticker (<number>) .*"
            )

        return title_string

    def _get_number_from_title_string(self, title_string: str) -> int:
        """Return the newsticker's number from the title string as int."""

        # The inner (\d+) captures just the number into group 1
        match: re.Match[str] | None = re.search(r"\((\d+)\)", title_string)
        if not match:
            raise NoValidTitleFoundError(
                f"Title '{title_string}' from URL '{self.url}' could not be parsed"
            )
        return int(match.group(1))

    def _get_date(self) -> date:
        """Return the date of the newstickers website as date object."""
        time_tag: Tag | None = self.soup.time
        if not time_tag:
            raise NoValidDateFoundError(
                f"Time from URL '{self.url}' could not be parsed"
            )
        date_string: str = str(time_tag.string)

        # Raise error when date doesn't match the format 'day.month.year'
        pattern = r"^[\d]{1,2}\.[\d]{1,2}\.[\d]{1,2}$"
        if not re.fullmatch(pattern, date_string):
            raise NoValidDateFoundError(
                f"Date '{date_string}' from URL '{self.url}' does not match format 'day.month.year'"
            )

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
