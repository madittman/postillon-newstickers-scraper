import glob
import os
from pathlib import Path
from unittest.mock import Mock, patch

from bs4 import Tag

from newstickers_parsers.newstickers_image_parser import NewstickersImageParser
from tests.data.newsticker_strings import EXPECTED_IMAGE_FILENAME_BY_FILENAME

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


def _test_get_image_tag() -> None:
    """Test method '_get_image_tag' from NewstickersImageParser class."""
    for website in WEBSITES:
        mocked_parser: NewstickersImageParser = get_mocked_parser(website)
        image_tag: Tag | None = mocked_parser._get_image_tag()

        # 'image_url' is the full path to the HTML file since 'request.get' was mocked to read file instead
        image_url: str | None = str(image_tag.get("src")) if image_tag else None

        image_filename: str | None = str(Path(image_url).name) if image_url else None

        expected_image_filename: str | None = EXPECTED_IMAGE_FILENAME_BY_FILENAME[
            Path(website).name
        ]
        assert image_filename == expected_image_filename


def test_get_raw_text_from_image() -> None:
    """Test method '_get_raw_text_from_image' from NewstickersImageParser class."""
    for website in WEBSITES:
        pass
        # mocked_parser: NewstickersImageParser = get_mocked_parser(filename)
