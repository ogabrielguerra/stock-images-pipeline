import os
from PIL import Image
from modules.open_vino.OvUpscaler import OvUpscaler
from modules.images.ImageHelper import AspectRatio


def run():
    image = Image.open('sample3.png')

    # Create a placeholder image
    placeholder_image = AspectRatio.get_placeholder_image(image)
    merged_image_path = 'merged_image.jpg'
    placeholder_image.save(merged_image_path, 'JPEG')

    # Upscale the full image
    superres_model_path = 'models/intel/single-image-super-resolution-1032/FP32/single-image-super-resolution-1032.xml'
    ovs = OvUpscaler(superres_model_path)
    ovs.runner(merged_image_path, 'output')

    # Crop black area
    upscaled_image = Image.open(os.path.join('output', merged_image_path))
    border_box = upscaled_image.getbbox()
    new_border_box = (border_box[0] + 25, border_box[1], border_box[2] - 25, border_box[3])
    crop = upscaled_image.crop(new_border_box)
    crop.save('output/cropped_upscale.jpg')


# im = Image.open('foo-border.jpg')
# print(im.getbbox())
# im = im.convert('RGB')
# print(im.getbbox())

run()
