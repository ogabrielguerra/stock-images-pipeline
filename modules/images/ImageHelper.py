import math
from PIL import Image


class ImageHelper:

    @staticmethod
    def get_aspect_ratio(width: int, height: int) -> str:
        if width > height:
            if width % 16 == 0 and height % 9 == 0:
                return '16:9'
            elif width % 7 == 0 and height % 4 == 0:
                return '7:4'
            elif width % 4 == 0 and height % 3 == 0:
                return '4:3'
        else:
            if width % 9 == 0 and height % 16 == 0:
                return '9:16'
            elif width % 3 == 0 and height % 4 == 0:
                return '3:4'

        return 'Undefined'

    @staticmethod
    def get_extension(image_name: str) -> str:
        image_name_parts = image_name.split('.')
        return image_name_parts[len(image_name_parts) - 1]

    @staticmethod
    def has_png_extension(image_name: str) -> bool:
        image_name_parts = image_name.split('.')
        extension = image_name_parts[len(image_name_parts) - 1]
        if extension == 'png':
            return True
        return False

    @staticmethod
    def has_jpg_extension(image_name: str) -> bool:
        image_name_parts = image_name.split('.')
        extension = image_name_parts[len(image_name_parts) - 1]
        return extension == 'jpg'

    @staticmethod
    def remove_extension(image_name: str) -> str:
        image_name_parts = image_name.split('.')
        return '.'.join(image_name_parts[:len(image_name_parts) - 1])

    # TODO: Implement multi format support
    @staticmethod
    def convert_image_format(image_full_path: str, target_path: str) -> None:
        im1 = Image.open(image_full_path)
        separator = '.'
        image_parts = target_path.split(separator)
        image_parts.pop(len(image_parts) - 1)

        new_target_image = separator.join(image_parts) + '.jpg'

        print('Converting new image to ' + new_target_image)
        im1.save(new_target_image)


class AspectRatio:

    @staticmethod
    def get_next_height(height) -> int:
        """
        Get the next height in 16:9. Needs refinement
        """
        if height % 1080 == 0:
            return height
        elif height < 1080:
            return 1080
        else:
            return (height // 1080 + 1) * 1080

    @staticmethod
    def get_proportional_width_from_height(original_height, original_width) -> int:
        """
        Get the proportional width of an image given the original height
        """
        height = AspectRatio.get_next_height(original_height)
        return math.floor((original_width * height) / original_height)

    @staticmethod
    def get_16_9_width_from_height(height) -> int:
        """
        Get the width a image has to have in 16:9 format given the original height
        """
        return math.floor(height * 1.77777)

    @staticmethod
    def get_placeholder_image(image: Image) -> Image:
        """
        Create a placeholder and paste the image to be upscaled and then cropped.
        """
        # Get original image dimensions

        image_size = image.size
        image_width = image_size[0]
        image_height = image_size[1]

        # Get next height proportional to 16:9 aspect
        new_height = AspectRatio.get_next_height(image_height)
        # Get proportional width, considering original widht x height aspect ratio
        new_width = AspectRatio.get_proportional_width_from_height(image_height, image_width)

        # Create a new image as placeholder
        placeholder_width = AspectRatio.get_16_9_width_from_height(new_height)
        placeholder_image = Image.new('RGB', (placeholder_width, new_height), (0, 0, 0))

        # Resize as new image using the new dimensions
        resized_image = image.resize((new_width, new_height))
        resized_image_size = resized_image.size
        resized_image_width = resized_image_size[0]

        # Get x position for pasting the resized image in the center of placeholder image
        x = math.floor((placeholder_width - resized_image_width) / 2)

        placeholder_image.paste(resized_image, (x, 0))
        return placeholder_image
