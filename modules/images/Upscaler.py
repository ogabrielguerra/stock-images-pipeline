import os
import shutil
import cv2
from modules.open_vino.OvUpscaler import OvUpscaler
from modules.images.ImageHelper import ImageHelper
from datetime import datetime
from modules.images.ImageHelper import AspectRatio
from PIL import Image
from modules.rich_theme.Theme import Theme

Image.MAX_IMAGE_PIXELS = None


class Upscaler:

    def __init__(self, configs: dict):
        Theme.header1('UPSCALING IMAGES')
        self.source_dir = configs.get('slices_dir')
        self.target_dir = configs.get('upload_dir')
        self.tmp_dir = configs.get('tmp_dir')
        superres_model_path = 'models/intel/single-image-super-resolution-1032/FP32/single-image-super-resolution-1032.xml'
        self.ovs = OvUpscaler(superres_model_path)

    def process_with_openvino_superres(self, image_path: str, output_path: str) -> None:
        self.ovs.runner(image_path, output_path)

    def scanner(self) -> bool:
        start_time = datetime.now()
        image_dirs = os.listdir(self.source_dir)

        if len(image_dirs) == 0:
            Theme.warning('No image dir to process.')
            return False

        for d in image_dirs:
            dir_path = os.path.join(self.source_dir, d)

            for f in os.listdir(dir_path):
                image_path = os.path.join(dir_path, f)
                image = cv2.imread(image_path)
                height = image.shape[0]
                width = image.shape[1]

                if ImageHelper.get_aspect_ratio(width, height) == '16:9':
                    Theme.info("Upscaling 16:9 image with OpenVino")
                    self.process_with_openvino_superres(image_path, self.target_dir)

                else:
                    Theme.info("Upscaling non 16:9 image with OpenVino")
                    # Create a placeholder image
                    pil_image = Image.open(image_path)
                    placeholder_image = AspectRatio.get_placeholder_image(pil_image)

                    # Create a tmp image
                    temp_image_path = os.path.join(self.tmp_dir, f)
                    placeholder_image.save(temp_image_path, 'JPEG')

                    # TODO: Pass OpenCV image to PIL avoiding saving a file
                    self.process_with_openvino_superres(temp_image_path, self.target_dir)

                    # Clean up temporary and close image
                    os.remove(temp_image_path)
                    pil_image.close()

                    # Open upscaled image and crop it
                    path = os.path.join(self.target_dir, f)
                    new_image = Image.open(path)
                    border_box = new_image.getbbox()
                    border_box = (border_box[0] + 25, border_box[1], border_box[2] - 25, border_box[3])
                    crop = new_image.crop(border_box)
                    crop.save(path)

                    # Close image
                    new_image.close()

            shutil.rmtree(dir_path)
            Theme.info("Source image removed.")

        Theme.success(f"Success upscaling images.\n Total time: {str(datetime.now() - start_time)}.")
        return True
