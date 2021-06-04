"""Module providing the engine for memes generation."""
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Class for generating memes."""

    def __init__(self, output_dir):
        """Initialize an object.

        @param output_dir: directory where an output image is to be stored.
        """
        self.output_dir = output_dir

    MAX_IMG_WIDTH = 500

    def make_meme(self, img_path: str, text: str, author: str, width=500) -> str:
        """Generate meme based on provided image and text.

        @param img_path: Image on which the text will be placed.
        @param text: Text placed on the image.
        @param author: Author of the citation, placed below the text.
        @param width: Desired width of the image.
        @return: Path to the generated meme image.
        """
        output_path = self.output_dir + "/meme.jpg"

        #The image width cannot be larger than 'MAX_IMG_WIDTH'
        if width > self.MAX_IMG_WIDTH:
            width = self.MAX_IMG_WIDTH

        with Image.open(img_path) as img:
            img = proportional_resize(img, width)
            fnt = ImageFont.truetype("./fonts/LilitaOne-Regular.ttf", 30)
            d = ImageDraw.Draw(img)
            d.text((10, 60), text, font=fnt, fill=(255, 255, 255))
            d.text((10, 100), author, font=fnt, fill=(255, 255, 255))
            img.save(output_path)

        return output_path


def proportional_resize(img: Image, width: int):
    """Resize the image proportionally, based on desired width.

    @param img: Image to be resized.
    @param width: Desired width.
    @return: Resized image.
    """
    percent = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(percent)))
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

