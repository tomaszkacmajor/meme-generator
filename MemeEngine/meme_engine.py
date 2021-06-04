""""""
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """"""

    def __init__(self, output_dir):
        """Initialize an object.

        @param output_dir:
        """
        self.output_dir = output_dir

    MAX_WIDTH = 500

    def make_meme(self, img_path: str, text: str, author: str, width=500) -> str:
        """

        @param img_path:
        @param text:
        @param author:
        @param width:
        @return:
        """
        output_path = self.output_dir + "/meme.jpg"
        if width > self.MAX_WIDTH:
            width = self.MAX_WIDTH

        with Image.open(img_path) as img:
            percent = (width / float(img.size[0]))
            height = int((float(img.size[1]) * float(percent)))
            img = img.resize((width, height), Image.ANTIALIAS)

            fnt = ImageFont.truetype("./fonts/LilitaOne-Regular.ttf", 40)
            d = ImageDraw.Draw(img)
            d.text((10, 60), text, font=fnt, fill=(255, 255, 255))
            d.text((10, 100), author, font=fnt, fill=(255, 255, 255))
            img.save(output_path)

        return output_path
