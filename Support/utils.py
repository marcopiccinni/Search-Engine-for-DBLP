from os import system, name


def clear():
    """clear screen"""

    # for windows
    if name == 'nt':
        _ = system('cls')

    # UNIX BASED
    else:
        _ = system('clear')