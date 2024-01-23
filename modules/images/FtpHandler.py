import os
import paramiko
import shutil
from ftplib import FTP
from modules.rich_theme.Theme import Theme


class FtpHandler:

    def __init__(self, configs) -> None:
        Theme.header1('UPLOADING IMAGES')
        self.services = configs.get('services')
        self.upload_files_dir = 'jobs/upload/'

    def get_ftp_connection(self, stock_service):
        service = self.services.get(stock_service)
        ftp = FTP(service.get('ftp_host'))
        ftp.login(
            user=service.get('ftp_username'),
            passwd=service.get('ftp_password')
        )
        return ftp

    def get_sftp_connection(self, stock_service):
        service = self.services.get(stock_service)
        host, port = service.get('ftp_host'), 22
        transport = paramiko.Transport((host, port))
        username, password = service.get('ftp_username'), service.get('ftp_password')
        transport.connect(None, username, password)
        return transport

    def send_through_ftp(self, service):
        Theme.header2(f"Sending images to {service}")

        ftp = self.get_ftp_connection(service)

        for f in os.listdir(self.upload_files_dir):
            Theme.info(f"Uploading file {f}")
            try:
                ftp.storbinary('STOR ' + f, open(self.upload_files_dir + f, 'rb'))
            except Exception:
                print('Error uploading file ' + f)
        ftp.quit()

    def send_through_sftp(self, service):
        Theme.header2(f"Sending images to {service}")

        transport = self.get_sftp_connection(service)
        sftp = paramiko.SFTPClient.from_transport(transport)

        for f in os.listdir(self.upload_files_dir):
            Theme.info(f"Uploading file {f}")
            local_path = os.path.join(self.upload_files_dir, f)

            try:
                sftp.put(local_path, f)
                shutil.move(local_path, 'jobs/publishing-logs')
            except Exception as e:
                Theme.info(f"Error Uploading file {f}.\n{e}")

        if sftp:
            sftp.close()
        if transport:
            transport.close()

    def send_files(self):
        image_dirs = os.listdir(self.upload_files_dir)
        if len(image_dirs) == 0:
            Theme.warning('No images to upload.')
            return False

        for service in self.services:
            service_obj = self.services.get(service)

            if service_obj.get('is_sftp'):
                self.send_through_sftp(service)
            else:
                self.send_through_ftp(service)

        Theme.success(f"Success uploading images.")