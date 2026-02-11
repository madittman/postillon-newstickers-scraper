"""ORM class for a newsticker's website"""

from dataclasses import dataclass
from datetime import date


@dataclass
class NewstickersWebsite:
    number: int
    title: str
    date: date
    url: str