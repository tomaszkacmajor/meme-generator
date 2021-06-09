import os
import unittest
from parameterized import parameterized
from PIL import Image
from MemeEngine.meme_engine import proportional_resize, MemeEngine, get_wrapped_text
from QuoteEngine import QuoteModel

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MemeEngineTests(unittest.TestCase):

    @parameterized.expand([
        [500, 500, 250, 250],
        [500, 251, 250, 125],
        [200, 200, 200, 200],
    ])
    def test_image_proportional_resize(self, width, height, new_width, new_height):
        img = Image.new(mode="RGB", size=(width, height))
        img = proportional_resize(img, new_width)
        self.assertEqual(img.size, (new_width, new_height))

    @parameterized.expand([
        ["Test body text", "Author 1", 25, 175],
        ["body text", "Author longer than body", 22.5, 258],
    ])
    def test_get_max_text_width(self, body, author, font_size, expected):
        meme_engine = MemeEngine("")
        meme_engine.FONT_SIZE = font_size
        quote = QuoteModel(body, author)
        result = meme_engine.get_max_text_width(quote)
        self.assertEqual(expected, result)

    @parameterized.expand([
        ["Test body text which is too long for one line", 25, "Test body text which is\ntoo long for one line", 2],
        ["Test body text which is too long for one line", 10, "Test body\ntext which\nis too\nlong for\none line", 5],
        ["Test body text", 25, "Test body text", 1]
    ])
    def test_get_wrapped_text(self, text, max_width, expected_wrapped_text, expected_no_lines):
        wrapped_text, no_lines = get_wrapped_text(text, max_width)
        self.assertEqual(wrapped_text, expected_wrapped_text)
        self.assertEqual(no_lines, expected_no_lines)

if __name__ == '__main__':
    unittest.main()
