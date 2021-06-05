"""Module providing the engine for memes generation."""
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

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
    FONT_SIZE = 25
    QUOTE_FONT = "./fonts/LilitaOne-Regular.ttf"
    AUTHOR_FONT = "./fonts/SansitaSwashed-Regular.ttf"
    FONT_COLOR = (255, 255, 255)

    _font_quote = ImageFont.truetype(QUOTE_FONT, FONT_SIZE)
    _font_author = ImageFont.truetype(AUTHOR_FONT, FONT_SIZE)

    def make_meme(self, img_path: str, text: str,
                  author: str, width=500) -> str:
        """Generate meme based on provided image and text.

        @param img_path: Image on which the text will be placed.
        @param text: Text placed on the image.
        @param author: Author of the citation, placed below the text.
        @param width: Desired width of the image.
        @return: Path to the generated meme image.
        """
        meme_no = random.randint(0, 10000)
        output_path = self.output_dir + "/meme_" + str(meme_no) + ".jpg"

        # The image width cannot be larger than 'MAX_IMG_WIDTH'
        if width > self.MAX_IMG_WIDTH:
            width = self.MAX_IMG_WIDTH

        wrapper = textwrap.TextWrapper(width=25)
        word_list = wrapper.wrap(text=text)
        caption_new = ''
        for ii in word_list[:-1]:
            caption_new = caption_new + ii + '\n'
        caption_new += word_list[-1]

        with Image.open(img_path) as img:
            img = proportional_resize(img, width)
            d = ImageDraw.Draw(img)
            pos = self.get_random_text_pos(img, text, author, len(word_list))
            d.text(pos, caption_new, font=self._font_quote, fill=self.FONT_COLOR)
            pos = pos[0], pos[1] + self.DIST_BETWEEN_TEXT_AND_AUTHOR * len(word_list)
            d.text(pos, author, font=self._font_author, fill=self.FONT_COLOR)
            img.save(output_path)

        return output_path

    def get_random_text_pos(self, img: Image, text: str,
                            author: str, no_body_lines: str) -> (int, int):
        """Get random text pos for the image, considering its size and margins.

        @param img: Image on which the text will be drawn.
        @param text: Body of the text to be drawn.
        @param author: Author of the text to be drawn.
        @param no_body_lines: Number of lines for a body text.
        @return: Tuple of (x, y) position of the text.
        """
        max_text_len = max(len(text), len(author))
        # Experimentally chosen average width of one letter.
        width_of_a_letter = self.FONT_SIZE / 2

        width = img.size[0]
        height = img.size[1]
        text_size = int(max_text_len * width_of_a_letter)

        min_pos_x = self.MARGINS_SIZE
        min_pos_y = self.MARGINS_SIZE
        max_pos_x = width - min_pos_x - text_size
        max_pos_y = height - min_pos_y - self.DIST_BETWEEN_TEXT_AND_AUTHOR*no_body_lines
        if max_pos_x < min_pos_x:
            max_pos_x = min_pos_x + 1
        if max_pos_y < min_pos_y:
            max_pos_y = min_pos_y + 1

        pos_x = random.randint(min_pos_x, max_pos_x)
        pos_y = random.randint(min_pos_y, max_pos_y)

        return pos_x, pos_y


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
