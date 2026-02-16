from typing import Optional

from pydantic import BaseModel

from models.newstickers_website.newstickers_website_base import NewstickersWebsiteBase


class NewstickerBase(BaseModel):
    text: str
    newstickers_website: NewstickersWebsiteBase
    extracted_from_image: bool

    # Only set when 'extracted_from_image' is True
    image_extraction_invalid: Optional[bool] = None
