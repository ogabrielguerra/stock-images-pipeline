import os
import cv2
from cv2 import dnn_superres
from datetime import datetime


class DnnUpscaler:
    def __init__(self, configs: dict):
        print('** UPSCALER')
        self.source_dir = configs.get('slices_dir')
        self.target_dir = configs.get('target_dir')

        self.model_path = 'models/EDSR_x2.pb'
        self.model_name = 'edsr'
        self.sr = dnn_superres.DnnSuperResImpl_create()

    def process(self, context_dir: str, image_name: str):
        start_time = datetime.now()

        image_source_path = os.path.join(self.source_dir, context_dir, image_name)
        image_final_path = os.path.join(self.target_dir, image_name)

        print('Reading image at ' + image_source_path)
        image = cv2.imread(image_source_path)
        self.sr.readModel(self.model_path)
        self.sr.setModel(self.model_name, 2)
        result = self.sr.upsample(image)

        try:
            print('Creating image at ' + image_source_path)
            cv2.imwrite(image_final_path, result)
        except Exception:
            print(Exception)

        print('Upscale finished ' + str(datetime.now() - start_time))
