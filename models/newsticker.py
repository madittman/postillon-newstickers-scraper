"""ORM class for a newsticker"""

from dataclasses import dataclass
from typing import Optional

from models.newstickers_website import NewstickersWebsite


@dataclass
class Newsticker:
    text: str
    newstickers_website: NewstickersWebsite
    extracted_from_image: bool

    # Only set when 'extracted_from_image' is True
    image_extraction_invalid: Optional[bool] = None