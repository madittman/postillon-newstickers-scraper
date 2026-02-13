from datetime import datetime
from typing import Generator
from unittest.mock import Mock, patch

import pytest
import requests

from url_builder.url_builder import UrlBuilder


@pytest.fixture
def mocked_url_builder() -> Generator[UrlBuilder]:

    # Create Mock object to act as the response
    mock_method: Mock = Mock()

    # Define mapping of URLs to return whether URL is valid
    def side_effect(url: str) -> bool:
        returns: dict[str, bool] = {
            "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html": True,
            "https://www.der-postillon.com/0/00/newsticker-0.html": False,
            "https://www.der-postillon.com/2009/02/newsticker-2.html": True,
            "https://www.der-postillon.com/0/00/newsticker-1001.html": False,
        }
        return returns.get(url, False)

    mock_method.side_effect = side_effect

    # Patch '_is_url_valid' method to return the mocked value
    with patch.object(UrlBuilder, "_is_url_valid", new=mock_method):
        yield UrlBuilder()


def test_lower_equal(mocked_url_builder: UrlBuilder) -> None:
    """Test dunder method '__le__' from UrlBuilder class."""
    assert mocked_url_builder <= datetime(2020, 1, 1)


def test_getters(mocked_url_builder: UrlBuilder) -> None:
    """Test getter methods from UrlBuilder class."""
    assert mocked_url_builder._get_year() == 2009
    assert mocked_url_builder._get_month() == 2
    assert mocked_url_builder.get_number() == 1
    assert (
        mocked_url_builder.get_url()
        == "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html"
    )


def test_set_params(mocked_url_builder: UrlBuilder) -> None:
    """Test method '_set_params' from UrlBuilder class."""
    mocked_url_builder.set_all_params(
        year=2023,
        month=5,
        number=5000,
    )
    assert mocked_url_builder._get_year() == 2023
    assert mocked_url_builder._get_month() == 5
    assert mocked_url_builder.get_number() == 5000
    assert (
        mocked_url_builder.get_url()
        == "https://www.der-postillon.com/2023/05/newsticker-5000.html"
    )


def test_some_special_urls(mocked_url_builder: UrlBuilder) -> None:
    """Test method '_get_url' for some special URLs from UrlBuilder class."""
    mocked_url_builder._set_number(60)
    assert (
        mocked_url_builder.get_url()
        == "https://www.der-postillon.com/2010/04/newsticker-60_05.html"
    )
    mocked_url_builder._set_number(71)
    assert mocked_url_builder.get_url() is None  # Newsticker 71 doesn't exist


def test_is_url_valid(mocked_url_builder: UrlBuilder) -> None:
    """Test method '_is_url_valid' from UrlBuilder class."""
    url: str | None = mocked_url_builder.get_url()
    assert mocked_url_builder._is_url_valid(url)

    mocked_url_builder.set_all_params(
        year=0,
        month=0,
        number=0,
    )
    url = mocked_url_builder.get_url()
    assert not mocked_url_builder._is_url_valid(url)


def test_increment_number(mocked_url_builder: UrlBuilder) -> None:
    """Test method '_increment_number' from UrlBuilder class."""
    mocked_url_builder.increment_number()
    assert mocked_url_builder._get_year() == 2009
    assert mocked_url_builder._get_month() == 2
    assert mocked_url_builder.get_number() == 2
    assert (
        mocked_url_builder.get_url()
        == "https://www.der-postillon.com/2009/02/newsticker-2.html"
    )

    # Create an invalid URL so that increment fails
    mocked_url_builder.set_all_params(
        year=0,
        month=0,
        number=1000,
    )
    with pytest.raises(requests.exceptions.RequestException):
        mocked_url_builder.increment_number()
