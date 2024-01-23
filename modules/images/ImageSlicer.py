import cv2
import os
from pathlib import Path
from modules.rich_theme.Theme import Theme


class ImageSlicer:
    def __init__(self, configs) -> None:
        Theme.header1('SLICING IMAGES')
        self.input_dir = configs.get('input_dir')
        self.slices_dir = configs.get('slices_dir')

    def extract_quadrants(self, image_source) -> bool:
        Theme.info(f"Extracting quadrants from  dir {image_source}.")

        image_source_path = os.path.join(self.input_dir, image_source)
        img = cv2.imread(image_source_path)
        h, w, channels = img.shape

        quadrants = [
            img[:h // 2, :w // 2],
            img[:h // 2, w // 2:],
            img[h // 2:, :w // 2],
            img[h // 2:, w // 2:]
        ]

        image_name = Path(image_source).stem

        sliced_image_full_path = os.path.join(self.slices_dir, image_name)

        if not os.path.isdir(sliced_image_full_path):
            Theme.info(f"Creating dir {sliced_image_full_path}.")
            os.mkdir(sliced_image_full_path)
        else:
            Theme.info(f"Skipping dir creation. {sliced_image_full_path} already exists.")

        for i in range(0, 4):
            sliced_image_name = 'q' + str(i + 1) + '_' + image_name + '.jpg'
            sliced_image_full_path = os.path.join(self.slices_dir, image_name, sliced_image_name)
            cv2.imwrite(sliced_image_full_path, quadrants[i])

        Theme.success(f"Success extracting quadrants from image!")
        return True

    def scanner(self) -> bool:
        files = os.listdir(self.input_dir)
        if len(files) == 0:
            Theme.warning('No image to process.')
            return False

        for f in files:
            self.extract_quadrants(f)
            os.remove(os.path.join(self.input_dir, f))
        return True
