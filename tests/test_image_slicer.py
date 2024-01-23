import os
import shutil
from modules.images.ImageSlicer import ImageSlicer
from tests.Base import Base


class TestImageSlicer(Base):

    def test_extract_quadrants(self):
        input_target = os.path.join('tests/jobs/input', self.IMAGE_PNG)
        shutil.copy(self.IMAGE_FULL_PATH, input_target)

        image_slicer = ImageSlicer(self.configs)
        image_slicer.extract_quadrants(self.IMAGE_PNG)
        self.assertTrue(os.path.isdir(self.SLICES_PATH))

        images_list = os.listdir(os.path.join(self.SLICES_PATH, self.IMAGE))
        self.assertEqual(len(images_list), 4)

        shutil.rmtree(os.path.join(self.SLICES_PATH, self.IMAGE))
        os.remove(input_target)
