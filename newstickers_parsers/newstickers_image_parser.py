import re
import sys
from dataclasses import dataclass
from io import BytesIO

import numpy as np
import pytesseract  # type: ignore
import requests
from bs4 import Tag
from bs4.element import AttributeValueList
from PIL import Image, ImageOps
from requests import Response

from exceptions.exceptions import NoValidImageFoundError
from models.newsticker import Newsticker
from models.newstickers_website import NewstickersWebsite
from newstickers_parsers.newstickers_parser import NewstickersParser


@dataclass
class NewstickersImageParser(NewstickersParser):
    """Class for recognizing and extracting the newsticker from the image on the newsticker's website."""

    def _get_image_tag(self) -> Tag | None:
        """
        Find and return the <img> tag from the newsticker's website.
        If no valid image tag is found, return None.
        """

        # Find the <div> tag that wraps the image
        div_tag: Tag | None = self.soup.find("div", class_="separator")
        if not div_tag:
            return None

        # Find the <a> tag that wraps the image
        a_tag: Tag | None = div_tag.find("a")
        if not a_tag:
            raise NoValidImageFoundError(
                f"<a> tag from URL '{self.url}' could not be parsed"
            )

        # Extract the actual <img> tag inside the <a> tag
        img_tag: Tag | None = a_tag.find("img")
        if not img_tag:
            raise NoValidImageFoundError(
                f"<img> tag from URL '{self.url}' could not be parsed"
            )

        # If image width is less than or equal to 1, it's not a newsticker image
        image_width: str | AttributeValueList | None = img_tag.get("width")
        if not isinstance(image_width, str):
            raise NoValidImageFoundError(
                f"Image width from URL '{self.url}' could not be parsed"
            )

        if int(str(image_width)) <= 1:
            return None

        return img_tag

    def _get_image(self) -> Image.Image | None:
        """
        Return the image from the newsticker's website as a PIL Image object.
        Raise error if image URL could not be parsed.
        """
        image_tag: Tag | None = self._get_image_tag()
        if not image_tag:
            return None
        image_url: str | AttributeValueList | None = image_tag.get("src")
        if not isinstance(image_url, str):
            raise NoValidImageFoundError(
                f"Image URL from URL '{self.url}' could not be parsed"
            )

        # Download the image data
        response: Response = requests.get(image_url)

        # Raise error for 4xx or 5xx responses
        response.raise_for_status()

        # Convert raw bytes into a PIL Image object
        # (BytesIO creates a file-like object in memory that PIL can read)
        return Image.open(BytesIO(response.content))

    def get_newsticker(self) -> Newsticker | None:
        """Return the Newsticker object or return None if no valid image is found."""
        newstickers_website: NewstickersWebsite = self._get_newstickers_website()
        image: Image.Image | None = self._get_image()
        if not image:
            return None

        raw_text: str = self._get_raw_text_from_image(image)
        newsticker_string: str = self._get_newsticker_string(raw_text)

        # Set 'image_extraction_invalid' to True and print error message when newsticker could not be read properly
        image_extraction_invalid: bool = False
        if not self._is_newsticker_string_valid(newsticker_string):
            image_extraction_invalid = True
            print(
                "> The following image text could not be properly recognized:\n"
                + f"'{newsticker_string}'\n"
                + f"from URL '{self.url}'\n",
                file=sys.stderr,
            )

        return Newsticker(
            text=newsticker_string,
            newstickers_website=newstickers_website,
            extracted_from_image=True,
            image_extraction_invalid=image_extraction_invalid,
        )

    @staticmethod
    def _get_raw_text_from_image(image: Image.Image) -> str:
        """Read and return the newsticker's raw text from the image."""

        # Invert the image for better text recognition.
        # After inversion, the text is black on white.
        inverted_image: Image.Image = ImageOps.invert(image)
        image_array = np.array(inverted_image)

        # Read text from inverted image
        return pytesseract.image_to_string(image_array, lang="deu")

    @staticmethod
    def _get_newsticker_string(raw_text: str) -> str:
        """Return only the clean newsticker within '+++' from the raw text."""
        raw_text_parts: list[str] = raw_text.split()
        pattern: str = r"\+{1,3}"  # Exactly 1, 2, or 3 pluses
        for idx, part in enumerate(raw_text_parts):
            if bool(re.fullmatch(pattern, part)):  # Hit start of newsticker
                del raw_text_parts[
                    : idx + 1
                ]  # Remove everything before including the pluses
                break
        clean_text_parts: list[str] = ["+++"]
        for part in raw_text_parts:  # Traverse words after start of newsticker
            if bool(re.fullmatch(pattern, part)):  # Hit end of newsticker
                clean_text_parts.append("+++")
                break
            clean_text_parts.append(part)

        # Concatenate cleaned text parts
        newsticker_string: str = clean_text_parts[0]
        for part in clean_text_parts[1:]:
            newsticker_string += " " + part

        return newsticker_string

    @staticmethod
    def _is_newsticker_string_valid(newsticker_string: str) -> bool:
        """
        Return True if the newsticker is valid, False otherwise.
        A valid newsticker must have the following format:
            +++ <part1> <part2> ... <partN>: <partN+1> <partN+2> ... +++
        """

        # Newsticker string must consist of at least 3 parts (+++, word, +++)
        newsticker_parts: list[str] = newsticker_string.split()
        if len(newsticker_parts) < 3:
            return False

        # First and last part must be exactly 1, 2, or 3 pluses
        pattern: str = r"\+{1,3}"
        if not (
            bool(re.fullmatch(pattern, newsticker_parts[0]))
            and bool(re.fullmatch(pattern, newsticker_parts[-1]))
        ):
            return False

        # Search for colon
        # The part with the colon needs to be in front of at least two parts, i.e. a word and the +++
        for part in newsticker_parts[1:-2]:
            if ":" in part:
                break
        else:  # Invalid if no colon found
            return False

        # Check for unallowed symbols
        unallowed_symbols: list[str] = [
            "#",
            "$",
            "&",
            "(",
            ")",
            "*",
            "+",
            "/",
            "<",
            "=",
            ">",
            "@",
            "[",
            "\\",
            "]",
            "^",
            "_",
            "`",
            "{",
            "|",
            "}",
            "~",
        ]
        for symbol in unallowed_symbols:
            # Only look for a symbol in the parts between '+++'
            for newsticker_part in newsticker_parts[1:-1]:
                if symbol in newsticker_part:
                    return False

        return True
