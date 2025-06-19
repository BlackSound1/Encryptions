from pathlib import Path
from string import ascii_lowercase

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

ALPHABET = ascii_lowercase


def _load_square(file: Path) -> list:
    with open(file, "r") as f:
        return [line.rstrip("\n") for line in f]


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
    square = _load_square(alphabet_file)

    LEN_KEY = len(key)
    LEN_MESSAGE = len(message)

    # If the key is too long for the message, get only the first characters that will fit
    if LEN_KEY > LEN_MESSAGE:
        key = key[:LEN_MESSAGE]
    # If it's too long, repeat the key until it reaches the length of the message
    elif LEN_KEY < LEN_MESSAGE:
        div, mod = divmod(LEN_MESSAGE, LEN_KEY)

        key = key * div + key[:mod]

    encrypted = ""

    # Iterate through the key and message at the same time
    for key_letter, message_letter in zip(key, message):
        # Find the alphabet that starts with the key letter
        for alpha in square:
            if alpha[0] == key_letter:
                # Find where the message_letter is in the norma alphabet
                normal_index = ALPHABET.find(message_letter)

                # See where that location is in the found alphabet
                encrypted += alpha[normal_index]

    print(encrypted)


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
