import typer
from modules.images.ImageSlicer import ImageSlicer
from modules.images.Upscaler import Upscaler
from modules.images.ImageTagger import ImageTagger
from modules.images.FtpHandler import FtpHandler
from modules.rich_theme.Theme import Theme
from dotenv import load_dotenv
from App import App

cli = typer.Typer()
load_dotenv()
app = App()
configs = app.get_configs()


@cli.command()
def slice():
    # Split the image into 4 pieces
    q = ImageSlicer(configs)
    q.scanner()


@cli.command()
def upscale():
    # Upscale each image
    u = Upscaler(configs)
    u.scanner()


@cli.command()
def tag():
    # Get tags for each image
    it = ImageTagger(configs)
    it.scanner()


@cli.command()
def upload():
    # Send files to stock
    ftp = FtpHandler(configs)
    ftp.send_files()


@cli.command()
def read_tags():
    it = ImageTagger(configs)
    it.read_tags()


@cli.command()
def process():
    Theme.app_header()
    slice()
    upscale()
    tag()


@cli.command()
def alljobs():
    slice()
    upscale()
    tag()
    upload()


if __name__ == "__main__":
    cli()
