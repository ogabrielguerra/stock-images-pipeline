from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel


class Theme:
    @staticmethod
    def app_header():
        console = Console()
        text = "IMAGE PIPELINE"
        text = Padding(text, 1)
        console.print(text, style="black on white bold")

    @staticmethod
    def header1(string: str):
        console = Console()
        text = Padding(f"{string}", (2, 0, 1, 1))
        console.print(text, style="yellow bold")
        # console.print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))

    @staticmethod
    def header2(string: str):
        console = Console()
        text = Padding(f"{string}", (1, 0, 0, 1))
        console.print(text, style="yellow3 bold")

    @staticmethod
    def info(string: str):
        console = Console()
        text = Padding(f"{string}", (0, 0, 0, 1))
        console.print(text, style="slate_blue3 italic")

    @staticmethod
    def warning(string: str):
        console = Console()
        text = Padding(f"{string}", (0, 0, 0, 1))
        console.print(text, style="indian_red")

    @staticmethod
    def error(string: str):
        console = Console()
        text = Padding(f"{string}", (0, 0, 0, 1))
        console.print(text, style="white on dark_orange3")

    @staticmethod
    def success(string: str):
        console = Console()
        text = Padding(f"{string}", (1, 0, 1, 1))
        console.print(text, style="sea_green3 bold")


    @staticmethod
    def tip(string: str):
        console = Console()
        text = Padding(f"{string}", (1, 1, 1, 1))
        console.print(text, style="white on purple4 bold")
