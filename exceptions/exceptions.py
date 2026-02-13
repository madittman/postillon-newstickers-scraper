class NoPostBodyDivFoundError(Exception):
    """Raised when 'post-body' <div> tag could not be found on newsticker's website."""

    pass


class NoValidTitleFoundError(Exception):
    """Raised when title from newsticker's website could not be parsed."""

    pass


class NoValidDateFoundError(Exception):
    """Raised when time/date from newsticker's website could not be parsed."""

    pass


class NoNewstickerFoundError(Exception):
    """Raised when no newsticker was found on newsticker's website."""

    pass


class NoValidImageFoundError(Exception):
    """Raised when image from newsticker's website could not be parsed."""

    pass
