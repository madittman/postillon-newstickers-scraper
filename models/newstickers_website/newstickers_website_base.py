"""ORM class for a newsticker's website"""

from datetime import date

from pydantic import BaseModel


class NewstickersWebsiteBase(BaseModel):
    number: int
    title: str
    date: date
    url: str
