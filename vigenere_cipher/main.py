from pathlib import Path

from typing_extensions import Annotated

import typer
from typer import rich_utils

rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.COMMANDS_PANEL_TITLE = "[not dim]Commands"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_HELPTEXT = "not dim"

app = typer.Typer(
    name="Vigenere Cipher",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
    epilog="Thanks for using this utility",
    help="""
    Hey
    """,
)

__all__ = ["app"]


def _load_alphabet(file: Path) -> dict:
    pass


@app.command(
    short_help="Encrypt a given message using a Vigenere cipher and a key.",
    options_metavar="[--help]",
    no_args_is_help=True,
    help="""
    """,
)
def encrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    key: Annotated[str, typer.Argument(help="The key used in encryption", show_default=False)],
    alphabet_file: Annotated[
        Path, typer.Argument(help="The file with the alphabet square", show_default=False)
    ],
) -> None:
    pass


@app.command(
    short_help="Decrypt a given message using a Vigenere cipher and a key.",
    options_metavar="[--help]",
    no_args_is_help=True,
    help="""
    """,
)
def decrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    key: Annotated[str, typer.Argument(help="The key used in encryption", show_default=False)],
    alphabet_file: Annotated[
        Path, typer.Argument(help="The file with the alphabet square", show_default=False)
    ],
) -> None:
    pass


if __name__ == "__main__":
    app()
