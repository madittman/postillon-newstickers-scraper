from datetime import datetime

import pytest
import requests

from url_builder.url_builder import UrlBuilder


@pytest.fixture
def url_builder() -> UrlBuilder:
    return UrlBuilder()


def test_lower_equal(url_builder) -> None:
    assert url_builder <= datetime(2020, 1, 1)


def test_default_params(url_builder) -> None:
    assert url_builder._get_year() == 2009
    assert url_builder._get_month() == 2
    assert url_builder.get_number() == 1
    assert (
        url_builder.get_url()
        == "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html"
    )


def test_set_params(url_builder) -> None:
    url_builder.set_all_params(
        year=2023,
        month=5,
        number=5000,
    )
    assert url_builder._get_year() == 2023
    assert url_builder._get_month() == 5
    assert url_builder.get_number() == 5000
    assert (
        url_builder.get_url()
        == "https://www.der-postillon.com/2023/05/newsticker-5000.html"
    )


def test_some_special_urls(url_builder) -> None:
    url_builder._set_number(60)
    assert (
        url_builder.get_url()
        == "https://www.der-postillon.com/2010/04/newsticker-60_05.html"
    )
    url_builder._set_number(71)
    assert url_builder.get_url() is None  # Newsticker 71 doesn't exist


def test_is_url_valid(url_builder) -> None:
    assert url_builder._is_url_valid() is True
    url_builder.set_all_params(
        year=0,
        month=0,
        number=0,
    )
    assert url_builder._is_url_valid() is False


def test_increment_number(url_builder) -> None:
    url_builder.increment_number()
    assert url_builder._get_year() == 2009
    assert url_builder._get_month() == 2
    assert url_builder.get_number() == 2
    assert (
        url_builder.get_url()
        == "https://www.der-postillon.com/2009/02/newsticker-2.html"
    )

    # Create an invalid URL so that increment fails
    url_builder.set_all_params(
        year=0,
        month=0,
        number=1000,
    )
    with pytest.raises(requests.exceptions.RequestException):
        url_builder.increment_number()
