import string
from typing import Optional

from typing_extensions import Annotated
from pathlib import Path

import typer
from typer import rich_utils

ALPHABET = string.ascii_lowercase
ALPHABET_LEN = len(ALPHABET)

rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.COMMANDS_PANEL_TITLE = "[not dim]Commands"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_HELPTEXT = "not dim"

app = typer.Typer(
    name="Monoalphabetic Substitution Cipher",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
    epilog="Thanks for using this utility",
)

__all__ = ["app"]


def load_alphabet(alphabet_string: Optional[str] = None, alphabet_file: Optional[Path] = None) -> str:
    """
    Load the cipher alphabet.

    The cipher alphabet can be loaded either from a file or directly as a string in the command-line.

    :param alphabet_string: The alphabet, given directly as a string
    :param alphabet_file: The file containing the desired alphabet
    :return: The cipher alphabet
    """

    if alphabet_file and alphabet_string:
        raise typer.BadParameter("Can't specify both --alphabet and --alphabet-file")

    # If neither option is specified, assume the normal English alphabet is desired
    if not (alphabet_file or alphabet_string):
        return string.ascii_lowercase

    if alphabet_string:
        return alphabet_string

    try:
        return alphabet_file.read_text()
    except FileNotFoundError:
        raise typer.BadParameter(f"Alphabet file not found: {alphabet_file}")


def validate_alphabet(message: str, alphabet: str) -> None:
    """
    Ensure the given alphabet follows some rules.

    :param message: The message to test against
    :param alphabet: The cipher alphabet to test
    :return: None
    """

    if len(set(alphabet)) != len(alphabet):
        raise typer.BadParameter("The cipher alphabet contains duplicates")

    for c in message:
        if c not in alphabet:
            raise typer.BadParameter("The cipher alphabet doesn't cover all characters in the message")

    if alphabet == ALPHABET:
        print("The cipher alphabet is the same as the English alphabet. No actual encryption/ decryption will occur")


def ma_sub_cipher(message: str, cipher_alphabet: str, encrypting: bool) -> str:
    """
    Actually perform the encryption/ decryption

    :param message: The message to encrypt/ decrypt
    :param cipher_alphabet: The cipher alphabet to use
    :param encrypting: Whether we are encrypting/ decrypting
    :return: The enciphered message
    """

    # Create translation tables for the cipher
    if encrypting:
        translation_table = str.maketrans(ALPHABET, cipher_alphabet)
    else:
        translation_table = str.maketrans(cipher_alphabet, ALPHABET)

    # Translate the message using the translation table
    return message.translate(translation_table)


@app.command(
    short_help="Encrypt the given message using a monoalphabetic substitution cipher.",
    options_metavar="[--help] [-f FILE] | [-a STRING]",
    no_args_is_help=True,
)
def encrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    alphabet: Annotated[
        str, typer.Option(..., "--alphabet", "-a", show_default=False, rich_help_panel="Pick one of")
    ] = None,
    alphabet_file: Annotated[
        Path,
        typer.Option(
            "--alphabet-file", "-f", show_default=False, dir_okay=False, exists=True, rich_help_panel="Pick one of"
        ),
    ] = None,
):
    cipher_alphabet = load_alphabet(alphabet, alphabet_file)
    validate_alphabet(message, cipher_alphabet)
    print(ma_sub_cipher(message, cipher_alphabet, encrypting=True))


@app.command(
    short_help="Decrypt the given message using a monoalphabetic substitution cipher.",
    options_metavar="[--help]",
    no_args_is_help=True,
)
def decrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    alphabet: Annotated[
        str, typer.Option(..., "--alphabet", "-a", show_default=False, rich_help_panel="Pick one of")
    ] = None,
    alphabet_file: Annotated[
        Path,
        typer.Option(
            "--alphabet-file", "-f", show_default=False, dir_okay=False, exists=True, rich_help_panel="Pick one of"
        ),
    ] = None,
):
    cipher_alphabet = load_alphabet(alphabet, alphabet_file)
    validate_alphabet(message, cipher_alphabet)
    print(ma_sub_cipher(message, cipher_alphabet, encrypting=False))


if __name__ == "__main__":
    app()
