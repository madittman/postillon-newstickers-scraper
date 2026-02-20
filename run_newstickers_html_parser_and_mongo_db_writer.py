"""
Run MongoDbWriter to insert Newsticker objects into MongoDB.
This requires a local running MongoDB server the MongoDbWriter can connect to!
"""

import asyncio
from datetime import date

from models.newsticker.newsticker import Newsticker
from models.newsticker.newsticker_base import NewstickerBase
from models.newstickers_website.newstickers_website_base import NewstickersWebsiteBase
from mongo_db_writer.mongo_db_writer import MongoDbWriter

URI: str = "mongodb://localhost:27017"
DB_NAME: str = "test_newstickers"


# ONLY for testing
async def main():
    mongo_db_writer: MongoDbWriter = MongoDbWriter(uri=URI, db_name=DB_NAME)

    # Initialize the database
    await mongo_db_writer.initialize()

    # Create a NewstickersWebsiteBase object
    newstickers_website_base: NewstickersWebsiteBase = NewstickersWebsiteBase(
        number=1, title="Example News", date=date.today(), url="https://example.com"
    )

    # Create a NewstickerBase object referencing the inserted NewstickersWebsite object
    newsticker_base: NewstickerBase = NewstickerBase(
        text="Breaking news!",
        newstickers_website=newstickers_website_base,
        extracted_from_image=False,
    )

    # Convert the NewstickerBase object to a standard Python dict
    # and unpack that dict into the arguments for Newsticker
    newsticker: Newsticker = Newsticker(**newsticker_base.model_dump())

    newstickers: list[Newsticker] = [newsticker, newsticker]
    for _newsticker in newstickers:
        try:
            # Insert Newsticker object into database
            await mongo_db_writer.insert_newsticker(_newsticker)

        except Exception as e:
            print(f"Stopped insertion due to error: {e}")
            raise  # Halt on first error

    print("All Newstickers inserted successfully.")


asyncio.run(main())
