"""ORM class for a newsticker's website"""

from beanie import Document

from models.newstickers_website.newstickers_website_base import NewstickersWebsiteBase


# Database Object (Beanie)
class NewstickersWebsite(NewstickersWebsiteBase, Document):
    class Settings:
        name = "websites"  # collection name
