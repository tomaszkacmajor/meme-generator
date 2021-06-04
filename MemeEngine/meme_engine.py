"""Module providing the engine for memes generation."""
import random
from PIL import Image, ImageDraw
from QuoteEngine import QuoteModel


class MemeEngine:
    """Class for generating memes."""

    def __init__(self, output_dir):
        """Initialize an object.

        @param output_dir: directory where an output image is to be stored.
        """
        self.output_dir = output_dir

    MAX_IMG_WIDTH = 500
    DIST_BETWEEN_TEXT_AND_AUTHOR = 40
    MARGINS_SIZE = 10

    def make_meme(self, img_path: str, quote: QuoteModel, width=500) -> str:
        """Generate meme based on provided image and quote.

        @param img_path: Image on which the text will be placed.
        @param quote: Text placed on the image.
        @param width: Desired width of the image.
        @return: Path to the generated meme image.
        """
        meme_no = random.randint(0, 10000)
        output_path = self.output_dir + "/meme_" + str(meme_no) + ".jpg"

        # The image width cannot be larger than 'MAX_IMG_WIDTH'
        if width > self.MAX_IMG_WIDTH:
            width = self.MAX_IMG_WIDTH

        with Image.open(img_path) as img:
            img = proportional_resize(img, width)
            d = ImageDraw.Draw(img)
            pos_x, pos_y = self.get_random_text_pos(img, quote)
            d.text((pos_x, pos_y), quote.body, font=quote.font_quote, fill=(255, 255, 255))
            d.text((pos_x, pos_y + self.DIST_BETWEEN_TEXT_AND_AUTHOR), quote.author, font=quote.font_author, fill=(255, 255, 255))
            img.save(output_path)

        return output_path

    def get_random_text_pos(self, img: Image, quote: QuoteModel) -> (int, int):
        """Get random text position for the image, considering its size and margins.

        @param img: Image on which the text will be drawn.
        @param quote: Quote to be drawn.
        @return: Tuple of (x, y) position of the text.
        """
        # Experimentally chosen average width of one letter.
        width_of_a_letter = quote.font_size / 2
        max_text_len = max(len(quote.body), len(quote.author))

        width = img.size[0]
        height = img.size[1]
        text_size = int(max_text_len * width_of_a_letter)

        min_pos_x = self.MARGINS_SIZE
        min_pos_y = self.MARGINS_SIZE
        max_pos_x = width - min_pos_x - text_size
        max_pos_y = height - min_pos_y - self.DIST_BETWEEN_TEXT_AND_AUTHOR
        if max_pos_x < min_pos_x:
            max_pos_x = min_pos_x + 1
        if max_pos_y < min_pos_y:
            max_pos_y = min_pos_y + 1

        return random.randint(min_pos_x, max_pos_x), random.randint(min_pos_y, max_pos_y)


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
