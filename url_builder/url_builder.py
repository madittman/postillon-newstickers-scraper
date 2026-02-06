from dataclasses import dataclass, field
from datetime import datetime
from typing import Union

import requests
from typing_extensions import Self

from url_builder.special_urls import SPECIAL_URLS


@dataclass
class UrlBuilder:
    """Class for generating a valid URL for a Postillon's newstickers site."""

    # Start with URL of the very first newsticker there was
    url_parts: list[str] = field(
        default_factory=lambda: [
            "https://",
            "www.der-postillon.com/",
            "2009",  # year (index 2)
            "/",
            "02",  # month (index 4)
            "/",
            "newsticker-",
            "1",  # number (index 7)
            ".html",
        ]
    )

    def __le__(self, obj: object) -> bool:
        """Compare datetime to URL's year and month."""
        if not isinstance(obj, datetime):
            return False
        if self._get_year() > obj.year:
            return False
        elif self._get_year() == obj.year:
            if self._get_month() > obj.month:
                return False
        return True

    def _get_year(self) -> int:
        """Return year from URL."""
        return int(self.url_parts[2])

    def _get_month(self) -> int:
        """Return month from URL."""
        return int(self.url_parts[4])

    def _set_year(self, year: int) -> None:
        """Set year in URL."""
        self.url_parts[2] = str(year)

    def _set_month(self, month: int) -> None:
        """Set month in URL (month always has two digits)."""
        _month: str = str(month)
        if len(_month) == 1:  # Add '0' if month has only one digit
            _month = "0" + _month
        self.url_parts[4] = _month

    def _set_number(self, number: int) -> None:
        """Set newsticker number in URL."""
        self.url_parts[7] = str(number)

    def _set_all_params(self, year: int, month: int, number: int) -> None:
        """Set year, month, and newsticker number in URL."""
        self._set_year(year)
        self._set_month(month)
        self._set_number(number)

    def _is_url_valid(self) -> bool:
        """Check if set URL is valid."""
        url: Union[str, None] = self.get_url()
        if url is None:
            # None is treated as a valid URL which means the URL doesn't exist
            return True
        try:
            response: requests.models.Response = requests.get(url)
            response.raise_for_status()  # Raise error for 4xx or 5xx responses
            return True
        except requests.exceptions.RequestException:
            return False

    def get_number(self) -> int:
        """Return newsticker number from URL."""
        return int(self.url_parts[7])

    def get_url(self) -> Union[str, None]:
        """Return the whole URL."""
        # Return the hardcoded URL if there is one for the newsticker number
        number: int = self.get_number()
        if number in SPECIAL_URLS:
            return SPECIAL_URLS[number]

        url: str = ""
        for url_part in self.url_parts:
            url += url_part
        return url

    def increment_number(self) -> Self:
        """Increment newsticker number to URL and validate it."""
        year: int = self._get_year()
        month: int = self._get_month()
        number: int = self.get_number()
        number += 1
        self._set_number(number)

        # Check if URL with increased number is valid, otherwise increase month
        if not self._is_url_valid():
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1

        # Set all parameters for new URL
        self._set_all_params(
            year=year,
            month=month,
            number=number,
        )

        # Raise error if new URL is not valid
        if not self._is_url_valid():
            raise requests.exceptions.RequestException(f"Invalid URL: {self.get_url()}")

        return self
