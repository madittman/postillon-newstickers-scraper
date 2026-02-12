import glob
import os
from pathlib import Path
from unittest.mock import Mock, patch

from bs4 import Tag

from models.newsticker import Newsticker
from newstickers_parsers.newstickers_image_parser import NewstickersImageParser
from tests.data.expected_objects import (
    EXPECTED_IMAGE_PATH_BY_WEBSITE,
    expected_newsticker_by_website,
)

# Construct the full path to the testing files
TESTS_PATH: str = str(Path(__file__).parent.parent)
DATA_PATH: str = os.path.join(TESTS_PATH, "data")
WEBSITES: list[str] = glob.glob(pathname=os.path.join(DATA_PATH, "websites", "*.html"))


def get_mocked_parser(filename: str) -> NewstickersImageParser:
    """
    Return a NewstickersImageParser object that reads the file as a mocked HTML page.
    Read the file as binary ("rb") because 'requests.Response.content' returns bytes.
    """
    with open(filename, "rb") as file:
        response_content: bytes = file.read()

    # Create Mock object to act as the response
    mock_response: Mock = Mock()
    mock_response.content = response_content

    # Patch 'requests.get' to return the mock response
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        return NewstickersImageParser(url=filename)  # The mocked URL is the filename


def test_get_image_tag() -> None:
    """Test method '_get_image_tag' from NewstickersImageParser class."""
    for website in WEBSITES:
        mocked_parser: NewstickersImageParser = get_mocked_parser(website)
        image_tag: Tag | None = mocked_parser._get_image_tag()

        # 'image_url' is the full path to the HTML file since 'request.get' was mocked to read file instead
        image_url: str | None = str(image_tag.get("src")) if image_tag else None

        image_filename: str | None = str(Path(image_url).name) if image_url else None

        # Extract image filename from 'EXPECTED_IMAGE_PATH_BY_WEBSITE'
        expected_image_path: str | None = EXPECTED_IMAGE_PATH_BY_WEBSITE[
            Path(website).name
        ]
        expected_image_filename: str | None = (
            Path(expected_image_path).name if expected_image_path else None
        )

        assert image_filename == expected_image_filename


def test_get_newsticker() -> None:
    """Test method 'get_newsticker' from NewstickersImageParser class."""
    for website in WEBSITES:
        mocked_parser: NewstickersImageParser = get_mocked_parser(website)

        # Extract full image path from 'EXPECTED_IMAGE_PATH_BY_WEBSITE'
        expected_image_path: str | None = EXPECTED_IMAGE_PATH_BY_WEBSITE[
            Path(website).name
        ]
        if not expected_image_path:
            continue  # Skip website when there is no image
        expected_full_image_path: str = os.path.join(
            DATA_PATH, "websites", expected_image_path
        )

        with open(expected_full_image_path, "rb") as file:
            response_content: bytes = file.read()

        # Create Mock object to act as the response
        mock_response: Mock = Mock()
        mock_response.content = response_content

        # Patch 'requests.get' when it is called from 'get_newsticker' method
        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_response
            newsticker: Newsticker | None = mocked_parser.get_newsticker()

        # Assert Newsticker object
        expected_newsticker: Newsticker | None = expected_newsticker_by_website(
            Path(website).name, DATA_PATH
        )
        assert newsticker == expected_newsticker
