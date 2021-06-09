"""Module providing the engine for memes generation."""
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

from QuoteEngine import QuoteModel


class MemeEngine:
    """Class for generating memes."""

    def __init__(self, output_dir):
        """Initialize an object.

        @param output_dir: directory where an output image is to be stored.
        """
        self.output_dir = output_dir

    MAX_IMG_WIDTH = 500
    TEXT_AUTH_DIST = 40
    MARGINS_SIZE = 10
    FONT_SIZE = 25
    WRAP_SIZE = 25
    QUOTE_FONT = "./fonts/LilitaOne-Regular.ttf"
    AUTHOR_FONT = "./fonts/SansitaSwashed-Regular.ttf"
    FONT_COLOR = (255, 255, 255)

    _font_quote = ImageFont.truetype(QUOTE_FONT, FONT_SIZE)
    _font_author = ImageFont.truetype(AUTHOR_FONT, FONT_SIZE)

    def make_meme(self, img_path: str, quote: QuoteModel,
                  width=500) -> str:
        """Generate meme based on provided image and text.

        @param img_path: Image on which the text will be placed.
        @param quote: Quote placed on the image.
        @param width: Desired width of the image.
        @return: Path to the generated meme image.
        """
        meme_no = random.randint(0, 10000)
        output_path = self.output_dir + "/meme_" + str(meme_no) + ".jpg"

        # The image width cannot be larger than 'MAX_IMG_WIDTH'
        if width > self.MAX_IMG_WIDTH:
            width = self.MAX_IMG_WIDTH

        text_body, no_lines = get_wrapped_text(quote.body, self.WRAP_SIZE)
        max_text_width = self.get_max_text_width(quote)

        with Image.open(img_path) as img:
            img = proportional_resize(img, width)
            d = ImageDraw.Draw(img)
            pos = self.get_random_text_pos(img, max_text_width, no_lines)
            d.text(pos, text_body, font=self._font_quote, fill=self.FONT_COLOR)
            pos = pos[0], pos[1] + self.FONT_SIZE * no_lines + self.TEXT_AUTH_DIST
            d.text(pos, quote.author, font=self._font_author, fill=self.FONT_COLOR)
            img.save(output_path)

        return output_path

    def get_random_text_pos(self, img: Image, max_text_width: int,
                            no_body_lines: str) -> (int, int):
        """Get random text pos for the image, considering its size and margins.

        @param img: Image on which the text will be drawn.
        @param max_text_width: Max text width in pixels.
        @param no_body_lines: Number of lines for a body text.
        @return: Tuple of (x, y) position of the text.
        """
        width = img.size[0]
        height = img.size[1]

        x_range, y_range = self.get_pos_ranges(width, height, no_body_lines, max_text_width)
        pos_x = random.randint(*x_range)
        pos_y = random.randint(*y_range)

        return pos_x, pos_y

    def get_pos_ranges(self, width: int, height: int,
                       no_body_lines: int, max_text_width: int):
        """Get ranges of permitted text location.

        @param width: Image width
        @param height: Image height
        @param no_body_lines: number of body text lines
        @param max_text_width: Max width of the text in pixels.
        @return: Ranges of permitted text location.
        """
        min_pos_x = self.MARGINS_SIZE
        min_pos_y = self.MARGINS_SIZE
        max_pos_x = width - self.MARGINS_SIZE - max_text_width
        max_pos_y = height - self.MARGINS_SIZE - no_body_lines * self.FONT_SIZE - self.TEXT_AUTH_DIST
        if max_pos_x < min_pos_x:
            max_pos_x = min_pos_x + 1
        if max_pos_y < min_pos_y:
            max_pos_y = min_pos_y + 1
        return (min_pos_x, max_pos_x), (min_pos_y, max_pos_y)

    def get_max_text_width(self, quote: QuoteModel):
        """Get max width of the text quote.

        @param quote: quote of the meme
        @return: Max width of the text
        """
        max_text_len = max(len(quote.body), len(quote.author))
        # Experimentally chosen average width of one letter.
        width_of_a_letter = self.FONT_SIZE / 2
        text_size = int(max_text_len * width_of_a_letter)
        return text_size


def proportional_resize(img: Image, width: int) -> Image:
    """Resize the image proportionally, based on desired width.

    @param img: Image to be resized.
    @param width: Desired width.
    @return: Resized image.
    """
    percent = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(percent)))
    img = img.resize((width, height), Image.ANTIALIAS)
    return img


def get_wrapped_text(text: str, width: int) -> (str, int):
    """Wrap the text, given the max text width.

    @param text: Text to be wrapped.
    @param width: Max text width.
    @return: Wrapped text and number of lines.
    """
    wrapper = textwrap.TextWrapper(width=width)
    lines = wrapper.wrap(text=text)
    wrapped_text = ''
    for ii in lines[:-1]:
        wrapped_text = wrapped_text + ii + '\n'
    wrapped_text += lines[-1]
    no_lines = len(lines)

    return wrapped_text, no_lines
