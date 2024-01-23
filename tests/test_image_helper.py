import unittest
import os
from modules.images.ImageHelper import ImageHelper


class TestImageHelper(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.IMAGE_PNG = 'foo.png'
        self.IMAGE_JPG = 'foo.jpg'
        self.IMAGE = 'foo'
        self.IMAGE_FULL_PATH = 'tests/image_samples/square-turtle.png'
        self.TARGET_PATH = 'tests/tmp/small.jpg'

    def test_has_png_extendion(self):
        res = ImageHelper.has_png_extension(self.IMAGE_PNG)
        self.assertTrue(res)
        res = ImageHelper.has_png_extension(self.IMAGE_JPG)
        self.assertFalse(res)

    def test_has_jpg_extendion(self):
        res = ImageHelper.has_jpg_extension(self.IMAGE_PNG)
        self.assertFalse(res)
        res = ImageHelper.has_jpg_extension(self.IMAGE_JPG)
        self.assertTrue(res)

    def test_remove_extension(self):
        res = ImageHelper.remove_extension(self.IMAGE_PNG)
        self.assertEqual(res, self.IMAGE)

    def test_convert_image_format(self):
        ImageHelper.convert_image_format(self.IMAGE_FULL_PATH, self.TARGET_PATH)
        self.assertTrue(os.path.exists(self.TARGET_PATH))
        os.remove(self.TARGET_PATH)

