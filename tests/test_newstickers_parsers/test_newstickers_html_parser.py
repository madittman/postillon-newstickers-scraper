import glob
import os
from pathlib import Path
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from models.newstickers_website import NewstickersWebsite
from newstickers_parsers.newstickers_html_parser import NewstickersHtmlParser
from tests.data.newsticker_strings import NEWSTICKER_STRINGS_BY_FILENAME

# Construct the full path to the testing files
TESTS_PATH: str = str(Path(__file__).parent.parent)
DATA_PATH: str = os.path.join(TESTS_PATH, "data")
FILENAMES: list[str] = glob.glob(
    pathname=os.path.join(DATA_PATH, "websites", "*.html")
)


def get_mocked_parser(filename: str) -> NewstickersHtmlParser:
    """
    Return a NewstickersHtmlParser object that reads the file as a mocked HTML page.
    Read the file as binary ("rb") because 'requests.Response.content' returns bytes.
    """
    with open(filename, "rb") as file:
        response_content: bytes = file.read()

    # Create Mock object to act as the response
    fake_response: Mock = Mock()
    fake_response.content = response_content

    # Patch 'requests.get' to return the fake response
    with patch("requests.get") as mock_get:
        mock_get.return_value = fake_response

        # The URL argument doesn't matter since the response is mocked
        return NewstickersHtmlParser(url=filename)


def test_post_init() -> None:
    for filename in FILENAMES:
        with open(filename, "rb") as file:
            mocked_parser: NewstickersHtmlParser = get_mocked_parser(filename)
            expected_soup: BeautifulSoup = BeautifulSoup(file.read(), features="html.parser")
            assert mocked_parser.soup == expected_soup

def test_get_newstickers_website() -> None:
    for filename in FILENAMES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(filename)
        newstickers_website: NewstickersWebsite = mocked_parser._get_newstickers_website()

        expected_title_string: str = mocked_parser._get_title_string()
        expected_newstickers_website: NewstickersWebsite = NewstickersWebsite(
            number=mocked_parser._get_number_from_title_string(expected_title_string),
            title=expected_title_string,
            date=mocked_parser._get_date(),
            url=filename,
        )
        assert newstickers_website == expected_newstickers_website

def test_extract_newsticker_strings() -> None:
    for filename in FILENAMES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(filename)
        newsticker_strings: list[str] = mocked_parser._extract_newsticker_strings()
        assert newsticker_strings == NEWSTICKER_STRINGS_BY_FILENAME[Path(filename).name]

def test_get_next_newsticker() -> None:
    for filename in FILENAMES:
        mocked_parser: NewstickersHtmlParser = get_mocked_parser(filename)
        for newsticker in mocked_parser.get_next_newsticker():
            # Assert Newsticker object
            assert newsticker.text in NEWSTICKER_STRINGS_BY_FILENAME[Path(filename).name]
            assert newsticker.extracted_from_image == False
            assert newsticker.image_extraction_invalid is None

            # Assert NewstickersWebsite object
            newstickers_website: NewstickersWebsite = newsticker.newstickers_website
            expected_title_string: str = mocked_parser._get_title_string()
            assert newstickers_website.title == expected_title_string
            assert newstickers_website.number == mocked_parser._get_number_from_title_string(expected_title_string)
            assert newstickers_website.date == mocked_parser._get_date()
            assert newstickers_website.url == filename