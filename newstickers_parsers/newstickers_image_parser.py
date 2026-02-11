import re
from dataclasses import dataclass, field

import numpy as np
import pytesseract  # type: ignore
from PIL import Image, ImageFile, ImageOps


@dataclass
class NewstickersImageParser:
    """Class for recognizing and extracting the newsticker from the image on the newsticker's website."""

    image: ImageFile.ImageFile
    raw_text: str = field(init=False)

    def __post_init__(self) -> None:
        """
        Set the image and invert it for better text recognition.
        After inversion, the text is black on white.
        """
        inverted_image: Image.Image = ImageOps.invert(self.image)
        image_array = np.array(inverted_image)
        self.raw_text: str = pytesseract.image_to_string(image_array, lang="deu")

    def extract_newsticker(self) -> str:
        """Return only the clean newsticker within '+++'."""
        raw_text_parts: list[str] = self.raw_text.split()
        pattern: str = r"\+{1,3}"  # Exactly 1, 2, or 3 pluses
        for idx, part in enumerate(raw_text_parts):
            if bool(re.fullmatch(pattern, part)):  # Hit start of newsticker
                del raw_text_parts[:idx + 1]  # Remove everything before including the pluses
                break
        clean_text_parts: list[str] = ["+++"]
        for part in raw_text_parts:  # Traverse words after start of newsticker
            if bool(re.fullmatch(pattern, part)):  # Hit end of newsticker
                clean_text_parts.append("+++")
                break
            clean_text_parts.append(part)

        # Concatenate cleaned text parts
        result: str = ""
        for part in clean_text_parts:
            result += part + " "
        return result

    @staticmethod
    def is_newsticker_valid(newsticker: str) -> bool:
        """
        Return True if the newsticker is valid, False otherwise.
        A valid newsticker must have the following format:
            +++ <part1> <part2> ... <partN>: <partN+1> <partN+2> ... +++
        """
        newsticker_parts: list[str] = newsticker.split()
        if len(newsticker_parts) < 3:
            return False

        # First and last part must be exactly 1, 2, or 3 pluses
        pattern: str = r"\+{1,3}"
        if not (bool(re.fullmatch(pattern, newsticker_parts[0])) and bool(re.fullmatch(pattern, newsticker_parts[-1]))):
            return False

        # Search for colon
        # The part with the colon needs to be in front of at least two parts, i.e. a word and the +++
        for part in newsticker_parts[1:-2]:
            if ":" in part:
                break
        else:  # Invalid if no colon found
            return False

        return True