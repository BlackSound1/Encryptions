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


def _load_square(file: Path) -> list:
    """
    Loads the given Vigenere square file,
    removing the trailing newlines along the way.

    :param file: The file to open which contains a valid Vigenere square
    :return: The square as a list of alphabets
    """
    with open(file, "r") as f:
        return [line.rstrip("\n") for line in f]


def _same_length_key_and_message(key: str, message: str) -> str:
    """
    Since the message and key can both be any length, ensure the key is
    as long as the message.

    :param key: The key which will be used to encrypt/ decrypt
    :param message: The message to process
    :return: The key, perhaps altered to be the same length as the message
    """

    LEN_KEY = len(key)
    LEN_MESSAGE = len(message)

    # If the key is too long for the message, get only the first characters that will fit
    if LEN_KEY > LEN_MESSAGE:
        key = key[:LEN_MESSAGE]

    # If it's too long, repeat the key until it reaches the length of the message
    elif LEN_KEY < LEN_MESSAGE:
        div, mod = divmod(LEN_MESSAGE, LEN_KEY)

        key = key * div + key[:mod]

    return key


def _vigenere_cipher(message: str, key: str, square: list, encrypting: bool) -> str:
    """
    Actually perform the Vigenere cipher.

    :param message: The message to encrypt/ decrypt
    :param key: The secret key to encrypt/ decrypt with
    :param square: The Vigenere square to use as a lookup table
    :param encrypting: Whether we are encrypting or decrypting
    :return: The encrypted/ decrypted message
    """

    ALPHABET = ascii_lowercase

    to_return = ""

    # Iterate through the key and message at the same time
    for key_letter, message_letter in zip(key, message):
        # Find the alphabet that starts with the key letter
        for alpha in square:
            if alpha[0] == key_letter:
                if encrypting:
                    # Find where the message_letter is in the normal alphabet
                    normal_index = ALPHABET.find(message_letter)

                    # See where that location is in the found alphabet
                    to_return += alpha[normal_index]
                else:
                    # Find where the message_letter is in the cipher alphabet
                    cipher_index = alpha.find(message_letter)

                    # See where that location is in the normal alphabet
                    to_return += ALPHABET[cipher_index]
    return to_return


@app.command(
    short_help="Encrypt a given message using a Vigenere cipher and a key.",
    options_metavar="[--help]",
    no_args_is_help=True,
    help="""
    Encrypt a given message using a Vigenere cipher and a key.
    
    A Vigenere cipher uses a Vigenere square as a sort of lookup table. Supply the
    location of the square and an arbitrary key. These will be used
    together to scramble the message.
    
    Examples:
    >>> vigenere encrypt "diverttroopstoeastridge" "white" samples/vigenere_square
    >>> zpdxvpazhslzbhiwzbkmznm
    """,
)
def encrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    key: Annotated[str, typer.Argument(help="The key used in encryption", show_default=False)],
    square_file: Annotated[
        Path, typer.Argument(help="The file with the alphabet square", show_default=False)
    ],
) -> None:
    """
    Encrypt the message using a Vigenere cipher with a key.

    :param message: The message to encrypt
    :param key: The key to encrypt with
    :param square_file: The Path where the Vigenere square file is stored
    :return: None
    """
    square = _load_square(square_file)
    key = _same_length_key_and_message(key, message)
    print(_vigenere_cipher(message, key, square, encrypting=True))


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
    square_file: Annotated[
        Path, typer.Argument(help="The file with the alphabet square", show_default=False)
    ],
) -> None:
    """
    Decrypt the message using a Vigenere cipher with a key.

    :param message: The message to decrypt
    :param key: The key to decrypt with
    :param square_file: The Path where the Vigenere square file is stored
    :return: None
    """
    square = _load_square(square_file)
    key = _same_length_key_and_message(key, message)
    print(_vigenere_cipher(message, key, square, encrypting=False))


if __name__ == "__main__":
    app()
