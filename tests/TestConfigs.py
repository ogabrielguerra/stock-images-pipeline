import os


class App:
    def __init__(self):

        self.test_vars = {
            'image_png': 'square-turtle.png',
            'image_jpg': 'square-turtle.jpg',
            'image': 'square-turtle',
            'image_samples_dir': 'tests/image_samples',
            'tmp_dir': 'tests/jobs/tmp',
            'target_path': 'tests/tmp/small.jpg',
        }

        services = {
            'dreamstime': {
                'is_sftp': False,
                'ftp_host': os.getenv('DREAMSTIME_FTP_HOST'),
                'ftp_username': os.getenv('DREAMSTIME_FTP_USERNAME'),
                'ftp_password': os.getenv('DREAMSTIME_FTP_PASSWORD'),
            },
            'depositphotos': {
                'is_sftp': False,
                'ftp_host': os.getenv('DEPOSITPHOTOS_FTP_HOST'),
                'ftp_username': os.getenv('DEPOSITPHOTOS_FTP_USERNAME'),
                'ftp_password': os.getenv('DEPOSITPHOTOS_FTP_PASSWORD'),
            },
            # 'shutterstock': {
            #     'is_sftp': True,
            #     'ftp_host': os.getenv('SHUTTERSTOCK_FTP_HOST'),
            #     'ftp_username': os.getenv('SHUTTERSTOCK_FTP_USERNAME'),
            #     'ftp_password': os.getenv('SHUTTERSTOCK_FTP_PASSWORD'),
            # },
            'adobe': {
                'is_sftp': True,
                'ftp_host': os.getenv('ADOBE_FTP_HOST'),
                'ftp_username': os.getenv('ADOBE_FTP_USERNAME'),
                'ftp_password': os.getenv('ADOBE_FTP_PASSWORD'),
            }
        }

        self.configs = {
            'slices_dir': 'tests/jobs/slices',
            'input_dir': 'tests/jobs/input',
            'target_dir': 'tests/jobs/upscale',
            'metadata_dir': 'tests/jobs/metadata',
            'upload_dir': 'tests/jobs/upload',
            'tmp_dir': 'tests/jobs/tmp',
            'services': services
        }

    def get_configs(self):
        return self.configs

    def get_test_vars(self):
        return self.test_vars
