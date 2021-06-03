"""Module with QuoteModel class."""
class QuoteModel:
    """A class encapsulating body and author of a quote."""

    def __init__(self, body: str, author: str):
        """Construct a new QuoteModel object.

        @param body: body of a quote
        @param author: author of a quote
        """
        self.body = body
        self.author = author
