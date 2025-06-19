from string import ascii_lowercase


def main() -> None:
    """
    Populates the samples/vigenere_square file with a Vigenere square

    :return: None
    """

    alphabet = ascii_lowercase

    final_list = []

    # The square should start with bcdef....
    first, rest = alphabet[0], alphabet[1:]
    alphabet = rest + first
    final_list.append(alphabet)

    for _ in range(len(alphabet) - 1):
        first, rest = alphabet[0], alphabet[1:]
        alphabet = rest + first
        final_list.append("\n" + alphabet)

    with open("samples/vigenere_square", "w") as file:
        file.writelines(final_list)


if __name__ == "__main__":
    main()
