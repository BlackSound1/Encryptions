import string
from typing_extensions import Annotated

import typer
from typer import rich_utils

ALPHABET = string.ascii_lowercase
ALPHABET_LEN = len(ALPHABET)

rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.COMMANDS_PANEL_TITLE = "[not dim]Commands"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_HELPTEXT = "not dim"

app = typer.Typer(
    name="Caesar Cipher",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
    epilog="Thanks for using this utility",
    help="""
    Uses a Caesar cipher to encrypt/ decrypt a message, with an arbitrary offset.

    Examples:
    >>> caesar encrypt "hello world" 3
    >>> khoor zruog
    >>> caesar decrypt "khoor zruog" 3
    >>> hello world
    """,
)

__all__ = ["app"]


def _caesar_cipher(message: str, offset: int, encrypting: bool) -> str:
    """
    Actually perform the Caesar cipher.

    :param message: The given message
    :param offset: The offset to use in encryption/ decryption
    :param encrypting: Whether we are encrypting or decrypting
    :return: The message, as processed by the Caesar cipher
    """

    if not message:
        return ""

    # Make sure offset is always within length of alphabet
    offset %= ALPHABET_LEN

    # If decrypting, reverse offset
    if not encrypting:
        offset = -offset

    result = []

    for char in message:

        # Leave non-alphanumeric characters alone
        if not char.isalpha():
            result.append(char)
        else:
            alphabet_index = ALPHABET.find(char)
            if alphabet_index == -1:
                continue

            # Apply shift and wrap-around (if needed)
            new_alphabet_index = (alphabet_index + offset) % ALPHABET_LEN
            new_char = ALPHABET[new_alphabet_index]

            # Restore original case
            result.append(new_char)

    return "".join(result)


@app.command(
    short_help="Encrypt the given message using a Caesar cipher.",
    options_metavar="[--help]",
    no_args_is_help=True,
    help="""
    Encrypt the given message using a Caesar cipher.

    Caesar ciphers require an offset to be specified. This is the value to shift the
    alphabet by when encrypting/ decrypting.

    Example:
    >>> caesar encrypt "hello world" 3
    >>> khoor zruog
    """,
)
def encrypt(
    message: Annotated[str, typer.Argument(help="The message to encrypt", show_default=False)],
    offset: Annotated[int, typer.Argument(help="Set the offset to use", show_default=False)],
) -> None:
    """
    Encrypt the given message using a Caesar cipher.

    :param message: The message to encrypt
    :param offset: The offset to use in the cipher. For decryption, use the same offset
    :return: None
    """
    print(_caesar_cipher(message, offset, encrypting=True))


@app.command(
    short_help="Decrypt the given message using a Caesar cipher.",
    options_metavar="[--help]",
    no_args_is_help=True,
    help="""
    Decrypt the given message using a Caesar cipher.

    Caesar ciphers require an offset to be specified. This is the value to shift the
    alphabet by when encrypting/ decrypting.

    The offset must be same as what was used to encrypt the message,
    or else the result won't make sense.

    Example:
    >>> caesar decrypt "khoor zruog" 3
    >>> hello world
    """,
)
def decrypt(
    message: Annotated[str, typer.Argument(help="The message to decrypt", show_default=False)],
    offset: Annotated[int, typer.Argument(help="Set the offset to use", show_default=False)],
) -> None:
    """
    Decrypt the given message using a Caesar cipher.

    :param message: The message to decrypt
    :param offset: The offset to use in decrypting the ciphertext.
    Must be the same as the offset used to encrypt, or else the message won't make sense.
    :return: None
    """
    print(_caesar_cipher(message, offset, encrypting=False))


if __name__ == "__main__":
    app()
