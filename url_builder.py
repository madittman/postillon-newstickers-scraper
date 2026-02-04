import requests
import re
from dataclasses import dataclass
from typing import Self


@dataclass
class UrlBuilder:
    """Class for generating a valid URL for a Postillon's newstickers site."""

    # Start from URL of newsticker with number 2
    raw_url: str = "https://www.der-postillon.com/2009/02/newsticker-2.html"

    def _get_year(self) -> int:
        """Return year from URL as int."""
        return int(self.raw_url.split("/")[3])

    def _get_month(self) -> int:
        """Return month from URL as int."""
        return int(self.raw_url.split("/")[4])

    def _get_number(self) -> int:
        """Return newsticker's number from URL as int."""
        # Split URL by '-' or '.'
        return int(re.split(r'[-.]', self.raw_url)[4])

    def _set_year(self, year: int) -> None:
        """Set year in URL."""
        parts: list[str] = self.raw_url.split("/")
        parts[3] = str(year)
        self.raw_url = "/".join(parts)

    def _set_month(self, month: int) -> None:
        """Set month in URL."""
        parts: list[str] = self.raw_url.split("/")
        parts[4] = str(month)

        # Add '0' if month is one digit
        if len(parts[4]) == 1:
            parts[4] = "0" + parts[4]
        self.raw_url = "/".join(parts)

    def _set_number(self, number: int) -> None:
        """Set newsticker's number in URL."""
        shortened_url: str = self.raw_url[:-5]  # Remove .html ending
        parts: list[str] = shortened_url.split("/")
        parts[5] = "newsticker-" + str(number)
        self.raw_url = "/".join(parts) + ".html"

    def _set_all_params(self, year: int, month: int, number: int) -> None:
        """Set year, month, and newsticker's number in URL."""
        self._set_year(year)
        self._set_month(month)
        self._set_number(number)

    def _is_url_valid(self) -> bool:
        """Check if set URL is valid."""
        try:
            response: requests.models.Response = requests.get(self.raw_url)
            response.raise_for_status()  # Raise error for 4xx or 5xx responses
            return True
        except requests.exceptions.RequestException:
            return False

    def __add__(self, number: int) -> Self:
        """Increment newsticker's number to URL."""
        for _ in range(number):
            year: int = self._get_year()
            month: int = self._get_month()
            number: int = self._get_number()
            number += 1
            self._set_number(number)

            # Check if URL with increased number is valid, otherwise increase month
            if not self._is_url_valid():
                if month < 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self._set_all_params(year, month, number)

            # Check if URL is valid with increased month, otherwise throw an error
            if not self._is_url_valid():
                raise Exception(f"Invalid URL: {self.raw_url}")

        return self