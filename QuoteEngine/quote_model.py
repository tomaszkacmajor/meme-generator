"""Module with QuoteModel class."""
import random
from PIL import ImageFont


class QuoteModel:
    """A class encapsulating body, author of a quote and their appearance."""

    def __init__(self, body: str, author: str):
        """Construct a new QuoteModel object.

        @param body: body of a quote
        @param author: author of a quote
        """
        self.body = body
        self.author = author

        self.font_size = random.randint(20, 30)
        self.font_quote = ImageFont.truetype("./fonts/LilitaOne-Regular.ttf", self.font_size)
        self.font_author = ImageFont.truetype("./fonts/SansitaSwashed-Regular.ttf", self.font_size)
