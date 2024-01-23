import os


class App:
    def __init__(self):
        self.configs = {
            'slices_dir': 'jobs/slices',
            'input_dir': 'jobs/input',
            'target_dir': 'jobs/upscale',
            'metadata_dir': 'jobs/metadata',
            'upload_dir': 'jobs/upload',
            'tmp_dir': 'jobs/tmp',
            'services': {
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
        }

    def get_configs(self):
        return self.configs
