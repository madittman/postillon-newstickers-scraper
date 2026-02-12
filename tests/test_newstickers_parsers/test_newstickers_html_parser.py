import glob
import os
from pathlib import Path
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from models.newstickers_website import NewstickersWebsite
from newstickers_parsers.newstickers_html_parser import NewstickersHtmlParser
from tests.data.newsticker_strings import EXPECTED_NEWSTICKER_STRINGS_BY_WEBSITE

# Construct the full path to the testing files
TESTS_PATH: str = str(Path(__file__).parent.parent)
DATA_PATH: str = os.path.join(TESTS_PATH, "data")
WEBSITES: list[str] = glob.glob(
    pathname=os.path.join(DATA_PATH, "websites", "*.html")
)


def get_mocked_parser(website: str) -> NewstickersHtmlParser:
    """
    Return a NewstickersHtmlParser object that reads the HTML page as a mocked response.
    Read the file as binary ("rb") because 'requests.Response.content' returns bytes.
    """
    with open(website, "rb") as file:
        response_content: bytes = file.read()

    # Create Mock object to act as the response
    mock_response: Mock = Mock()
    mock_response.content = response_content

    # Patch 'requests.get' to return the mock response
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        return NewstickersHtmlParser(url=website)  # The mocked URL is the locally stored website


def test_post_init() -> None:
    """Test dunder method '__post_init__' from parent class."""
    for website in WEBSITES:
        with open(website, "rb") as file:
            mocked_parser: NewstickersHtmlParser = get_mocked_parser(website)
            expected_soup: BeautifulSoup = BeautifulSoup(file.read(), features="html.parser")
            assert mocked_parser.soup == expected_soup

def test_get_newstickers_website() -> None:
    """Test method '_get_newstickers_website' from parent class."""
    for website in WEBSITES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(website)
        newstickers_website: NewstickersWebsite = mocked_parser._get_newstickers_website()

        expected_title_string: str = mocked_parser._get_title_string()
        expected_newstickers_website: NewstickersWebsite = NewstickersWebsite(
            number=mocked_parser._get_number_from_title_string(expected_title_string),
            title=expected_title_string,
            date=mocked_parser._get_date(),
            url=website,
        )
        assert newstickers_website == expected_newstickers_website

def test_extract_newsticker_strings() -> None:
    """Test method '_extract_newsticker_strings' from NewstickersHtmlParser class."""
    for website in WEBSITES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(website)
        newsticker_strings: list[str] = mocked_parser._extract_newsticker_strings()
        expected_newsticker_strings: list[str] = EXPECTED_NEWSTICKER_STRINGS_BY_WEBSITE[Path(website).name]
        assert newsticker_strings == expected_newsticker_strings

def test_get_next_newsticker() -> None:
    """Test generator 'get_next_newsticker' from NewstickersHtmlParser class."""
    for website in WEBSITES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(website)
        for newsticker in mocked_parser.get_next_newsticker():
            expected_newsticker_strings: list[str] = EXPECTED_NEWSTICKER_STRINGS_BY_WEBSITE[Path(website).name]

            # Assert Newsticker object
            assert newsticker.text in expected_newsticker_strings
            assert newsticker.extracted_from_image == False
            assert newsticker.image_extraction_invalid is None

            # Assert NewstickersWebsite object
            newstickers_website: NewstickersWebsite = newsticker.newstickers_website
            expected_title_string: str = mocked_parser._get_title_string()
            assert newstickers_website.title == expected_title_string
            assert newstickers_website.number == mocked_parser._get_number_from_title_string(expected_title_string)
            assert newstickers_website.date == mocked_parser._get_date()
            assert newstickers_website.url == website