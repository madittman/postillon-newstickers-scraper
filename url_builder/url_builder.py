import requests
from dataclasses import dataclass, field
from typing import Self, Union
from datetime import datetime


# Some URLs don't follow the rules, so they are kept here
# A None entry means there was no newsticker with that number
special_urls: dict[int, Union[str, None]] = {
    39: "https://www.der-postillon.com/2009/12/weihnachts-newsticker-39.html",
    45: "https://www.der-postillon.com/2010/01/berufsrisiko-newsticker-45.html",
    54: "https://www.der-postillon.com/2010/03/newsticker-54_08.html",
    56: "https://www.der-postillon.com/2010/03/newsticker-56_18.html",
    60: "https://www.der-postillon.com/2010/04/newsticker-60_05.html",
    71: None,
    100: "https://www.der-postillon.com/2010/09/newsticker-100-das-jubilaum.html",
    500: "https://www.der-postillon.com/2013/09/newsticker-500-xxl-edition-106.html",
    546: "https://www.der-postillon.com/2013/12/newsticker-546_23.html",
    696: "https://www.der-postillon.com/2014/12/newsticker-696-christmas-edition.html",
    991: "https://www.der-postillon.com/2016/12/newsticker-991-weihnachtsspezialausgabe.html",
    992: "https://www.der-postillon.com/2016/12/newsticker-992-weihnachtsspezialausgabe.html",
    1141: "https://www.der-postillon.com/2017/12/newsticker-1141-weihnachtsspezialausgabe.html",
    1290: "https://www.der-postillon.com/2018/12/newsticker-1290_28.html",
    1742: "https://www.der-postillon.com/2021/12/newsticker-1742-weihnachtsausgabe.html",
    1796: None,  # Somehow newsticker 1796 has number 1795 in URL and newsticker 1795 doesn't exist
    1869: "https://www.der-postillon.com/2022/10/newsticker-1869-halloween-spezialausgabe.html",
    2039: "https://www.der-postillon.com/2023/12/newsticker-2039-weihnachtsausgabe.html",
    2339: "https://www.der-postillon.com/2025/12/newsticker-2339-weihnachtsspezialausgabe.html",
}


@dataclass
class UrlBuilder:
    """Class for generating a valid URL for a Postillon's newstickers site."""

    # Start from URL of newsticker with number 2
    url_parts: list[Union[str, int]] = field(default_factory=lambda: [
        "https://",
        "www.der-postillon.com/",
        2009,
        "/",
        2,
        "/",
        "newsticker-",
        2,
        ".html",
    ])

    def get_url(self) -> Union[str, None]:
        """Return the whole URL."""
        # Return the hardcoded URL if the newsticker's number has one
        number: int = self._get_number()
        if number in special_urls:
            return special_urls[number]

        url: str = ""
        for index, part in enumerate(self.url_parts):
            part = str(part)
            if index == 4 and len(part) == 1:  # Add '0' if month is one digit
                part = "0" + part
            url += part
        return url

    def _get_year(self) -> int:
        """Return year from URL."""
        return self.url_parts[2]

    def _get_month(self) -> int:
        """Return month from URL."""
        return self.url_parts[4]

    def _get_number(self) -> int:
        """Return newsticker's number from URL."""
        return self.url_parts[7]

    def _set_year(self, year: int) -> None:
        """Set year in URL."""
        self.url_parts[2] = year

    def _set_month(self, month: int) -> None:
        """Set month in URL."""
        self.url_parts[4] = month

    def _set_number(self, number: int) -> None:
        """Set newsticker's number in URL."""
        self.url_parts[7] = number

    def _set_all_params(self, year: int, month: int, number: int) -> None:
        """Set year, month, newsticker's name and newsticker's number in URL."""
        self._set_year(year)
        self._set_month(month)
        self._set_number(number)

    def _is_url_valid(self) -> bool:
        """Check if set URL is valid."""
        url: Union[str, None] = self.get_url()
        if url is None:
            return True  # None is a valid URL as it doesn't exist
        try:
            response: requests.models.Response = requests.get(url)
            response.raise_for_status()  # Raise error for 4xx or 5xx responses
            return True
        except requests.exceptions.RequestException:
            return False

    def __lt__(self, _datetime: datetime):
        """Compare datetime to URL's year and month."""
        if self._get_year() < _datetime.year:
            return True
        if self._get_month() < _datetime.month:
            return True
        return False

    def __le__(self, _datetime: datetime):
        """Compare datetime to URL's year and month."""
        if self._get_year() <= _datetime.year:
            return True
        if self._get_month() <= _datetime.month:
            return True
        return False

    def __eq__(self, _datetime: datetime):
        """Compare datetime to URL's year and month."""
        if self._get_year() == _datetime.year:
            return True
        if self._get_month() == _datetime.month:
            return True
        return False

    def __ge__(self, _datetime: datetime):
        """Compare datetime to URL's year and month."""
        if self._get_year() >= _datetime.year:
            return True
        if self._get_month() >= _datetime.month:
            return True
        return False

    def __gt__(self, _datetime: datetime):
        """Compare datetime to URL's year and month."""
        if self._get_year() > _datetime.year:
            return True
        if self._get_month() > _datetime.month:
            return True
        return False

    def __add__(self, number: int) -> Self:
        """Increment newsticker's number to URL and validate it."""
        for _ in range(number):
            year: int = self._get_year()
            month: int = self._get_month()
            number: int = self._get_number()

            # Always increase number by 1 and check URL again
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