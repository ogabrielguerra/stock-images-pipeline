import os
import shutil
from modules.images.Upscaler import Upscaler
from modules.images.ImageSlicer import ImageSlicer
from tests.Base import Base


class TestUpscaler(Base):

    def prepare(self):
        input_target = os.path.join('tests/jobs/input', self.IMAGE_PNG)
        shutil.copy(self.IMAGE_FULL_PATH, input_target)
        image_slicer = ImageSlicer(self.configs)
        image_slicer.extract_quadrants(self.IMAGE_PNG)

    # TODO: test upscaler with a smaller image size to save resources
    # TODO: test upscaler with 16:9, non 16:9 and square images
    # TODO: test upscaler with the fallback model DnnUpscaler
    def test_upscale(self):
        self.prepare()
        upscaler = Upscaler(self.configs)
        upscaler.scanner()

        slices_list = os.listdir(self.SLICES_PATH)
        self.assertEqual(len(slices_list), 0)

        images_list = os.listdir(self.UPLOAD_PATH)
        self.assertEqual(len(images_list), 4)

        for f in images_list:
            os.remove(os.path.join(self.UPLOAD_PATH, f))


