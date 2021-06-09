import os
import unittest
from parameterized import parameterized
from PIL import Image
from MemeEngine.meme_engine import proportional_resize

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


if __name__ == '__main__':
    unittest.main()
