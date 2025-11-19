import typer
from typer import rich_utils

from caesar_cipher.main import app as caesar
from ma_sub_cipher.main import app as ma
from vigenere_cipher.main import app as vigenere

rich_utils.COMMANDS_PANEL_TITLE = "[not dim]Ciphers"
rich_utils.STYLE_HELPTEXT = "not dim"

app = typer.Typer(
    name="Encryptions App",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
    subcommand_metavar="CIPHER [ARGS...]",
    options_metavar="",
    epilog="Thanks for using this utility",
    help="""
    This app offers codecs to encrypt and decrypt textual messages.

    Examples:
    >>> main.py caesar encrypt "hello world" 3
    >>> khoor zruog
    >>> main.py ma decrypt "dsvvbkbnvw" -f samples/ma_sub_cipher_alphabet.txt
    >>> helloworld
    >>> main.py vigenere encrypt "diverttroopstoeastridge" "white" samples/vigenere_square
    >>> zpdxvpazhslzbhiwzbkmznm
    """,
)

__all__ = ["app"]

app.add_typer(caesar, name="caesar")
app.add_typer(ma, name="ma")
app.add_typer(vigenere, name="vigenere")


if __name__ == "__main__":
    app()
