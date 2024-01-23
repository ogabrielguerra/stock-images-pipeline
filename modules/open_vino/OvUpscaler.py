import os
import time
from pathlib import Path

import cv2
import numpy as np
from openvino.runtime import Core


class OvUpscaler:
    """
    This Class is based on OpenVino's Super Resolution model example.
    """

    def __init__(self, model_path) -> None:
        self.DEVICE = "CPU"
        self.CROPLINES = 1
        self.CROP_FACTOR = 1
        self.model_name = os.path.basename(model_path)
        self.model_xml_path = Path(model_path)

    @staticmethod
    def convert_result_to_image(result) -> np.ndarray:
        result = result.squeeze(0).transpose(1, 2, 0)
        result *= 255
        result[result < 0] = 0
        result[result > 255] = 255
        result = result.astype(np.uint8)
        return result

    def runner(self, image_path, output_path):
        ie = Core()
        model = ie.read_model(model=self.model_xml_path)
        compiled_model = ie.compile_model(model=model, device_name=self.DEVICE)

        original_image_key, bicubic_image_key = compiled_model.inputs
        output_key = compiled_model.output(0)

        input_height, input_width = list(original_image_key.shape)[2:]
        target_height, target_width = list(bicubic_image_key.shape)[2:]
        upsample_factor = int(target_height / input_height)

        full_image = cv2.imread(str(image_path))
        full_image_height, full_image_width = full_image.shape[:2]

        x_coords = list(range(0, full_image_width, input_width * self.CROP_FACTOR - self.CROPLINES * 2))

        while full_image_width - x_coords[-1] < input_width * self.CROP_FACTOR:
            x_coords.pop(-1)

        y_coords = list(range(0, full_image_height, input_height * self.CROP_FACTOR - self.CROPLINES * 2))

        while full_image_height - y_coords[-1] < input_height * self.CROP_FACTOR:
            y_coords.pop(-1)

        crop_width = x_coords[-1] + input_width * self.CROP_FACTOR
        crop_height = y_coords[-1] + input_height * self.CROP_FACTOR

        new_width = (
                x_coords[-1] * (upsample_factor // self.CROP_FACTOR)
                + target_width
                - self.CROPLINES * 2 * (upsample_factor // self.CROP_FACTOR)
        )
        new_height = (
                y_coords[-1] * (upsample_factor // self.CROP_FACTOR)
                + target_height
                - self.CROPLINES * 2 * (upsample_factor // self.CROP_FACTOR)
        )

        patch_nr = 0

        full_image_crop = full_image.copy()[:crop_height, :crop_width, :]
        full_superresolution_image = np.empty((new_height, new_width, 3), dtype=np.uint8)

        total_inference_duration = 0

        for y in y_coords:
            for x in x_coords:
                patch_nr += 1

                image_crop = full_image_crop[
                             y: y + input_height * self.CROP_FACTOR,
                             x: x + input_width * self.CROP_FACTOR,
                             ]

                bicubic_image = cv2.resize(
                    src=image_crop,
                    dsize=(target_width, target_height),
                    interpolation=cv2.INTER_CUBIC,
                )

                if self.CROP_FACTOR > 1:
                    image_crop = cv2.resize(src=image_crop, dsize=(input_width, input_height))

                input_image_original = np.expand_dims(image_crop.transpose(2, 0, 1), axis=0)
                input_image_bicubic = np.expand_dims(bicubic_image.transpose(2, 0, 1), axis=0)

                inference_start_time = time.perf_counter()

                result = compiled_model(
                    {
                        original_image_key.any_name: input_image_original,
                        bicubic_image_key.any_name: input_image_bicubic,
                    }
                )[output_key]

                inference_stop_time = time.perf_counter()
                inference_duration = inference_stop_time - inference_start_time
                total_inference_duration += inference_duration

                result_image = self.convert_result_to_image(result)

                adjusted_upsample_factor = upsample_factor // self.CROP_FACTOR
                new_y = y * adjusted_upsample_factor
                new_x = x * adjusted_upsample_factor

                full_superresolution_image[
                new_y: new_y + target_height - self.CROPLINES * adjusted_upsample_factor * 2,
                new_x: new_x + target_width - self.CROPLINES * adjusted_upsample_factor * 2,
                ] = result_image[
                    self.CROPLINES * adjusted_upsample_factor: -self.CROPLINES * adjusted_upsample_factor,
                    self.CROPLINES * adjusted_upsample_factor: -self.CROPLINES * adjusted_upsample_factor,
                    :,
                    ]

        if image_path.find('/'):
            image_name = str(image_path).split('/')[-1]
        else:
            image_name = str(image_path).split('.')[-1]

        final_image_path = os.path.join(output_path, image_name)
        cv2.imwrite(final_image_path, full_superresolution_image)
