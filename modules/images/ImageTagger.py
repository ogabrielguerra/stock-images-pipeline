import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from iptcinfo3 import IPTCInfo
from modules.images.ImageHelper import ImageHelper
from modules.rich_theme.Theme import Theme


class ImageTagger:
    def __init__(self, configs) -> None:
        Theme.header1('RETRIEVING METADATA')
        load_dotenv()
        self.api_key = os.getenv('IMAGGA_API_KEY')
        self.api_secret = os.getenv('IMAGGA_API_SECRET')
        self.metadata_dir = configs.get('metadata_dir')
        self.upload_dir = configs.get('upload_dir')

    def get_tags(self, image_source):
        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(self.api_key, self.api_secret),
            files={'image': open(image_source, 'rb')})
        return response.json()

    @staticmethod
    def remove_qn_from_string(q_string):
        if (q_string[0:3] == 'q1_' or
                q_string[0:3] == 'q2_' or
                q_string[0:3] == 'q3_' or
                q_string[0:3] == 'q4_'):

            separator = '_'
            image_name = q_string.split(separator)
            image_name.pop(0)
            return separator.join(image_name)
        else:
            print('String * ' + q_string + ' * doesn\'t have a qn starting. Not a slice?')
            return q_string

    @staticmethod
    def save_tags_as_json(response_json, json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)

    @staticmethod
    def json_tags_to_list(json_file_path):
        with open(json_file_path) as json_file:
            data = json.load(json_file)

        tags = data['result']['tags']
        tags_list = []

        for t in tags:
            tags_list.append(t['tag']['en'])

        return tags_list[0:40]

    @staticmethod
    def get_title_from_filename(filename: str):
        image_name = ImageHelper.remove_extension(filename)
        image_name = image_name.replace('Gabriel_Guerra', '')
        name_parts = image_name.split('_')
        name_parts.pop(0)
        name_parts.pop(0)
        name_parts.pop(len(name_parts) - 1)
        title = " ".join(name_parts)
        return title

    def embed_tags(self):

        image_dirs = os.listdir(self.upload_dir)

        if len(image_dirs) == 0:
            print('ImageTags: no image dir to process.')
            return False

        for f in image_dirs:
            image_to_embed_path = os.path.join(self.upload_dir, f)
            json_file_name = ImageHelper.remove_extension(f) + '.json'
            json_file_path = os.path.join(self.metadata_dir, json_file_name)
            tags_list = self.json_tags_to_list(json_file_path)

            # Start embedding tags
            # TODO: Append tags instead of assign
            # TODO: Check if tag exist before
            if os.path.exists(image_to_embed_path):
                Theme.info(f"Embedding tags to {image_to_embed_path}.")
                title = self.get_title_from_filename(json_file_name)
                description = title + ' ' + ' '.join(tags_list)
                info = IPTCInfo(image_to_embed_path)
                info['keywords'] = tags_list
                info['headline'] = title
                info['caption/abstract'] = description
                info.save_as(image_to_embed_path + '_tmp')
                os.remove(image_to_embed_path)
                os.rename(image_to_embed_path + '_tmp', image_to_embed_path)

    def scanner(self):
        start_time = datetime.now()
        image_dirs = os.listdir(self.upload_dir)

        if len(image_dirs) == 0:
            Theme.warning(f"ImageTags: no image dir to process.")
            return False

        for f in image_dirs:
            image_path = os.path.join(self.upload_dir, f)
            image_name = f
            json_file_name = ImageHelper.remove_extension(image_name) + '.json'
            json_file_path = os.path.join(self.metadata_dir, json_file_name)

            if not os.path.exists(json_file_path):
                Theme.info(f"Getting tags for image {f}.")
                response = self.get_tags(image_path)
                self.save_tags_as_json(response, json_file_path)
            else:
                Theme.info(f"Skipping. Tags already stored for {f}.")

        self.embed_tags()

        Theme.success(f"Success saving tags.\nTagging process total time: {str(datetime.now() - start_time)}.")
        Theme.tip("Images ready for upload")

    def read_tags(self):
        image_dirs = os.listdir(self.upload_dir)

        if len(image_dirs) == 0:
            print('ImageTags: no image dir to process.')
            return False

        for f in image_dirs:
            image_path = os.path.join(self.upload_dir, f)
            info = IPTCInfo(image_path)
            print(info['keywords'])
