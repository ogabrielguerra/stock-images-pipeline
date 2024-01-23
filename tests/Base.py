import unittest
from tests.TestConfigs import App
import os


class Base(unittest.TestCase):
    configs = None
    IMAGE_JPG = None
    IMAGE_PNG = None
    IMAGE_SAMPLES_DIR = None

    @classmethod
    def setUpClass(self):
        app = App()

        self.configs = app.get_configs()
        test_vars = app.get_test_vars()

        self.IMAGE_PNG = test_vars.get('image_png')
        self.IMAGE_JPG = test_vars.get('image_jpg')
        self.IMAGE = test_vars.get('image')

        self.IMAGE_SAMPLES_DIR = test_vars.get('image_samples_dir')
        self.IMAGE_FULL_PATH = os.path.join(self.IMAGE_SAMPLES_DIR, self.IMAGE_PNG)

        self.TARGET_PATH = os.path.join(test_vars.get('tmp_dir'), self.IMAGE_JPG)
        self.SLICES_PATH = self.configs.get('slices_dir')
        self.UPLOAD_PATH = self.configs.get('upload_dir')
