"""ORM class for a newsticker"""

from beanie import Document

from models.newsticker.newsticker_base import NewstickerBase


# Database Object (Beanie)
class Newsticker(NewstickerBase, Document):
    class Settings:
        name = "newstickers"  # collection name
